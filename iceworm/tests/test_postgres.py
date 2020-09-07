import contextlib
import textwrap
import time
import typing as ta
import urllib.parse

from omnibus import lang
from omnibus import threading as othr
import pytest
import sqlalchemy as sa

from .. import tpch
from .helpers import call_many_with_timeout
from .helpers import clean_pg
from .helpers import pg_url  # noqa


IS_NUMBER_JS = """
(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){is_number=require("is-number");module.exports.is_number=is_number},{"is-number":2}],2:[function(require,module,exports){"use strict";module.exports=function(num){if(typeof num==="number"){return num-num===0}if(typeof num==="string"&&num.trim()!==""){return Number.isFinite?Number.isFinite(+num):isFinite(+num)}return false}},{}]},{},[1]);
"""  # noqa


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

        conn.execute(textwrap.dedent(f"""
        create or replace function plv8_isnum(val json) returns json as $$
            if (typeof is_number == 'undefined') {{
            {IS_NUMBER_JS}
            }}
            return is_number(val);
        $$ language plv8 immutable strict;
        """))

        result = conn.scalar(textwrap.dedent("""
        select plv8_isnum('420');
        """))
        assert result is True

        result = conn.scalar(textwrap.dedent("""
        select plv8_isnum('"a420"');
        """))
        assert result is False

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

        conns: ta.List[sa.engine.Connection] = [
            es.enter_context(engine.connect().execution_options(autocommit=False, isolation_level='REPEATABLE READ'))
            for _ in range(3)
        ]
        conns[0].execute("create table blah0 (id integer primary key not null, data text)")
        conns[0].execute("create table blah1 (id integer primary key not null, data text)")
        conns[0].execute("insert into blah0 (id, data) values (0, 'hi')")
        conns[0].execute('commit')

        for _ in range(2):
            print(conns[0].scalar("select txid_current()"))

        for i, c in enumerate(conns):
            c.execute("abort")
            c.execute("begin")
            c.execute("set transaction isolation level repeatable read")
            c.execute("set local lock_timeout = '5s'")
            print('conn %d: %d' % (i, c.scalar("select txid_current()")))
            print(c.scalar("select current_setting('transaction_isolation')"))

        a = conns[0].scalar('select data from blah0 where id = 0')
        conns[1].execute("update blah0 set data = 'barf' where id = 0")
        b = conns[0].scalar('select data from blah0 where id = 0')
        conns[1].execute('commit')
        c = conns[0].scalar('select data from blah0 where id = 0')
        conns[0].execute('commit')
        conns[0].execute('begin')
        conns[1].execute('begin')
        print((a, b, c))

        for i, c in enumerate(conns):
            c.execute("abort")
            c.execute("begin")
            c.execute("set transaction isolation level repeatable read")
            c.execute("set local lock_timeout = '10s'")
            print('conn %d: %d' % (i, c.scalar("select txid_current()")))
            print(c.scalar("select current_setting('transaction_isolation')"))

        latch = othr.CountDownLatch(3, reset=True)

        def t0():
            conns[0].execute("select id from blah0 where id = 0 for share")
            print('t0 locked')
            time.sleep(3)
            latch.count_down()

            conns[0].execute("insert into blah1 (id, data) values (0, 'hi')")
            print('t0 inserted')
            time.sleep(3)
            latch.count_down()

            conns[0].execute('commit')
            print('t0 done')

        def t1():
            conns[1].execute("select id from blah0 where id = 0 for share")
            print('t1 locked')
            time.sleep(3)
            latch.count_down()

            conns[1].execute("insert into blah1 (id, data) values (1, 'hi')")
            print('t0 inserted')
            time.sleep(3)
            latch.count_down()

            conns[1].execute('commit')
            print('t1 done')

        def t2():
            latch.count_down()

            conns[2].execute("select id from blah0 where id = 0 for update")
            print('t2 got lock')

            conns[2].execute('commit')
            print('t1 done')

        call_many_with_timeout([t0, t1, t2])

        for c in conns:
            c.execute("select 1")


@pytest.mark.xfail()
def test_tpch(pg_url):  # noqa
    engine: sa.engine.Engine
    with contextlib.ExitStack() as es:
        engine = es.enter_context(lang.disposing(sa.create_engine(pg_url)))
        clean_pg(engine)

        metadata = sa.MetaData()
        sats = tpch.build_sa_tables(metadata=metadata)
        for sat in sats:
            sat.create(bind=engine)

        conn = es.enter_context(engine.connect())
        tpch.populate_sa_tables(conn, metadata)


@pytest.mark.xfail()
def test_pg8000(pg_url):  # noqa
    pg_url = urllib.parse.urlunparse(urllib.parse.urlparse(pg_url)._replace(scheme='postgresql+pg8000'))

    engine: sa.engine.Engine
    with contextlib.ExitStack() as es:
        engine = es.enter_context(lang.disposing(sa.create_engine(pg_url)))
        conn = es.enter_context(engine.connect())

        stmt = sa.select([sa.literal('abcd')])
        print(conn.scalar(stmt))

        print(stmt.compile(compile_kwargs={"literal_binds": True}))
