import abc
import logging
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang

from ... import elements as els
from .... import datatypes as dt
from .... import metadata as md
from ....types import QualifiedName
from ....utils import unique_dict
from ...utils import parse_simple_select_table
from ..base import Connection as _Connection
from ..base import Connector as _Connector
from ..base import Row
from ..base import RowSink
from ..base import RowSource
from ..base import Rows


log = logging.getLogger(__name__)


class Table(lang.Abstract):

    @abc.abstractproperty
    def md_table(self) -> md.Table:
        raise NotImplementedError


class SystemConnector(_Connector['SystemConnector', 'SystemConnector.Config']):

    class Config(_Connector.Config):
        id: els.Id = dc.field('system', check=els.id_check)

    def __init__(self, config: Config = Config()) -> None:
        super().__init__(check.isinstance(config, SystemConnector.Config))

        self._tables_by_name = unique_dict((t.md_table.name, t) for t in [
            NotificationsTable(),
        ])

    def connect(self) -> 'SystemConnection':
        return SystemConnection(self)


class SystemConnection(_Connection[SystemConnector]):

    def __init__(self, connector: SystemConnector) -> None:
        super().__init__(connector)

    def create_row_source(self, query: str) -> RowSource:
        table_name = parse_simple_select_table(query, star=True)
        table = self._ctor._tables_by_name[table_name]
        if not isinstance(table, RowSource):
            raise TypeError(table)
        return table

    def create_row_sink(self, table_name: QualifiedName) -> RowSink:
        table = self._ctor._tables_by_name[table_name]
        if not isinstance(table, RowSink):
            raise TypeError(table)
        return table

    def _reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        if names:
            return {n: self._ctor._tables_by_name[n].md_table for n in names if n in self._ctor._tables_by_name}
        else:
            return {t.md_table.name: t.md_table for t in self._ctor._tables_by_name.values()}


class NotificationsTable(Table, RowSource, RowSink):

    TABLE = md.Table(
        ['notifications'],
        [
            md.Column('message', dt.String()),
        ],
    )

    @property
    def md_table(self) -> md.Table:
        return self.TABLE

    def produce_rows(self) -> Rows:
        raise NotImplementedError

    def consume_rows(self, rows: ta.Iterable[Row]) -> None:
        for row in rows:
            check.arg(set(row) == {'message'})
            log.info(row['message'])
