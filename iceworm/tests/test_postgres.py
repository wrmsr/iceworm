import textwrap

from omnibus import docker
from omnibus import lang
import pytest
import sqlalchemy as sa


@pytest.mark.xfail()
def test_docker_postgres():
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
        with engine.connect() as conn:
            print(conn.scalar(sa.select([sa.func.version()])))

            conn.execute(textwrap.dedent("""
            CREATE EXTENSION IF NOT EXISTS plv8;
            """))

            conn.execute(textwrap.dedent("""
            DO $$ plv8.elog(NOTICE, "hello there!"); $$ LANGUAGE plv8;
            """))

            conn.execute(textwrap.dedent("""
            CREATE OR REPLACE FUNCTION plv8_test(keys TEXT[], vals TEXT[]) RETURNS JSON AS $$
                var o = {};
                for(var i=0; i<keys.length; i++){
                    o[keys[i]] = vals[i];
                }
                return o;
            $$ LANGUAGE plv8 IMMUTABLE STRICT;
            """))

            result = conn.scalar(textwrap.dedent("""
            SELECT plv8_test(ARRAY['name', 'age'], ARRAY['Tom', '29']);
            """))
            assert result == {'name': 'Tom', 'age': '29'}
