"""
TODO:
 - deal w csv header
  - oo, schema def in header lol: ```id integer, name varchar, ...```
 - NamePolicy - <schema>.<table>(.csv)?
 - local/pkg/s3/url/sftp?
 - csv/json/yaml/parquet
"""
import csv
import glob
import os.path
import typing as ta

from omnibus import check
from omnibus import collections as col
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import properties

from ... import elements as els
from ... import sites
from .... import metadata as md
from ....types import QualifiedName
from ...utils import parse_simple_select_table
from ..base import Connection as _Connection
from ..base import Connector as _Connector
from ..base import Rows
from ..base import RowSink
from ..base import RowSource


class SchemaPolicy(dc.Enum):
    pass


class SchemaPolicies(lang.Namespace):

    class YamlHeader(SchemaPolicy):
        pass

    class Provided(SchemaPolicy):
        columns: ta.Sequence[md.Column] = dc.field(coerce=col.seq)


class Mount(dc.Pure):
    path: str = dc.field(check_type=str)
    schema: SchemaPolicy = dc.field(check_type=SchemaPolicy)
    globs: ta.Sequence[str] = dc.field(coerce=col.seq)


class Table(dc.Pure):
    md_table: md.Table
    path: str


class FileConnector(_Connector['FileConnector', 'FileConnector.Config']):

    class Config(_Connector.Config):
        mounts: ta.Sequence[Mount] = dc.field(coerce=col.seq, check=lambda l: all(isinstance(e, Mount) for e in l))

    def __init__(self, config: Config) -> None:
        super().__init__(check.isinstance(config, FileConnector.Config))

    @properties.cached
    @property
    def tables_by_name(self) -> ta.Mapping[QualifiedName, Table]:
        tables_by_name = {}

        for mnt in self._config.mounts:
            for glb in mnt.globs:
                for fp in glob.iglob(os.path.join(mnt.path, glb)):
                    if isinstance(mnt.schema, SchemaPolicies.Provided):
                        cols = mnt.schema.columns
                    else:
                        raise TypeError(mnt.schema)

                    name = QualifiedName(os.path.basename(fp).split('.')[:-1])
                    table = Table(
                        md.Table(name, cols),
                        fp,
                    )

                    check.not_in(name, tables_by_name)
                    tables_by_name[name] = table

        return tables_by_name

    def connect(self) -> 'FileConnection':
        return FileConnection(self)


class FileConnection(_Connection[FileConnector]):

    def __init__(self, connector: FileConnector) -> None:
        super().__init__(connector)

    def create_row_source(self, query: str) -> RowSource:
        table_name = parse_simple_select_table(query, star=True)
        table = self._ctor.tables_by_name[table_name]
        return CsvFileRowSource(table)

    def create_row_sink(self, table: QualifiedName) -> RowSink:
        raise TypeError

    def _reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        if names:
            ret = {}
            for name in names:
                try:
                    ret[name] = self._ctor.tables_by_name[name].md_table
                except KeyError:
                    pass
            return ret

        else:
            return {n: t.md_table for n, t in self._ctor.tables_by_name.items()}


class CsvFileRowSource(RowSource):

    def __init__(self, table: Table) -> None:
        super().__init__()

        self._table = table

    def produce_rows(self) -> Rows:
        with open(self._table.path, 'r') as f:
            reader = csv.reader(f)
            rows = iter(reader)
            header_cols = next(rows)  # noqa
            cols = [c.name for c in self._table.md_table.columns]
            for vals in rows:
                row = dict(zip(cols, vals))
                yield row


class MountPathProcessor(els.InstanceElementProcessor):

    class Instance(els.InstanceElementProcessor.Instance['MountPathProcessor']):

        @properties.cached
        def matches(self) -> ta.Iterable[els.Element]:
            return [
                e
                for e in self.input
                if isinstance(e, FileConnector.Config)
                and any(not os.path.isabs(m.path) for m in e.mounts)
            ]

        def make_abs(self, cfg: FileConnector.Config) -> FileConnector.Config:
            sos = [sb for sb in els.iter_origins(cfg) if isinstance(sb, sites.Site) and sites.SiteLoaded in sb.anns]
            if sos:
                base_path = os.path.dirname(sos[0].anns[sites.SiteLoaded].abs_path)
            else:
                base_path = os.getcwd()

            return dc.replace(
                cfg,
                mounts=[
                    dc.replace(
                        m,
                        path=os.path.abspath(os.path.join(base_path, m.path)),
                    )
                    for m in cfg.mounts
                ],
                meta={els.Origin: els.Origin(cfg)},
            )

        @properties.cached
        def output(self) -> ta.Iterable[els.Element]:
            return [self.make_abs(c) if c in self.matches else c for c in self.input]
