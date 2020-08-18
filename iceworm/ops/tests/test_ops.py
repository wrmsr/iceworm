import contextlib
import inspect
import os.path

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import docker
import pytest

from .. import connectors as ctrs
from .. import execution as exe
from .. import files
from .. import ops
from .. import sql
from ... import datatypes as dt
from ... import metadata as md
from ...types import QualifiedName


@pytest.fixture()
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


class View(dc.Pure):
    conn_name: str
    table: md.Table = dc.field(check=lambda o: isinstance(o, md.Table))
    src: QualifiedName = dc.field(coerce=QualifiedName.of)


@pytest.mark.xfail()
def test_ops(db_url):  # noqa
    cs = ctrs.ConnectorSet([
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
    ])

    plan = [
        ops.DropTable(['pg', 'foo']),
        ops.CreateTableAs(['pg', 'foo'], 'select 1'),
    ]

    views = [
        View(
            'pg',
            md.Table(
                'a',
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
                'b',
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
                'c',
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('c', dt.Integer()),
                    md.Column('d', dt.Integer()),
                ],
            ),
            ['pg', 'b'],
        ),
    ]

    for view in views:
        plan.extend([
            ops.DropTable([view.conn_name, view.table.name]),
            ops.CreateTable(view.conn_name, view.table),
            ops.InsertInto([view.conn_name, view.table.name], view.src),
        ])

    with contextlib.ExitStack() as es:
        conns = es.enter_context(contextlib.closing(ctrs.ConnectionSet(cs)))

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

        sa_conn = check.isinstance(conns['pg'], sql.SqlConnection).sa_conn
        print(list(sa_conn.execute('select * from foo')))
        print(list(sa_conn.execute('select * from a')))
        print(list(sa_conn.execute('select * from b')))
        print(list(sa_conn.execute('select * from c')))
