import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from ..collections import seq


class Value(dc.Enum):

    @classmethod
    def of(cls, obj: ta.Union['Value', str, ta.Sequence]) -> 'Value':
        if isinstance(obj, Value):
            return obj
        elif isinstance(obj, str):
            return Text(obj)
        elif isinstance(obj, ta.Sequence):
            return Table.of(obj)
        else:
            raise TypeError(obj)


class Text(Value):
    text: str

    @classmethod
    def of(cls, obj: ta.Union['Text', str]) -> 'Text':
        if isinstance(obj, Text):
            return obj
        elif isinstance(obj, str):
            return Text(obj)
        else:
            raise TypeError(obj)


class Cell(dc.Pure):
    value: Value

    @classmethod
    def of(cls, obj: ta.Union['Cell', ta.Any]) -> 'Cell':
        if isinstance(obj, Cell):
            return obj
        else:
            return Cell(Value.of(obj))


class Row(dc.Pure):
    cells: ta.Sequence[Cell] = dc.field(coerce=seq)

    @classmethod
    def of(cls, obj: ta.Union['Row', ta.Sequence[ta.Any]]) -> 'Row':
        if isinstance(obj, Row):
            return obj
        elif isinstance(obj, str):
            raise TypeError(obj)
        elif isinstance(obj, ta.Sequence):
            return Row([Cell.of(e) for e in obj])
        else:
            raise TypeError(obj)


class Table(Value):
    rows: ta.Sequence[Row] = dc.field(coerce=seq)

    @classmethod
    def of(cls, obj: ta.Union['Table', ta.Sequence[ta.Any]]) -> 'Table':
        if isinstance(obj, Table):
            return obj
        elif isinstance(obj, str):
            raise TypeError(obj)
        elif isinstance(obj, ta.Sequence):
            return Table([Row.of(e) for e in obj])
        else:
            raise TypeError(obj)


def test_dot():
    print(Value.of('hi'))
    print(Value.of([['a', 'b'], ['c', 'd']]))
