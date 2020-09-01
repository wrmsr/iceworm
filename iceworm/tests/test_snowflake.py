from omnibus import lang
import pytest
import sqlalchemy as sa

from .. import snowflake


@pytest.mark.xfail()
def test_conns():
    with lang.disposing(sa.create_engine(snowflake.get_url())) as engine:
        with engine.connect() as conn:
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
