import typing as ta

import pytest
import sqlalchemy as sa
import sqlalchemy.dialects  # noqa
import sqlalchemy.pool  # noqa

from omnibus import check
from omnibus import lang


class CustomEscape:

    def __init__(self, escape: ta.Union[ta.Callable[[], str], str]) -> None:
        super().__init__()
        check.arg(callable(escape) or isinstance(escape, str))
        self.escape = escape

    def __call__(self):
        if callable(self.escape):
            return self.escape()
        elif isinstance(self.escape, str):
            return self.escape
        else:
            raise TypeError(repr(self.escape))


@lang.cached_nullary
def _dummy_pg8000_connection():
    import pg8000

    class DummyPg8000Connection(pg8000.Connection):

        def connect(self, sock=None):
            self.charset = 'utf8mb4'

            # See pg8000.constants.CLIENT for details unpacking
            self.server_capabilities = 0x807ff7ff

            self.server_charset = 'latin1'
            self.server_language = 8
            self.server_status = 0

        def execute(self, query, args=None):
            raise NotImplementedError

        def executemany(self, query, args):
            raise NotImplementedError

        def escape(self, obj, mapping=None):
            if isinstance(obj, CustomEscape):
                return obj()
            else:
                return super().escape(obj, mapping=mapping)

    return DummyPg8000Connection


@lang.cached_nullary
def _PGDialect_dummypg8000():
    import sqlalchemy.dialects.postgresql.pg8000  # noqa

    class __PGDialect_dummypg8000(sa.dialects.postgresql.pg8000.PGDialect_pg8000):
        driver = 'dummypg8000'

        def connect(self, *cargs, **cparams):
            return _dummy_pg8000_connection()(*cargs, **cparams)

        def initialize(self, connection):
            pass

        def do_execute(self, cursor, statement, parameters, context=None):
            raise NotImplementedError

        def do_rollback(self, dbapi_connection):
            pass

    globals()['__PGDialect_dummypg8000'] = __PGDialect_dummypg8000
    sa.dialects.registry.register(
        'dummypg8000',
        __PGDialect_dummypg8000.__module__,
        __PGDialect_dummypg8000.__name__,
    )

    return __PGDialect_dummypg8000


def _create_pg8000_dummy_engine() -> sa.engine.Engine:
    _PGDialect_dummypg8000()

    def creator(*cargs, **cparams):
        return _dummy_pg8000_connection()('dummy')

    dialect = sa.dialects.registry.load('dummypg8000')(dbapi=__import__('pg8000'))
    engine = sa.engine.base.Engine(sa.pool.NullPool(creator, dialect=dialect), dialect, 'dummy')
    dialect.engine_created(engine)
    return engine


def pg8000_render_statement(elem, *multiparams, **params) -> str:
    engine = _create_pg8000_dummy_engine()
    dialect = engine.dialect

    distilled_params = sa.cutils._distill_params(multiparams, params)
    if distilled_params:
        # note this is usually dict but we support RowProxy
        # as well; but dict.keys() as an iterable is OK
        keys = distilled_params[0].keys()
    else:
        keys = []

    with engine.connect() as connection:
        compiled = elem.compile(
            dialect=dialect,
            column_keys=keys,
            inline=len(distilled_params) > 1,
            schema_translate_map=engine.schema_for_object
            if not engine.schema_for_object.is_default else None
        )

        context = dialect.execution_ctx_cls._init_compiled(
            dialect,
            connection,
            connection.connection,
            compiled,
            distilled_params
        )

        cursor = context.cursor
        statement = context.statement
        parameters = context.parameters

        if not context.executemany:
            parameters = parameters[0]

        statement = cursor.mogrify(statement, parameters)

        return statement


@pytest.mark.xfail()
def test_render():
    assert pg8000_render_statement(sa.select([1])) == 'SELECT 1'
