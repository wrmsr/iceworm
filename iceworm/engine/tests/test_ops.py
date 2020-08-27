"""
TODO:
 - db nuke fixture
 - hot comments:
  - upstream cfg: select * from v /*+ weak */;
  - col type ann/enforcement: select a /*+ type: char(36) */
  - catalog chainmap?
"""
import contextlib
import inspect
import os.path
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import docker
from omnibus import inject as inj
from omnibus import lang
import pytest

from .. import computed as cmp
from .. import connectors as ctrs
from .. import execution as exe
from .. import files
from .. import ops
from .. import sql
from .. import targets as tars
from .. import transforms as tfm
from .. import worlds as wo
from ... import datatypes as dt
from ... import metadata as md
from ...trees import analysis as ana
from ...trees import datatypes as tdatatypes
from ...trees import nodes as no
from ...trees import origins
from ...trees import parsing as par
from ...trees import rendering
from ...trees import symbols
from ...trees import transforms as ttfm
from ...types import QualifiedName
from ...utils import secrets as sec
from ..base import Op


@lang.cached_nullary
def db_url():
    if docker.is_in_docker():
        (host, port) = 'iceworm-postgres', 5432

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_iceworm-postgres_1', 5432)])

        [(host, port)] = eps.values()

    return f'postgresql+psycopg2://iceworm:iceworm@{host}:{port}'


CONNECTORS = ctrs.ConnectorSet([

    sql.SqlConnector(
        'pg',
        sql.SqlConnector.Config(
            url=sec.ComputedSecret(db_url),
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


TARGETS = [

    tars.Table(

    ),

]

VIEWS = [

        wo.View(
            md.Table(
                ['a'],
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('a', dt.Integer()),
                    md.Column('b', dt.Integer()),
                ],
            ),
            'select * from csv.a',
            [wo.Materialization(['pg', 'a'])],
        ),

        wo.View(
            md.Table(
                ['b'],
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('c', dt.Integer()),
                    md.Column('d', dt.Integer()),
                ],
            ),
            'select * from csv.b',
            [wo.Materialization(['pg', 'b'])],
        ),

        wo.View(
            md.Table(
                ['c'],
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('c', dt.Integer()),
                    md.Column('d', dt.Integer()),
                ],
            ),
            'select * from pg.b',
            [wo.Materialization(['pg', 'c'])],
        ),

        wo.View(
            md.Table(
                ['nums'],
                [
                    md.Column('num', dt.Integer(), primary_key=True),
                ]
            ),
            'select * from cmp.nums',
            [wo.Materialization(['pg', 'nums'])],
        ),

        # wo.View(
        #     md.Table(
        #         ['qnums'],
        #         [
        #             md.Column('num', dt.Integer(), primary_key=True),
        #         ]
        #     ),
        #     'select * from cmp.nums',
        #     [wo.Materialization(['pg', 'nums'])],
        # ),

    ]


@pytest.mark.xfail()
def test_ops():
    with contextlib.closing(CONNECTORS['csv'].connect()) as fconn:
        # print(fconn.reflect())
        print(fconn.reflect([QualifiedName.of(['a'])]))

    plan = [
        ops.DropTable(['pg', 'foo']),
        ops.CreateTableAs(['pg', 'foo'], 'select 1'),
    ]

    for view in VIEWS:
        for mat in view.materializations:
            plan.extend([
                ops.DropTable(mat.name),
                ops.CreateTable(dc.replace(view.table, name=mat.name)),
                ops.InsertIntoSelect(mat.name, view.query),
            ])

    with contextlib.ExitStack() as es:
        conns = es.enter_context(contextlib.closing(ctrs.ConnectionSet(CONNECTORS)))

        executors_by_op_cls = {
            ops.AtomicCreateTableAs: exe.AtomicCreateTableAsExecutor(conns),
            ops.CreateTable: exe.CreateTableExecutor(conns),
            ops.DropTable: exe.DropTableExecutor(conns),
            ops.InsertIntoSelect: exe.InsertIntoSelectExecutor(conns),
            ops.List: exe.ListExecutor(),
            ops.Transaction: exe.TransactionExecutor(conns),
        }

        def execute(op: Op) -> None:
            executor = executors_by_op_cls[type(op)]
            if inspect.isgeneratorfunction(executor.execute):
                for child in executor.execute(op):
                    execute(child)
            else:
                check.none(executor.execute(op))

        root = ops.Transaction({'pg'}, ops.List(plan))

        root = tfm.CreateTableAsAtomizer()(root)

        execute(root)

        with contextlib.closing(CONNECTORS['pg'].connect()) as pconn:
            print(pconn.reflect([QualifiedName.of(['a'])]))

        sa_conn = check.isinstance(conns['pg'], sql.SqlConnection).sa_conn
        print(list(sa_conn.execute('select * from foo')))
        print(list(sa_conn.execute('select * from a')))
        print(list(sa_conn.execute('select * from b')))
        print(list(sa_conn.execute('select * from c')))
        print(list(sa_conn.execute('select * from nums')))


@pytest.mark.xfail()
def test_queries():
    binder = inj.create_binder()

    binder.bind(CONNECTORS)
    binder.bind(wo.World, as_singleton=True)

    injector = inj.create_injector(binder)

    world = injector[wo.World]

    for query in [
        'select * from cmp.nums',
        'select * from csv.a',
        'select * from pg.test',
        'select * from cmp.nums, csv.a, pg.test',
    ]:
        print(query)

        root = par.parse_statement(query)

        table_names = {
            tn.name.name
            for tn in ana.basic(root).get_node_type_set(no.Table)
        }

        alias_sets_by_tbl: ta.MutableMapping[md.Object, ta.Set[QualifiedName]] = ocol.IdentityKeyDict()
        for tn in table_names:
            obj = check.single(world.reflect(tn))
            aset = alias_sets_by_tbl.setdefault(obj, set())
            if tn != obj.name:
                aset.add(tn)

        cat = md.Catalog(
            tables=[
                dc.replace(t, aliases={*t.aliases, *aset}) if aset else t
                for t, aset in alias_sets_by_tbl.items()
            ],
        )

        print(cat)

        root = ttfm.AliasRelationsTransformer(root)(root)
        root = ttfm.LabelSelectItemsTransformer(root)(root)
        root = ttfm.ExpandSelectsTransformer(root, cat)(root)
        print(rendering.render(root))

        syms = symbols.analyze(root, cat)
        oris = origins.analyze(root, syms)

        dts = tdatatypes.analyze(root, oris, cat)
        print(dts.dts_by_node[root])

        print()
