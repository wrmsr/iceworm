import inspect

from omnibus import check
from omnibus import docker
from omnibus import lang
import pytest
import sqlalchemy as sa

from .. import execution
from .. import tasks


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
def test_tasks(db_engine):  # noqa
    conn: sa.engine.Connection
    with db_engine.connect() as conn:
        print(conn.scalar(sa.select([sa.func.version()])))

        executors_by_task_cls = {
            tasks.CreateTableAs: execution.CreateTableAsExecutor(conn),
            tasks.DropTable: execution.DropTableExecutor(conn),
            tasks.Transaction: execution.TransactionExecutor(conn),
        }

        def execute(task: tasks.Task) -> None:
            executor = executors_by_task_cls[type(task)]
            if inspect.isgeneratorfunction(executor.execute):
                for child in executor.execute(task):
                    execute(child)
            else:
                check.none(executor.execute(task))

        ts = [
            tasks.Transaction([
                tasks.DropTable('foo'),
                tasks.CreateTableAs('foo', 'select 1'),
            ]),
        ]
        for t in ts:
            execute(t)

        print(list(conn.execute('select * from foo')))
