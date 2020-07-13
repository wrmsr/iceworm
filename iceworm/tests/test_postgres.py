"""
TODO:
 - snowflake engine session sharing
"""
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
            create extension if not exists plv8;
            """))

            conn.execute(textwrap.dedent("""
            DO $$ plv8.elog(NOTICE, "hello there!"); $$ LANGUAGE plv8;
            """))

            conn.execute(textwrap.dedent("""
            create or replace function plv8_test(keys text[], vals text[]) returns json as $$
                var o = {};
                for(var i=0; i<keys.length; i++){
                    o[keys[i]] = vals[i];
                }
                return o;
            $$ language plv8 immutable strict;
            """))

            result = conn.scalar(textwrap.dedent("""
            select plv8_test(array['name', 'age'], array['tom', '29']);
            """))
            assert result == {'name': 'tom', 'age': '29'}

            conn.execute("""drop table if exists t""")
            conn.execute("""create table t(id integer primary key)""")
            metadata = sa.MetaData()
            t = sa.Table('t', metadata, autoload=True, autoload_with=engine)
            print(t)
