import textwrap
import typing as ta

from omnibus import check
from omnibus import lang
import pytest
import sqlalchemy as sa
import sqlalchemy.pool

from .. import alchemy as alch
from .. import metadata as md


@pytest.yield_fixture()
def sqlite_engine() -> ta.Generator[sa.engine.Engine, None, None]:
    engine: sa.engine.Engine
    with lang.disposing(
            sa.create_engine(
                'sqlite://',
                connect_args={'check_same_thread': False},
                poolclass=sa.pool.StaticPool,
            )
    ) as engine:
        yield engine


def test_sqlite_metadata(sqlite_engine):
    with sqlite_engine.connect() as conn:
        conn.execute(textwrap.dedent("""
        create table test(id integer primary key);
        """))

        metadata = sa.MetaData()
        sa_tbl = sa.Table('test', metadata, autoload=True, autoload_with=sqlite_engine)
        print(sa_tbl)

        tbl = check.isinstance(alch.ToInternal()(sa_tbl), md.Table)
        print(tbl)
