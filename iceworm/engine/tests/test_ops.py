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
from omnibus import inject as inj  # noqa
import pytest

from .. import connectors as ctrs
from .. import execution as exe
from .. import planning as pln
from .. import processing as proc
from .. import targets as tars
from ... import datatypes as dt
from ... import metadata as md
from ...tests.helpers import pg_engine  # noqa
from ...tests.helpers import pg_url  # noqa  # FIXME: jesus christ pytest fucking sucks
from ...tests.helpers import raw_pg_url
from ...utils import secrets as sec
from ..connectors import computed as cmp
from ..connectors import files
from ..connectors import sql


CONNECTORS = ctrs.ConnectorSet([

    sql.SqlConnector(
        'pg',
        sql.SqlConnector.Config(
            url=sec.ComputedSecret(raw_pg_url),
        ),
    ),

    files.FileConnector(
        'csv',
        files.FileConnector.Config(
            mounts=[
                files.Mount(
                    os.path.join(os.path.dirname(__file__), 'csv'),
                    files.ProvidedSchemaPolicy([
                        md.Column('id', dt.Integer(), primary_key=True),
                        md.Column('a', dt.Integer()),
                        md.Column('b', dt.Integer()),
                    ]),
                    [
                        '*.csv',
                    ],
                ),
            ],
        ),
    ),

    cmp.ComputedConnector(
        'cmp',
        cmp.ComputedConnector.Config(
            tables=[
                cmp.Table(
                    md.Table(
                        ['nums'],
                        [
                            md.Column('num', dt.Integer()),
                        ],
                    ),
                    lambda: [{'num': i} for i in range(10)],
                ),
            ],
        ),
    ),

])


TARGETS = tars.TargetSet([

    tars.Table(['pg', 'a']),
    tars.Rows(['pg', 'a'], 'select * from csv.a'),

    tars.Table(['pg', 'b']),
    tars.Rows(['pg', 'b'], 'select * from csv.b'),

    tars.Table(['pg', 'c']),
    tars.Rows(['pg', 'c'], 'select * from pg.b'),

    tars.Table(['pg', 'nums']),
    tars.Rows(['pg', 'nums'], 'select * from cmp.nums'),

])


@pytest.mark.xfail()
def test_ops(pg_engine):  # noqa
    # binder = inj.create_binder()
    # binder.bind(CONNECTORS)
    # binder.bind(inj.Key(ta.Iterable[ctrs.Connector]), to=ctrs.ConnectorSet)
    # binder.bind(TARGETS)
    # binder.bind(inj.Key(ta.Iterable[tars.Target]), to=tars.TargetSet)
    # injector = inj.create_injector(binder)  # noqa

    with pg_engine.connect() as pg_conn:
        print(list(pg_conn.execute('select 1')))

    tprocs = [
        proc.InferTableProcessor(CONNECTORS)
    ]

    targets = TARGETS
    while True:
        mtps = [tp for tp in tprocs if tp.matches(targets)]
        if not mtps:
            break
        targets = mtps[0].process(targets)

    plan = pln.TargetPlanner(targets, CONNECTORS).plan

    exe.PlanExecutor(plan, CONNECTORS).execute()

    with pg_engine.connect() as pg_conn:
        print(list(pg_conn.execute('select * from a')))
        print(list(pg_conn.execute('select * from b')))
        print(list(pg_conn.execute('select * from c')))
        print(list(pg_conn.execute('select * from nums')))
