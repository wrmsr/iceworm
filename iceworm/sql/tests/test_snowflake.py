import contextlib
import json

from omnibus import check
import sqlalchemy as sa

from .. import snowflake
from .. import tpch
from ... import sql
from ...tests import harness as har
from ...types import QualifiedName
from .helpers import DbManager


def test_conns(harness: har.Harness):
    with contextlib.ExitStack() as es:
        conn = es.enter_context(harness[DbManager].snowflake_engine.connect())

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


def test_tpch(harness: har.Harness):
    with contextlib.ExitStack() as es:
        engine = harness[DbManager].snowflake_engine
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


def test_exec_multi(harness: har.Harness):
    with contextlib.ExitStack() as es:
        engine = harness[DbManager].snowflake_engine
        conn = es.enter_context(engine.connect())
        schema = check.not_empty(snowflake.get_config()['schema'])

        query = f'call {schema}.exec_multi(array_construct(:a, :b))'
        params = {
            'a': 'select 1',
            'b': 'select 2',
        }
        stmt = sa.text(query).bindparams(*[sa.bindparam(k) for k in params])
        row = json.loads(check.single(check.single(conn.execute(stmt, params))))
        print(row)

        query = f'call {schema}.exec_multi(parse_json(:a))'
        params = {
            'a': json.dumps([
                'select 1',
                'select 2',
            ]),
        }
        stmt = sa.text(query).bindparams(*[sa.bindparam(k) for k in params])
        row = json.loads(check.single(check.single(conn.execute(stmt, params))))
        print(row)


def test_range():
    ada = snowflake.SnowflakeAdapter()
    stmt = ada.build_range(5)
    assert ada.render_query(stmt).split() == 'SELECT seq4() AS i FROM table(generator(rowcount => 5))'.split()
