import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
import sqlalchemy as sa

from .. import alchemy as alch
from .. import metadata as md
from ..types import QualifiedName
from .connectors import Connection
from .connectors import Connector
from .connectors import Row
from .connectors import RowGen
from .connectors import RowSink
from .connectors import RowSource
from .connectors import RowSpec
from .connectors import TableRowSpec


class SqlConnector(Connector['SqlConnector']):
    """
    postgres/mysql/snowflake
    """

    class Config(dc.Frozen):
        url: ta.Union[str, ta.Callable[[], str]]
        kwargs: ta.Mapping[str, ta.Any] = dc.field(ocol.frozendict(), coerce=ocol.frozendict)

    def __init__(self, name: str, config: Config) -> None:
        super().__init__(name)

        self._config = check.isinstance(config, SqlConnector.Config)

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

    def create_row_source(self, spec: RowSpec) -> RowSource:
        if isinstance(spec, TableRowSpec):
            return SqlRowSource(self.sa_conn, f'select * from {spec.name.dotted}')
        else:
            raise TypeError(spec)

    def create_row_sink(self, table: QualifiedName) -> RowSink:
        schema, name = table.pair
        md = sa.MetaData()
        md.reflect(bind=self.sa_conn, only=[name], schema=schema)
        tbl = md.tables[name]
        return SqlRowSink(self.sa_conn, tbl)

    def reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        if not names:
            raise TypeError

        ret = {}
        for name in names:
            schema, table = name.pair
            samd = sa.MetaData()
            samd.reflect(bind=self.sa_conn, only=[table], schema=schema)
            ret[name] = alch.ToInternal()(samd.tables[table])
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
        for row in rows:
            self._conn.execute(self._table.insert(), [row])