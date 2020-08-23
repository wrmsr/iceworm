import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from .. import metadata as md
from ..types import QualifiedName
from ..utils import seq
from .connectors import Connection
from .connectors import Connector
from .connectors import RowGen
from .connectors import RowSink
from .connectors import RowSource
from .connectors import RowSpec
from .connectors import TableRowSpec


class Table(dc.Pure):
    md_table: md.Table
    fn: ta.Callable[[], RowGen]


class ComputedConnector(Connector['ComputedConnector']):

    class Config(dc.Frozen):
        tables: ta.Sequence[Table] = dc.field(coerce=seq)

    def __init__(self, name: str, config: Config) -> None:
        super().__init__(name)

        self._config = check.isinstance(config, ComputedConnector.Config)

        self._tables_by_name: ta.Mapping[QualifiedName, Table] = {t.md_table.name: t for t in self._config.tables}

    def connect(self) -> 'ComputedConnection':
        return ComputedConnection(self)


class ComputedConnection(Connection[ComputedConnector]):

    def __init__(self, connector: ComputedConnector) -> None:
        super().__init__(connector)

    def create_row_source(self, spec: RowSpec) -> RowSource:
        if isinstance(spec, TableRowSpec):
            table = self._ctor._tables_by_name[spec.name]
            return ComputedRowSource(table)
        else:
            raise TypeError(spec)

    def create_row_sink(self, table: QualifiedName) -> RowSink:
        raise TypeError

    def reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        if names:
            ret = {}
            for name in names:
                try:
                    ret[name] = self._ctor._tables_by_name[name].md_table
                except KeyError:
                    pass
            return ret

        else:
            return {n: t.md_table for n, t in self._ctor._tables_by_name.items()}


class ComputedRowSource(RowSource):

    def __init__(self, table: Table) -> None:
        super().__init__()

        self._table = table

    def produce_rows(self) -> RowGen:
        return self._table.fn()
