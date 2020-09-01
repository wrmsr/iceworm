"""
TODO:
 - hot comments:
  - upstream cfg: select * from v /*+ weak */;
  - col type ann/enforcement: select a /*+ type: char(36) */
  - catalog chainmap?
"""
import os.path
import typing as ta  # noqa

from omnibus import check  # noqa
from omnibus import dataclasses as dc  # noqa
from omnibus import inject as inj  # noqa
import pytest

from .. import connectors as ctrs
from .. import execution as exe
from .. import planning as pln
from .. import processing as proc
from .. import rules as rls
from .. import targets as tars
from ...tests.helpers import pg_engine  # noqa
from ...tests.helpers import pg_url  # noqa  # FIXME: jesus christ pytest fucking sucks
from ...tests.helpers import raw_pg_url
from ...types import QualifiedName  # noqa
from ...utils import secrets as sec  # noqa
from ...utils import serde


CONNECTORS_SER = [

    {'system': {}},

    {'sql': {
        'name': 'pg',

        'url_secret': 'pg_url',
        # 'url': raw_pg_url(),
    }},

    {'file': {
        'name': 'csv',
        'mounts': [
            {'mount': {
                'path': os.path.join(os.path.dirname(__file__), 'csv'),
                'schema': {'provided': {
                    'columns': [
                        {'column': {'name': 'id', 'type': {'integer': {}}, 'primary_key': True}},
                        {'column': {'name': 'a', 'type': {'integer': {}}}},
                        {'column': {'name': 'b', 'type': {'integer': {}}}},
                    ],
                }},
                'globs': [
                    '*.csv',
                ],
            }},
        ],
    }},

    {'computed': {
        'name': 'cmp',
        'tables': [
            {'table': {
                'md_table': {'table': {
                    'name': ['nums'],
                    'columns': [
                        {'column': {'name': 'num', 'type': {'integer': {}}}},
                    ],
                }},
                'fn': lambda: [{'num': i} for i in range(10)],
            }},
        ],
    }},

]


TARGETS_SER = [
    {'table_as_select': {
        'name': ['pg', 'a'],
        'query': 'select * from csv.a',
    }},
    {'table_as_select': {
        'name': ['pg', 'b'],
        'query': 'select * from csv.b',
    }},
    {'table_as_select': {
        'name': ['pg', 'c'],
        'query': 'select * from pg.b',
    }},
    {'table_as_select': {
        'name': ['pg', 'nums'],
        'query': 'select * from cmp.nums',
    }},
    {'rows': {
        'table': ['system', 'notifications'],
        'query': "select 'hi' message",
    }},
]


@pytest.mark.xfail()
def test_ops(pg_engine):  # noqa
    # binder = inj.create_binder()
    # binder.bind(CONNECTORS)
    # binder.bind(inj.Key(ta.Iterable[ctrs.Connector]), to=ctrs.ConnectorSet)
    # binder.bind(targets)
    # binder.bind(inj.Key(ta.Iterable[tars.Target]), to=tars.TargetSet)
    # injector = inj.create_injector(binder)  # noqa

    secrets = sec.Secrets({'pg_url': raw_pg_url()})

    ctor_cfgs = serde.deserialize(CONNECTORS_SER, ta.Sequence[ctrs.Connector.Config])
    for i, ctor_cfg in list(enumerate(ctor_cfgs)):
        if isinstance(ctor_cfg, ctrs.sql.SqlConnector.Config) and ctor_cfg.url_secret is not None:
            ctor_cfgs[i] = dc.replace(ctor_cfg, url=secrets[ctor_cfg.url_secret].value, url_secret=None)

    connectors = ctrs.ConnectorSet.of(ctor_cfgs)

    targets = tars.TargetSet.of(serde.deserialize(TARGETS_SER, ta.Sequence[tars.Target]))

    tprocs = [
        tars.RuleTargetProcessor(rls.TableAsSelectProcessor()),
        proc.InferTableProcessor(connectors),
    ]

    targets = list(targets)
    while True:
        print(list(targets))
        mtps = [tp for tp in tprocs if tp.matches(targets)]
        if not mtps:
            break
        targets = mtps[0].process(targets)

    plan = pln.TargetPlanner(targets, connectors).plan(set(map(QualifiedName.of, [
        ['pg', 'a'],
        ['pg', 'b'],
        ['pg', 'c'],
        ['pg', 'nums'],
        ['system', 'notifications'],
    ])))

    exe.PlanExecutor(plan, connectors).execute()

    with pg_engine.connect() as pg_conn:
        print(list(pg_conn.execute('select * from a')))
        print(list(pg_conn.execute('select * from b')))
        print(list(pg_conn.execute('select * from c')))
        print(list(pg_conn.execute('select * from nums')))
