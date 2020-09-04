import contextlib

from omnibus import check
from omnibus import lang
import pytest
import sqlalchemy as sa

from .. import snowflake
from .. import sql
from .. import tpch
from ..types import QualifiedName


@pytest.mark.xfail()
def test_conns():
    with contextlib.ExitStack() as es:
        engine = es.enter_context(lang.disposing(sa.create_engine(snowflake.get_url())))
        conn = es.enter_context(engine.connect())

        print(conn.scalar('select current_version()'))
        print(conn.scalar('select current_warehouse()'))
        print(conn.scalar('select current_database()'))
        print(conn.scalar('select current_schema()'))

        metadata = sa.MetaData()
        tbl = sa.Table('test', metadata, autoload=True, autoload_with=conn)
        print(tbl)

        # conn.engine.table_names(schema, connection=conn)

        metadata = sa.MetaData()
        metadata.reflect(bind=conn, only=['test'])
        print(metadata.tables['test'])


@pytest.mark.xfail()
def test_tpch():
    engine: sa.engine.Engine
    with contextlib.ExitStack() as es:
        engine = es.enter_context(lang.disposing(sa.create_engine(snowflake.get_url())))
        conn = es.enter_context(engine.connect())

        mdkw = {}
        cfg = snowflake.get_config()
        if cfg.get('schema'):
            mdkw['schema'] = cfg['schema']
        check.not_empty(mdkw['schema'])
        metadata = sa.MetaData(**mdkw)

        sats = tpch.build_sa_tables(metadata=metadata)
        for sat in sats:
            conn.execute(sql.DropTableIfExists(QualifiedName.of_dotted(sat.fullname)))
            sat.create(bind=conn)

        tpch.populate_sa_tables(conn, metadata)
