"""
TODO:
 - hot comments:
  - upstream cfg: select * from v /*+ weak */;
  - col type ann/enforcement: select a /*+ type: char(36) */
  - catalog chainmap?
 - 'system: {}' -> 'system:' - null dc body = defaults? can't be global..
"""
import contextlib
import os.path
import typing as ta  # noqa

from omnibus import check  # noqa
from omnibus import dataclasses as dc  # noqa
from omnibus import inject as inj  # noqa
from omnibus import os as oos  # noqa
import pytest  # noqa

from .. import connectors as ctrs
from .. import elements as els
from .. import execution as exe
from .. import inference as infr
from .. import invalidations as invs  # noqa
from .. import planning as pln
from .. import rules as rls
from .. import sites  # noqa
from ... import domains as doms
from ...sql.tests.helpers import pg_engine  # noqa
from ...sql.tests.helpers import pg_url  # noqa  # FIXME: jesus christ pytest fucking sucks
from ...sql.tests.helpers import raw_pg_url
from ...types import QualifiedName  # noqa
from ...utils import secrets as sec  # noqa


def get_ele_dependencies(elements: ta.Iterable[els.Element]) -> ta.Mapping[els.Element, ta.AbstractSet[els.Element]]:  # noqa
    raise NotImplementedError


def get_src_table_domain(query: str, src: QualifiedName, dom: doms.Domain) -> doms.Domain:  # noqa
    raise NotImplementedError


class UrlSecretsReplacer(els.ElementProcessor):

    def __init__(self, secrets: sec.Secrets) -> None:
        super().__init__()

        self._secrets = check.isinstance(secrets, sec.Secrets)

    def processes(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return [e for e in elements.get_type_set(ctrs.sql.SqlConnector.Config) if e.url_secret]

    def process(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return [
            dc.replace(e, url=self._secrets[e.url_secret].value, url_secret=None)
            if isinstance(e, ctrs.sql.SqlConnector.Config) else e
            for e in elements
        ]


# @pytest.mark.xfail()
def test_ops(pg_engine, harness):  # noqa
    # binder = inj.create_binder()
    # binder.bind(CONNECTORS)
    # binder.bind(inj.Key(ta.Iterable[ctrs.Connector]), to=ctrs.ConnectorSet)
    # binder.bind(elements)
    # binder.bind(inj.Key(ta.Iterable[tars.Element]), to=tars.ElementSet)
    # injector = inj.create_injector(binder)  # noqa

    print(harness)
    with contextlib.ExitStack() as es:
        es.enter_context(oos.tmp_chdir(os.path.dirname(__file__)))

        secrets = sec.Secrets({'pg_url': raw_pg_url()})
        connectors: ta.Optional[ctrs.ConnectorSet] = None

        def epfac(eles, phase):
            if phase == els.processing.Phases.CONNECTORS + 1:
                nonlocal connectors
                connectors = ctrs.ConnectorSet.of(eles.get_type_set(ctrs.Connector.Config))

            if phase == els.processing.Phases.SITES:
                return [
                    sites.SiteProcessor(),
                ]

            elif phase == els.processing.Phases.CONNECTORS:
                return [
                    UrlSecretsReplacer(secrets),
                ]

            elif phase == els.processing.Phases.TARGETS:
                return [
                    rls.RuleElementProcessor(rls.TableAsSelectProcessor()),
                    infr.InferTableProcessor(connectors),
                ]

            else:
                return []

        elements = els.ElementSet.of([
            sites.Site('site0.yml'),
        ])

        elements = els.ElementProcessingDriver(epfac).process(elements)

        plan = pln.ElementPlanner(elements, connectors).plan({
            'pg/a',
            'pg/b',
            'pg/c',
            'pg/nums',
            'system/notifications',
        })

        exe.PlanExecutor(plan, connectors).execute()

        with pg_engine.connect() as pg_conn:
            print(list(pg_conn.execute('select * from a')))
            print(list(pg_conn.execute('select * from b')))
            print(list(pg_conn.execute('select * from c')))
            print(list(pg_conn.execute('select * from nums')))
