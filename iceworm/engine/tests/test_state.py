"""
TODO:
 -
"""
import os.path

from omnibus import lang
import pytest
import sqlalchemy as sa

from ...tests.helpers import pg_url  # noqa


@pytest.mark.xfail()
def test_state(pg_url):  # noqa
    with open(os.path.join(os.path.dirname(__file__), 'state.sql'), 'r') as f:
        buf = f.read()

    engine: sa.engine.Engine
    with lang.disposing(sa.create_engine(pg_url)) as engine:
        with engine.connect() as conn:
            conn.execute('DROP SCHEMA IF EXISTS "iceworm" CASCADE')
            conn.execute('CREATE SCHEMA IF NOT EXISTS "iceworm"')
            conn.execute('SET search_path TO "iceworm", "public"')

            if conn.scalar('SELECT COUNT(*) FROM pg_catalog.pg_user WHERE usename = \'iceworm\'') < 1:
                conn.execute('CREATE USER "iceworm" PASSWORD \'iceworm\'')
            conn.execute('ALTER ROLE "iceworm" SET search_path TO "iceworm", "public"')

            conn.execute('ALTER SCHEMA "iceworm" OWNER TO "iceworm"')

            conn.execute(buf)
