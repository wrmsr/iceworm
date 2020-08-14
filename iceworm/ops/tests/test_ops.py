import csv
import inspect
import os.path

from omnibus import check
from omnibus import docker
from omnibus import lang
import pytest
import sqlalchemy as sa

from .. import execution
from .. import ops
from ...types import QualifiedName


@pytest.yield_fixture()
def db_engine():
    if docker.is_in_docker():
        (host, port) = 'iceworm-postgres', 5432

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_iceworm-postgres_1', 5432)])

        [(host, port)] = eps.values()

    engine: sa.engine.Engine
    with lang.disposing(sa.create_engine(f'postgresql+pg8000://iceworm:iceworm@{host}:{port}')) as engine:
        yield engine


@pytest.mark.xfail()
def test_ops(db_engine):  # noqa
    conn: sa.engine.Connection
    with db_engine.connect() as conn:
        print(conn.scalar(sa.select([sa.func.version()])))

        executors_by_op_cls = {
            ops.CreateTableAs: execution.CreateTableAsExecutor(conn),
            ops.DropTable: execution.DropTableExecutor(conn),
            ops.Transaction: execution.TransactionExecutor(conn),
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
            ]),
        ]
        for t in ts:
            execute(t)

        print(list(conn.execute('select * from foo')))


@pytest.mark.xfail()
def test_csv(db_engine):  # noqa
    conn: sa.engine.Connection
    with db_engine.connect() as conn:
        conn.execute('drop table if exists a;')
        conn.execute('create table a(id integer primary key, a int, b int);')

        with open(os.path.join(os.path.dirname(__file__), 'csv/a.csv'), 'r') as f:
            reader = csv.reader(f)
            rows = iter(reader)
            cols = next(rows)
            for vals in rows:
                row = dict(zip(cols, vals))
                print(row)
                conn.execute(sa.insert(sa.table('a')).values(row))

        print(list(conn.execute('select * from a')))
