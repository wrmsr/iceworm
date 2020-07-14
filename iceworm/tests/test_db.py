from omnibus import lang
import pytest
import sqlalchemy as sa

from .. import db


@pytest.mark.xfail()
def test_db():
    with lang.disposing(sa.create_engine(db.get_url())) as engine:
        with engine.connect() as conn:
            print(conn.scalar('select current_version()'))
            print(conn.scalar('select current_warehouse()'))
            print(conn.scalar('select current_database()'))
            print(conn.scalar('select current_schema()'))

            metadata = sa.MetaData()
            tbl = sa.Table('test', metadata, autoload=True, autoload_with=conn)
            print(tbl)
