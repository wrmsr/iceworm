import typing as ta

from omnibus import lang
from omnibus import lifecycles as lc
from omnibus import properties
from omnibus.docker.dev.pytest import DockerManager
from omnibus.inject.dev import pytest as ptinj
import sqlalchemy as sa

from .. import snowflake


@ptinj.bind(ptinj.Function)
class DbManager(lc.ContextManageableLifecycle):

    def __init__(
            self,
            dm: DockerManager,
            request: ptinj.FixtureRequest,
            *,
            switches: ta.Optional[ptinj.Switches] = None,
    ) -> None:
        super().__init__()

        self._dm = dm
        self._request = request
        self._switches = switches

    @properties.stateful_cached
    @property
    def pg_url(self) -> str:
        [(host, port)] = self._dm.get_container_tcp_endpoints([('postgres', 5432)]).values()
        env = self._dm.compose_config['postgres']['environment']
        url = f"postgresql+psycopg2://{env['POSTGRES_USER']}:{env['POSTGRES_PASSWORD']}@{host}:{port}"
        with lang.disposing(sa.engine.create_engine(url)) as engine:
            clean_pg(engine)
        return url

    @properties.stateful_cached
    @property
    def pg_engine(self) -> sa.engine.Engine:
        return self._lifecycle_exit_stack.enter_context(lang.disposing(sa.engine.create_engine(self.pg_url)))

    @properties.stateful_cached
    @property
    def snowflake_engine(self) -> sa.engine.Engine:
        self._switches.skip_if_not('online')
        return self._lifecycle_exit_stack.enter_context(lang.disposing(sa.engine.create_engine(snowflake.get_url())))


def clean_pg(engine: sa.engine.Engine) -> None:
    with engine.connect() as conn:
        conn.execute('DROP SCHEMA IF EXISTS "iceworm" CASCADE')
        conn.execute('CREATE SCHEMA IF NOT EXISTS "iceworm"')
        conn.execute('SET search_path TO "iceworm", "public"')

        if conn.scalar('SELECT COUNT(*) FROM pg_catalog.pg_user WHERE usename = \'iceworm\'') < 1:
            conn.execute('CREATE USER "iceworm" PASSWORD \'iceworm\'')
        conn.execute('ALTER ROLE "iceworm" SET search_path TO "iceworm", "public"')

        conn.execute('ALTER SCHEMA "iceworm" OWNER TO "iceworm"')
