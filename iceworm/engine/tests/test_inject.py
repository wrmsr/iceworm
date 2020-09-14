import contextlib
import os.path
import typing as ta  # noqa

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import inject as inj
from omnibus import lang  # noqa
from omnibus import os as oos  # noqa
import pytest  # noqa

from .. import connectors as ctrs
from .. import elements as els
from .. import ops
from .. import planning as pln
from .. import rules as rls
from .. import sites
from .. import targets as tars
from ... import domains as doms
from ... import sql
from ...sql.tests.helpers import DbManager
from ...tests import harness as har
from ...trees import nodes as no
from ...trees import parsing as par
from ...types import QualifiedName  # noqa
from ...utils import secrets as sec  # noqa
from ...utils import serde


def get_ele_dependencies(elements: ta.Iterable[els.Element]) -> ta.Mapping[els.Element, ta.AbstractSet[els.Element]]:  # noqa
    raise NotImplementedError


def get_src_table_domain(query: str, src: QualifiedName, dom: doms.Domain) -> doms.Domain:  # noqa
    raise NotImplementedError


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


def install_element_processors(binder: inj.Binder) -> inj.Binder:
    els.inject.bind_element_processor(binder, UrlSecretsReplacer, els.Phases.CONNECTORS)

    binder.bind(inj.Key(ta.Callable[[str], no.Node]), to_instance=par.parse_stmt)

    ctrs.inject.install(binder)
    els.inject.install(binder)
    rls.inject.install(binder)
    sites.inject.install(binder)
    tars.inject.install(binder)

    return binder


# @pytest.mark.xfail
def test_inject(harness: har.Harness):
    with contextlib.ExitStack() as es:
        es.enter_context(oos.tmp_chdir(os.path.dirname(__file__)))

        secrets = sec.Secrets({'pg_url': harness[DbManager].pg_url})

        binder = inj.create_binder()
        binder.bind(sec.Secrets, to_instance=secrets)
        sql.inject.install(binder)
        install_element_processors(binder)
        drv = els.inject.InjectionElementProcessingDriver(binder)
        elements = drv.run([
            sites.Site('site0.yml'),
        ])

        print(elements)
        selements = serde.serialize(list(elements))
        delements = els.ElementSet.of(serde.deserialize(selements, ta.Sequence[els.Element]))
        assert list(delements) == list(elements)

        print(__import__('yaml').dump(selements))

        connectors = drv[ctrs.ConnectorSet]
        conns = es.enter_context(contextlib.closing(ctrs.ConnectionSet(connectors)))
        plan = pln.ElementPlanner(elements, connectors).plan({
            'pg/a',
            'pg/b',
            'pg/c',
            'pg/d',
            'pg/nums',
            'system/notifications',
        })

        binder = inj.create_binder()
        binder.bind(ctrs.ConnectorSet, to_instance=connectors)
        binder.bind(ctrs.ConnectionSet, to_instance=conns)
        ops.inject.install(binder)
        injector = inj.create_injector(binder)
        injector[ops.OpExecutionDriver].execute(plan)

        with harness[DbManager].pg_engine.connect() as pg_conn:
            print(list(pg_conn.execute('select * from a')))
            print(list(pg_conn.execute('select * from b')))
            print(list(pg_conn.execute('select * from c')))
            print(list(pg_conn.execute('select * from nums')))
