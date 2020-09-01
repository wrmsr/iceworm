import contextlib
import textwrap
import typing as ta

from omnibus import lang
import pytest
import sqlalchemy as sa

from ..utils import CountDownLatch
from .helpers import call_many_with_timeout
from .helpers import clean_pg
from .helpers import pg_url  # noqa


@pytest.mark.xfail()
def test_docker_postgres(pg_url):  # noqa
    engine: sa.engine.Engine
    with contextlib.ExitStack() as es:
        engine = es.enter_context(lang.disposing(sa.create_engine(pg_url)))
        clean_pg(engine)

        conn = es.enter_context(engine.connect())
        print(conn.scalar(sa.select([sa.func.version()])))

        conn.execute(textwrap.dedent("""
        create extension if not exists plv8;
        """))

        conn.execute(textwrap.dedent("""
        do $$ plv8.elog(NOTICE, "hello there!"); $$ language plv8;
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

        conn.execute(textwrap.dedent("""
        drop table if exists test;
        """))
        conn.execute(textwrap.dedent("""
        create table test(id integer primary key);
        """))

        metadata = sa.MetaData()
        tbl = sa.Table('test', metadata, autoload=True, autoload_with=engine)
        print(tbl)


@pytest.mark.xfail()
def test_postgres_locks(pg_url):  # noqa
    engine: sa.engine.Engine
    with contextlib.ExitStack() as es:
        engine = es.enter_context(lang.disposing(sa.create_engine(pg_url)))
        clean_pg(engine)

        print()

        conns: ta.List[sa.engine.Connection] = [es.enter_context(engine.connect()) for _ in range(3)]
        conns[0].execute("create table blah0 (id integer primary key not null, data text)")
        conns[0].execute("create table blah1 (id integer primary key not null, data text)")
        conns[0].execute("insert into blah0 (id, data) values (0, 'hi')")

        for _ in range(2):
            print(conns[0].scalar("select txid_current()"))

        for c in conns:
            c.execute("set transaction isolation level repeatable read")
            c.execute("begin")

        latch = CountDownLatch(3, reset=True)

        def t0():
            conns[0].execute("select id from blah0 where id = 0 for share")
            latch.count_down()

            conns[0].execute("insert into blah1 (id, data) values (0, 'hi')")

            print('t0 done')

        def t1():
            conns[1].execute("select id from blah0 where id = 0 for share")
            latch.count_down()

            conns[1].execute("insert into blah1 (id, data) values (1, 'hi')")

            print('t1 done')

        def t2():
            latch.count_down()

            conns[2].execute("select id from blah0 where id = 0 for update")
            print('t2 got lock')

        call_many_with_timeout([t0, t1, t2])

        for c in conns:
            c.execute("select 1")
