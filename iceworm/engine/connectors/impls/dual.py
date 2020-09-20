import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from ... import elements as els
from .... import metadata as md
from ....types import QualifiedName
from ...utils import parse_simple_select_table
from ..base import Connection as _Connection
from ..base import Connector as _Connector
from ..base import RowSink
from ..base import RowSource
from ..base import Rows


TABLE = md.Table(
    ['dual'],
    [
        md.Column('dummy', md.STRING),
    ]
)


class DualConnector(_Connector['DualConnector', 'DualConnector.Config']):

    class Config(_Connector.Config):
        id: els.Id = dc.field('dual', check=lambda s: isinstance(s, els.Id) and s)

    def __init__(self, config: Config) -> None:
        super().__init__(check.isinstance(config, DualConnector.Config))

    def connect(self) -> 'DualConnection':
        return DualConnection(self)


class DualConnection(_Connection[DualConnector]):

    def __init__(self, connector: DualConnector) -> None:
        super().__init__(connector)

    def create_row_source(self, query: str) -> RowSource:
        table_name = parse_simple_select_table(query, star=True)
        if table_name != TABLE.name:
            raise NameError(table_name)
        return DualRowSource()

    def create_row_sink(self, table: QualifiedName) -> RowSink:
        raise TypeError

    def _reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        if TABLE.name in names:
            return {TABLE.name: TABLE}
        else:
            return {}


class DualRowSource(RowSource):

    def produce_rows(self) -> Rows:
        return [{'dummy': 'x'}]
