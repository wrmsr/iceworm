import csv
import os.path
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from ..types import QualifiedName
from ..utils import mapping
from .connectors import Connection
from .connectors import Connector
from .connectors import RowGen
from .connectors import RowSink
from .connectors import RowSource
from .connectors import RowSpec
from .connectors import TableRowSpec


class FileConnector(Connector['FileConnector']):
    """
    local/s3/url/sftp?
    csv/json/yaml/parquet
    """

    class Config(dc.Frozen):
        base_path: str
        file_names_by_table_name: ta.Mapping[str, str] = dc.field(coerce=mapping)

    def __init__(self, name: str, config: Config) -> None:
        super().__init__(name)

        self._config = check.isinstance(config, FileConnector.Config)

    def connect(self) -> 'FileConnection':
        return FileConnection(self)


class FileConnection(Connection[FileConnector]):

    def __init__(self, connector: FileConnector) -> None:
        super().__init__(connector)

    def create_row_source(self, spec: RowSpec) -> RowSource:
        if isinstance(spec, TableRowSpec):
            file_name = self._connector._config.file_names_by_table_name[spec.table.parts[-1]]
            return CsvFileRowSource(os.path.join(self._connector._config.base_path, file_name))
        else:
            raise TypeError(spec)

    def create_row_sink(self, table: QualifiedName) -> RowSink:
        raise TypeError


class CsvFileRowSource(RowSource):

    def __init__(self, file_path: str) -> None:
        super().__init__()

        self._file_path = file_path

    def produce_rows(self) -> RowGen:
        with open(self._file_path, 'r') as f:
            reader = csv.reader(f)
            rows = iter(reader)
            cols = next(rows)
            for vals in rows:
                row = dict(zip(cols, vals))
                yield row
