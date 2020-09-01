import contextlib
import textwrap
import time
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import threading as othr
from omnibus import tpch
import pytest
import sqlalchemy as sa

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

        sats = {
            tpch.ents.Column.Type.INTEGER: sa.Integer(),
            tpch.ents.Column.Type.IDENTIFIER: sa.Integer(),
            tpch.ents.Column.Type.DATE: sa.Date(),
            tpch.ents.Column.Type.DOUBLE: sa.Float(),
            tpch.ents.Column.Type.VARCHAR: sa.String(),
        }

        samd = sa.MetaData()

        for ent in [
            tpch.ents.Customer,
            tpch.ents.LineItem,
            tpch.ents.Nation,
            tpch.ents.Order,
            tpch.ents.Part,
            tpch.ents.PartSupplier,
            tpch.ents.Region,
            tpch.ents.Supplier,
        ]:
            sacs = []
            for f in dc.fields(ent):
                if tpch.ents.Column not in f.metadata:
                    continue
                tc = check.isinstance(f.metadata[tpch.ents.Column], tpch.ents.Column)
                sac = sa.Column(tc.name, sats[tc.type], primary_key=f.name in ent.__meta__.primary_key)
                sacs.append(sac)

            sat = sa.Table(ent.__name__.upper(), samd, *sacs)
            print(sat)

            sat.create(bind=engine)

            print()
