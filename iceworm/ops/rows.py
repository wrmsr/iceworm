import abc
import csv
import typing as ta

from omnibus import lang
import sqlalchemy as sa


Row = ta.Mapping[str, ta.Any]
RowGen = ta.Generator[Row, None, None]


class RowSource(lang.Abstract):

    @abc.abstractmethod
    def yield_rows(self) -> RowGen:
        raise NotImplementedError


class SqlRowSource(RowSource):

    def __init__(self, conn: sa.engine.Connection, query: str) -> None:
        super().__init__()

        self._conn = conn
        self._query = query

    def yield_rows(self) -> RowGen:
        rows = self._conn.execute(self._query)
        for row in rows:
            yield row


class CsvFileRowSource(RowSource):

    def __init__(self, file_path: str) -> None:
        super().__init__()

        self._file_path = file_path

    def yield_rows(self) -> RowGen:
        with open(self._file_path, 'r') as f:
            reader = csv.reader(f)
            rows = iter(reader)
            cols = next(rows)
            for vals in rows:
                row = dict(zip(cols, vals))
                yield row
