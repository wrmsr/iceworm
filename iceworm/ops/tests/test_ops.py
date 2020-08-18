"""
TODO:
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
from ...types import QualifiedName


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


class View(dc.Pure):
    conn_name: str
    table: md.Table = dc.field(check=lambda o: isinstance(o, md.Table))
    src: QualifiedName = dc.field(coerce=QualifiedName.of)
    materialized: bool = False


VIEWS = [

        View(
            'pg',
            md.Table(
                ['a'],
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('a', dt.Integer()),
                    md.Column('b', dt.Integer()),
                ],
            ),
            ['csv', 'a'],
        ),

        View(
            'pg',
            md.Table(
                ['b'],
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('c', dt.Integer()),
                    md.Column('d', dt.Integer()),
                ],
            ),
            ['csv', 'b'],
        ),

        View(
            'pg',
            md.Table(
                ['c'],
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('c', dt.Integer()),
                    md.Column('d', dt.Integer()),
                ],
            ),
            ['pg', 'b'],
        ),

        View(
            'pg',
            md.Table(
                ['nums'],
                [
                    md.Column('num', dt.Integer(), primary_key=True),
                ]
            ),
            ['cmp', 'nums'],
        ),

    ]


class World:

    def __init__(self, connectors: ctrs.ConnectorSet) -> None:
        super().__init__()

        self._connectors = check.isinstance(connectors, ctrs.ConnectorSet)

        self._views_by_name: ta.MutableMapping[QualifiedName, View] = {}

    def resolve(self, name: QualifiedName) -> ta.Sequence:
        objs = []

        if len(name) > 1 and name[0] in self._connectors:
            ctor = self._connectors[name[0]]
            with contextlib.closing(ctor.connect()) as conn:
                connobjs = conn.reflect([QualifiedName(name[1:])])
                if connobjs:
                    objs.append(check.single(connobjs.values()))

        for ctor in self._connectors:
            with contextlib.closing(ctor.connect()) as conn:
                connobjs = conn.reflect([name])
                if connobjs:
                    objs.extend(connobjs.values())

        return objs


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
        plan.extend([
            ops.DropTable([view.conn_name, *view.table.name]),
            ops.CreateTable(view.conn_name, view.table),
            ops.InsertInto([view.conn_name, *view.table.name], view.src),
        ])

    with contextlib.ExitStack() as es:
        conns = es.enter_context(contextlib.closing(ctrs.ConnectionSet(CONNECTORS)))

        executors_by_op_cls = {
            ops.CreateTable: exe.CreateTableExecutor(conns),
            ops.CreateTableAs: exe.CreateTableAsExecutor(conns),
            ops.DropTable: exe.DropTableExecutor(conns),
            ops.InsertInto: exe.InsertIntoExecutor(conns),
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
