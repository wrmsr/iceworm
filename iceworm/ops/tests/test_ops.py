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
from omnibus import lang
import pytest

from .. import computed as cmp
from .. import connectors as ctrs
from .. import execution as exe
from .. import files
from .. import ops
from .. import sql
from ... import datatypes as dt
from ... import metadata as md
from ...trees import analysis as ana
from ...trees import datatypes as tdatatypes
from ...trees import nodes as no
from ...trees import origins
from ...trees import parsing as par
from ...trees import rendering
from ...trees import symbols
from ...trees import transforms as tfm
from ...types import QualifiedName
from ...utils import seq


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
            url=db_url,
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


class Materialization(dc.Pure):
    name: ta.Optional[QualifiedName] = dc.field(coerce=QualifiedName.of)


class View(dc.Pure):
    table: md.Table = dc.field(check=lambda o: isinstance(o, md.Table))
    query: str = dc.field(check=lambda o: isinstance(o, str))
    materializations: ta.Sequence[Materialization] = dc.field((), coerce=seq)


VIEWS = [

        View(
            md.Table(
                ['a'],
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('a', dt.Integer()),
                    md.Column('b', dt.Integer()),
                ],
            ),
            'select * from csv.a',
            [Materialization(['pg', 'a'])],
        ),

        View(
            md.Table(
                ['b'],
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('c', dt.Integer()),
                    md.Column('d', dt.Integer()),
                ],
            ),
            'select * from csv.b',
            [Materialization(['pg', 'b'])],
        ),

        View(
            md.Table(
                ['c'],
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('c', dt.Integer()),
                    md.Column('d', dt.Integer()),
                ],
            ),
            'select * from pg.b',
            [Materialization(['pg', 'c'])],
        ),

        View(
            md.Table(
                ['nums'],
                [
                    md.Column('num', dt.Integer(), primary_key=True),
                ]
            ),
            'select * from cmp.nums',
            [Materialization(['pg', 'nums'])],
        ),

        # View(
        #     md.Table(
        #         ['qnums'],
        #         [
        #             md.Column('num', dt.Integer(), primary_key=True),
        #         ]
        #     ),
        #     'select * from cmp.nums',
        #     [Materialization(['pg', 'nums'])],
        # ),

    ]


@pytest.mark.xfail()
def test_ops():
    with contextlib.closing(CONNECTORS['csv'].connect()) as fconn:
        print(fconn.reflect())
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
            ops.CreateTable: exe.CreateTableExecutor(conns),
            ops.CreateTableAs: exe.CreateTableAsExecutor(conns),
            ops.DropTable: exe.DropTableExecutor(conns),
            ops.InsertIntoSelect: exe.InsertIntoSelectExecutor(conns),
            ops.Transaction: exe.TransactionExecutor(conns),
        }

        def execute(op: ops.Op) -> None:
            executor = executors_by_op_cls[type(op)]
            if inspect.isgeneratorfunction(executor.execute):
                for child in executor.execute(op):
                    execute(child)
            else:
                check.none(executor.execute(op))

        ts = [
            ops.Transaction('pg', plan),
        ]
        for t in ts:
            execute(t)

        with contextlib.closing(CONNECTORS['pg'].connect()) as pconn:
            print(pconn.reflect([QualifiedName.of(['a'])]))

        sa_conn = check.isinstance(conns['pg'], sql.SqlConnection).sa_conn
        print(list(sa_conn.execute('select * from foo')))
        print(list(sa_conn.execute('select * from a')))
        print(list(sa_conn.execute('select * from b')))
        print(list(sa_conn.execute('select * from c')))
        print(list(sa_conn.execute('select * from nums')))


class World:

    def __init__(self, connectors: ctrs.ConnectorSet) -> None:
        super().__init__()

        self._ctors = check.isinstance(connectors, ctrs.ConnectorSet)

        self._views_by_name: ta.MutableMapping[QualifiedName, View] = {}

    def reflect(self, name: QualifiedName) -> ta.Sequence[md.Object]:
        objs = []

        if len(name) > 1 and name[0] in self._ctors:
            ctor = self._ctors[name[0]]
            with contextlib.closing(ctor.connect()) as conn:
                connobjs = conn.reflect([QualifiedName(name[1:])])
                if connobjs:
                    objs.append(check.single(connobjs.values()))

        for ctor in self._ctors:
            with contextlib.closing(ctor.connect()) as conn:
                connobjs = conn.reflect([name])
                if connobjs:
                    objs.extend(connobjs.values())

        return objs


@pytest.mark.xfail()
def test_queries():
    world = World(CONNECTORS)

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

        root = tfm.AliasRelationsTransformer(root)(root)
        root = tfm.LabelSelectItemsTransformer(root)(root)
        root = tfm.ExpandSelectsTransformer(root, cat)(root)
        print(rendering.render(root))

        syms = symbols.analyze(root, cat)
        oris = origins.analyze(root, syms)

        dts = tdatatypes.analyze(root, oris, cat)
        print(dts.dts_by_node[root])

        print()
