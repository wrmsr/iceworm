from omnibus import docker
from omnibus import lang
import pytest
import sqlalchemy as sa


@pytest.mark.xfail()
def test_docker_postgres():
    if docker.is_in_docker():
        (host, port) = 'iceworm-postgres-master', 5432

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_iceworm-postgres-master_1', 5432)])

        [(host, port)] = eps.values()

    engine: sa.engine.Engine
    with lang.disposing(sa.create_engine(f'postgresql+pg8000://iceworm:iceworm@{host}:{port}')) as engine:
        with engine.connect() as conn:
            print(conn.scalar(sa.select([sa.func.version()])))
