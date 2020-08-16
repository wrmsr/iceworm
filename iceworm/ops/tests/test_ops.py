import contextlib
import inspect
import os.path

from omnibus import check
from omnibus import docker
from omnibus import lang
import pytest
import sqlalchemy as sa

from .. import connectors as ctrs
from .. import execution as exe
from .. import ops
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


@pytest.yield_fixture()
def db_engine(db_url):
    engine: sa.engine.Engine
    with lang.disposing(sa.create_engine(db_url)) as engine:
        yield engine


@pytest.mark.xfail()
def test_ops(db_url):  # noqa
    cata = md.Catalog(
        [
            md.Table(
                'a',
                [
                    md.Column('id', dt.Integer(), primary_key=True),
                    md.Column('a', dt.Integer()),
                    md.Column('b', dt.Integer()),
                ],
            ),
        ],
    )

    cs = ctrs.ConnectorSet([
        ctrs.SqlConnector(
            'pg',
            ctrs.SqlConnector.Config(
                url=db_url,
            ),
        ),
        ctrs.FileConnector(
            'csv',
            os.path.join(os.path.dirname(__file__), 'csv/a.csv'),
        ),
    ])

    with contextlib.ExitStack() as es:
        engine: sa.engine.Engine = es.enter_context(lang.disposing(cs['pg'].create_engine()))
        conn: sa.engine.Connection = es.enter_context(engine.connect())

        executors_by_op_cls = {
            ops.CreateTable: exe.CreateTableExecutor(conn),
            ops.CreateTableAs: exe.CreateTableAsExecutor(conn),
            ops.DropTable: exe.DropTableExecutor(conn),
            ops.InsertInto: exe.InsertIntoExecutor(conn, cata),
            ops.Transaction: exe.TransactionExecutor(conn),
        }

        def execute(op: ops.Op) -> None:
            executor = executors_by_op_cls[type(op)]
            if inspect.isgeneratorfunction(executor.execute):
                for child in executor.execute(op):
                    execute(child)
            else:
                check.none(executor.execute(op))

        ts = [
            ops.Transaction([
                ops.DropTable(QualifiedName(['foo'])),
                ops.CreateTableAs(QualifiedName(['foo']), 'select 1'),

                ops.DropTable(QualifiedName(['a'])),
                ops.CreateTable(cata.tables_by_name['a']),
                ops.InsertInto(QualifiedName(['a']), QualifiedName(['csv'])),
            ]),
        ]
        for t in ts:
            execute(t)

        print(list(conn.execute('select * from foo')))
        print(list(conn.execute('select * from a')))
