import contextlib
import itertools
import os.path
import typing as ta  # noqa

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import inject as inj
from omnibus import lang  # noqa
from omnibus import os as oos  # noqa
from omnibus import properties
from omnibus.inject.dev import pytest as ptinj
import pytest  # noqa
import yaml  # noqa

from .. import connectors as ctrs
from .. import elements as els
from .. import inject as einj
from .. import ops
from .. import plans as pln
from .. import sites
from .. import targets as tars  # noqa
from ... import sql
from ...sql.tests.helpers import DbManager
from ...trees import nodes as no
from ...trees import parsing as par
from ...types import QualifiedName  # noqa
from ...utils import secrets as sec  # noqa
from ...utils import serde
from ...utils import unique_dict


# def get_ele_dependencies(elements: ta.Iterable[els.Element]) -> ta.Mapping[els.Element, ta.AbstractSet[els.Element]]:  # noqa
#     raise NotImplementedError


# def get_src_table_domain(query: str, src: QualifiedName, dom: doms.Domain) -> doms.Domain:  # noqa
#     raise NotImplementedError


class UrlSecretsReplacer(els.ElementProcessor):

    def __init__(self, secrets: sec.Secrets) -> None:
        super().__init__()

        self._secrets = check.isinstance(secrets, sec.Secrets)

    def match(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return [e for e in elements.get_type_set(ctrs.impls.sql.SqlConnector.Config) if e.url_secret]

    def process(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return [
            dc.replace(e, url=self._secrets[e.url_secret].value, url_secret=None)
            if isinstance(e, ctrs.impls.sql.SqlConnector.Config) else e
            for e in elements
        ]


@pytest.yield_fixture()
def exit_stack() -> ta.Iterator[contextlib.ExitStack]:
    with contextlib.ExitStack() as es:
        yield es


class Helper:

    def __init__(self, harness: ptinj.Harness) -> None:
        super().__init__()
        self._harness = harness

    @properties.cached
    @property
    def secrets(self) -> sec.Secrets:
        return sec.Secrets({'pg_url': self._harness[DbManager].pg_url})

    @properties.cached
    @property
    def injector(self) -> inj.Injector:
        binder = inj.create_binder()
        binder.bind(sec.Secrets, to_instance=self.secrets)
        sql.inject.install(binder)
        einj.install(binder)

        def _install_elements(b):
            els.inject.bind_element_processor(b, UrlSecretsReplacer, els.Phases.CONNECTORS)

        els.inject.bind_elements_module(binder, _install_elements)

        binder.bind(inj.Key(ta.Callable[[str], no.Node]), to_instance=par.parse_stmt)

        return inj.create_injector(binder)

    @properties.cached
    @property
    def elements_and_connectors(self) -> ta.Tuple[els.ElementSet, ctrs.ConnectorSet]:
        elements_injector = self.injector[inj.Key(inj.Injector, 'elements')]

        with els.inject.new_driver_scope(elements_injector) as drv:
            elements = drv.run([
                sites.Site('site0.yml'),
            ])
            connectors = drv[ctrs.ConnectorSet]

        return elements, connectors

    @property
    def elements(self) -> els.ElementSet:
        return self.elements_and_connectors[0]

    @property
    def connectors(self) -> ctrs.ConnectorSet:
        return self.elements_and_connectors[1]

    def verify_elements_serde(self) -> None:
        selements = serde.serialize(list(self.elements), ta.Sequence[els.Element])
        delements = els.ElementSet.of(serde.deserialize(selements, ta.Sequence[els.Element]))
        assert list(delements) == list(self.elements)

        print(yaml.dump(selements))

    def execute(self) -> None:
        with contextlib.closing(ctrs.ConnectionSet(self.connectors)) as conns:
            execution_injector = self.injector[inj.Key(inj.Injector, 'execution')]

            with ops.inject.new_execution_scope(execution_injector, conns):
                matrs_by_mat_id = unique_dict(
                    (matr.target.id, matr) for matr in self.elements.get_type_set(pln.Materializer))

                deps = {mat_id: {d.id for d in matr.srcs} for mat_id, matr in matrs_by_mat_id.items()}

                oed: ops.OpExecutionDriver = execution_injector[ops.OpExecutionDriver]
                for mat_id in itertools.chain.from_iterable(ocol.toposort(deps)):
                    matr = matrs_by_mat_id[mat_id]
                    oed.execute(matr.op)


def test_inject(harness: ptinj.Harness, exit_stack):
    exit_stack.enter_context(oos.tmp_chdir(os.path.dirname(__file__)))

    helper = Helper(harness)

    helper.verify_elements_serde()
    helper.execute()

    with harness[DbManager].pg_engine.connect() as pg_conn:
        print(list(pg_conn.execute('select * from a')))
        print(list(pg_conn.execute('select * from b')))
        print(list(pg_conn.execute('select * from c')))
        print(list(pg_conn.execute('select * from d')))
        print(list(pg_conn.execute('select * from nums')))
