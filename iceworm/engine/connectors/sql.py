import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
import sqlalchemy as sa

from ... import alchemy as alch
from ... import metadata as md
from ...types import QualifiedName
from ...utils import secrets
from ..utils import parse_simple_select_table
from .connectors import Connection
from .connectors import Connector
from .connectors import Row
from .connectors import RowGen
from .connectors import RowSink
from .connectors import RowSource


class SqlConnector(Connector['SqlConnector', 'SqlConnector.Config']):
    """
    postgres/mysql/snowflake
    """

    class Config(Connector.Config):
        url: ta.Optional[str] = dc.field(None, check=lambda s: s is None or (isinstance(s, str) and s))
        url_secret: ta.Optional[secrets.SecretKey] = dc.field(None, coerce=secrets.SecretKey.of_optional)

        dc.check(lambda url, url_secret: check.one_of([url, url_secret], not_none=True))

        kwargs: ta.Mapping[str, ta.Any] = dc.field(ocol.frozendict(), coerce=ocol.frozendict)

    def __init__(self, config: Config) -> None:
        super().__init__(check.isinstance(config, SqlConnector.Config))

        self._engine: ta.Optional[sa.engine.Engine] = None

    def connect(self, **kwargs) -> 'SqlConnection':
        return SqlConnection(self, self.engine.connect(**kwargs))

    @property
    def engine(self) -> sa.engine.Engine:
        if self._engine is None:
            url = self._config.url
            if callable(url):
                url = url()
            self._engine = sa.create_engine(url)
        return self._engine

    def close(self) -> None:
        if self._engine is not None:
            self._engine.dispose()


class SqlConnection(Connection[SqlConnector]):

    def __init__(self, connector: SqlConnector, conn: sa.engine.Connection) -> None:
        super().__init__(connector)

        self._conn = check.isinstance(conn, sa.engine.Connection)

    @property
    def sa_conn(self) -> sa.engine.Connection:
        return self._conn

    def close(self) -> None:
        self._conn.close()

    def create_row_source(self, query: str) -> RowSource:
        table_name = parse_simple_select_table(query, star=True)
        return SqlRowSource(self.sa_conn, f'select * from {table_name.dotted}')

    def create_row_sink(self, table: QualifiedName) -> RowSink:
        schema, name = table.pair
        md = sa.MetaData()
        md.reflect(bind=self.sa_conn, only=[name], schema=schema)
        tbl = md.tables[name]
        return SqlRowSink(self.sa_conn, tbl)

    def _reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        if not names:
            raise TypeError

        samd = sa.MetaData()
        available_by_schema = {}

        ret = {}
        for name in names:
            schema, table = name.pair

            try:
                available = available_by_schema[schema]
            except KeyError:
                available = available_by_schema[schema] = \
                    set(self.sa_conn.engine.table_names(schema, connection=self.sa_conn))

            if table not in available:
                continue

            reflect_opts = {
                'schema': schema,
                'autoload': True,
                'autoload_with': self.sa_conn,
                'extend_existing': False,
                'autoload_replace': True,
                'resolve_fks': True,
                '_extend_on': set(),
            }

            satbl = sa.Table(table, samd, **reflect_opts)
            ret[name] = alch.ToInternal()(satbl)

        return ret


class SqlRowSource(RowSource):

    def __init__(self, conn: sa.engine.Connection, query: str) -> None:
        super().__init__()

        self._conn = check.isinstance(conn, sa.engine.Connection)
        self._query = query

    def produce_rows(self) -> RowGen:
        rows = self._conn.execute(self._query)
        for row in rows:
            yield row


class SqlRowSink(RowSink):

    def __init__(self, conn: sa.engine.Connection, table: sa.Table) -> None:
        super().__init__()

        self._conn = check.isinstance(conn, sa.engine.Connection)
        self._table = check.isinstance(table, sa.Table)

    def consume_rows(self, rows: ta.Iterable[Row]) -> None:
        ks = [c.name for c in self._table.columns]
        for row in rows:
            check.state(len(row) == len(ks))
            # row = dict(zip(ks, row.values()))  # FIXME
            try:
                dct = {k: row[k] for k in ks}
            except KeyError:
                raise
            self._conn.execute(self._table.insert(), [dct])
