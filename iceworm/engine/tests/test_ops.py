"""
TODO:
 - hot comments:
  - upstream cfg: select * from v /*+ weak */;
  - col type ann/enforcement: select a /*+ type: char(36) */
  - catalog chainmap?
 - 'system: {}' -> 'system:' - null dc body = defaults? can't be global..
"""
import os.path
import typing as ta  # noqa

from omnibus import check  # noqa
from omnibus import dataclasses as dc  # noqa
from omnibus import inject as inj  # noqa
import pytest  # noqa
import yaml

from .. import connectors as ctrs
from .. import execution as exe
from .. import invalidations as invs  # noqa
from .. import planning as pln
from .. import processing as proc
from .. import rules as rls
from .. import elements as els
from ... import domains as doms
from ...tests.helpers import pg_engine  # noqa
from ...tests.helpers import pg_url  # noqa  # FIXME: jesus christ pytest fucking sucks
from ...tests.helpers import raw_pg_url
from ...types import QualifiedName  # noqa
from ...utils import secrets as sec  # noqa
from ...utils import serde


CONNECTORS_YML = f"""

- system_connector: {{}}

- sql_connector:
    id: pg
    url_secret: pg_url

- file_connector:
    id: csv
    mounts:
    - path: {os.path.join(os.path.dirname(__file__), 'csv')}
      schema:
        provided:
          columns:
          - {{name: id, type: integer, primary_key: true}}
          - {{name: a, type: integer}}
          - {{name: b, type: integer}}
      globs:
      - '*.csv'

"""

CONNECTORS_SER = yaml.safe_load(CONNECTORS_YML)

CONNECTORS_SER.extend([

    {'computed_connector': {
        'id': 'cmp',
        'tables': [
            {
                'md_table': {
                    'name': ['nums'],
                    'columns': [
                        {'name': 'num', 'type': 'integer'},
                    ],
                },
                'fn': lambda: [{'num': i} for i in range(10)],
            },
        ],
    }},

])

ELEMENTS_YML = """

- table_as_select:
    table: [pg, a]
    query: "select * from csv.a"

- table_as_select:
    table: [pg, b]
    query: "select * from csv.b"

- table_as_select:
    table: [pg, c]
    query: "select * from pg.b"

- table_as_select:
    table: [pg, nums]
    query: "select * from cmp.nums"

- table:
    id: system/notifications

- materialization:
    table: system/notifications
    dst: [system, notifications]

- rows:
    table: system/notifications
    query: "select 'hi' as message"

- invalidator:
    target: pg/a
    trigger:
      scheduled:
        spec: '0 1 * * *'

"""

ELEMENTS_SER = yaml.safe_load(ELEMENTS_YML)


def get_ele_dependencies(elements: ta.Iterable[els.Element]) -> ta.Mapping[els.Element, ta.AbstractSet[els.Element]]:  # noqa
    raise NotImplementedError


def get_src_table_domain(query: str, src: QualifiedName, dom: doms.Domain) -> doms.Domain:  # noqa
    raise NotImplementedError


# @pytest.mark.xfail()
def test_ops(pg_engine):  # noqa
    # binder = inj.create_binder()
    # binder.bind(CONNECTORS)
    # binder.bind(inj.Key(ta.Iterable[ctrs.Connector]), to=ctrs.ConnectorSet)
    # binder.bind(elements)
    # binder.bind(inj.Key(ta.Iterable[tars.Element]), to=tars.ElementSet)
    # injector = inj.create_injector(binder)  # noqa

    secrets = sec.Secrets({'pg_url': raw_pg_url()})

    ctor_cfgs = serde.deserialize(CONNECTORS_SER, ta.Sequence[ctrs.Connector.Config])

    def replace_url_secrets(cfg: ctrs.Connector.Config) -> ta.Mapping[str, ta.Any]:
        if isinstance(cfg, ctrs.sql.SqlConnector.Config) and cfg.url_secret is not None:
            return {'url': secrets[cfg.url_secret].value, 'url_secret': None}
        else:
            return {}

    ctor_cfgs = [cfg.fmap(replace_url_secrets) for cfg in ctor_cfgs]

    connectors = ctrs.ConnectorSet.of(ctor_cfgs)

    elements = els.ElementSet.of(serde.deserialize(ELEMENTS_SER, ta.Sequence[els.Element]))

    tprocs = [
        rls.RuleElementProcessor(rls.TableAsSelectProcessor()),
        proc.InferTableProcessor(connectors),
    ]

    elements = els.ElementSet.of(elements)
    while True:
        print(list(elements))
        mtps = [tp for tp in tprocs if tp.processes(elements)]
        if not mtps:
            break
        elements = els.ElementSet.of(mtps[0].process(elements))

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
