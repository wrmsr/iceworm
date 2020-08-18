"""
TODO:
 - deal w csv header
 - NamePolicy - <schema>.<table>(.csv)?
 - local/s3/url/sftp?
 - csv/json/yaml/parquet
"""
import csv
import glob
import os.path
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import properties

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


class SchemaPolicy(dc.Enum):
    pass


class YamlHeaderSchemaPolicy(SchemaPolicy):
    pass


class ProvidedSchemaPolicy(SchemaPolicy):
    columns: ta.Sequence[md.Column] = dc.field(coerce=seq)


class Mount(dc.Pure):
    path: str = dc.field(check=lambda o: isinstance(o, str))
    schema: SchemaPolicy = dc.field(check=lambda o: isinstance(o, SchemaPolicy))
    globs: ta.Sequence[str] = dc.field(coerce=seq)


class Table(dc.Pure):
    md_table: md.Table
    path: str


class FileConnector(Connector['FileConnector']):

    class Config(dc.Frozen):
        mounts: ta.Sequence[Mount] = dc.field(coerce=seq, check=lambda l: all(isinstance(e, Mount) for e in l))

    def __init__(self, name: str, config: Config) -> None:
        super().__init__(name)

        self._config = check.isinstance(config, FileConnector.Config)

    @properties.cached
    def tables_by_name(self) -> ta.Mapping[str, Table]:
        tables_by_name = {}

        for mnt in self._config.mounts:
            for glb in mnt.globs:
                for fp in glob.iglob(os.path.join(mnt.path, glb)):
                    if isinstance(mnt.schema, ProvidedSchemaPolicy):
                        cols = mnt.schema.columns
                    else:
                        raise TypeError(mnt.schema)

                    name = os.path.basename(fp).rpartition('.')[0]
                    table = Table(
                        md.Table(name, cols),
                        fp,
                    )

                    check.not_in(name, tables_by_name)
                    tables_by_name[name] = table

        return tables_by_name

    def connect(self) -> 'FileConnection':
        return FileConnection(self)


class FileConnection(Connection[FileConnector]):

    def __init__(self, connector: FileConnector) -> None:
        super().__init__(connector)

    def create_row_source(self, spec: RowSpec) -> RowSource:
        if isinstance(spec, TableRowSpec):
            table = self._connector.tables_by_name[spec.table[-1]]
            return CsvFileRowSource(table)
        else:
            raise TypeError(spec)

    def create_row_sink(self, table: QualifiedName) -> RowSink:
        raise TypeError

    def reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        if names:
            ret = {}
            for name in names:
                if len(name) == 1:
                    try:
                        ret[QualifiedName.of([name[0]])] = self._connector.tables_by_name[name[0]]
                    except KeyError:
                        pass
            return ret

        else:
            return {QualifiedName.of([n]): t for n, t in self._connector.tables_by_name.items()}


class CsvFileRowSource(RowSource):

    def __init__(self, table: Table) -> None:
        super().__init__()

        self._table = table

    def produce_rows(self) -> RowGen:
        with open(self._table.path, 'r') as f:
            reader = csv.reader(f)
            rows = iter(reader)
            cols = next(rows)
            for vals in rows:
                row = dict(zip(cols, vals))
                yield row
