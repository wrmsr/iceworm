from omnibus import lang
import pytest
import sqlalchemy as sa

from .. import conns


@pytest.mark.xfail()
def test_conns():
    with lang.disposing(sa.create_engine(conns.get_url())) as engine:
        with engine.connect() as conn:
            print(conn.scalar('select current_version()'))
            print(conn.scalar('select current_warehouse()'))
            print(conn.scalar('select current_database()'))
            print(conn.scalar('select current_schema()'))

            metadata = sa.MetaData()
            tbl = sa.Table('test', metadata, autoload=True, autoload_with=conn)
            print(tbl)
