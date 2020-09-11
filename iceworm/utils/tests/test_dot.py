"""
https://graphviz.org/doc/info/lang.html
"""
import html
import io
import subprocess
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import dispatch as disp
from omnibus import os as oos

from ..collections import seq


class Item(dc.Enum):
    pass


class Value(Item, abstract=True):

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


class Raw(Value):
    raw: str

    @classmethod
    def of(cls, obj: ta.Union['Raw', str]) -> 'Raw':
        if isinstance(obj, Raw):
            return obj
        elif isinstance(obj, str):
            return Raw(obj)
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


class Cell(Item):
    value: Value

    @classmethod
    def of(cls, obj: ta.Union['Cell', ta.Any]) -> 'Cell':
        if isinstance(obj, Cell):
            return obj
        else:
            return Cell(Value.of(obj))


class Row(Item):
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


class Id(Item):
    id: str

    @classmethod
    def of(cls, obj: ta.Union['Id', str]) -> 'Id':
        if isinstance(obj, Id):
            return obj
        elif isinstance(obj, str):
            return Id(obj)
        else:
            raise TypeError(obj)


class Attrs(Item):
    attrs: ta.Mapping[str, Value] = dc.field(
        coerce=lambda o: ocol.frozendict(
            (check.not_empty(check.isinstance(k, str)), Value.of(v))
            for k, v in check.isinstance(o, ta.Mapping).items()
        )
    )

    @classmethod
    def of(cls, obj: ta.Union['Attrs', ta.Mapping[str, ta.Any]]) -> 'Attrs':
        if isinstance(obj, Attrs):
            return obj
        elif isinstance(obj, ta.Mapping):
            return Attrs(obj)
        else:
            raise TypeError(obj)


class Edge(Item):
    left: Id = dc.field(coerce=Id.of)
    right: Id = dc.field(coerce=Id.of)
    attrs: Attrs = dc.field(Attrs({}), coerce=Attrs.of)


class Node(Item):
    id: Id = dc.field(coerce=Id.of)
    attrs: Attrs = dc.field(Attrs({}), coerce=Attrs.of)


class Graph(Item):
    nodes: ta.Sequence[Node] = dc.field(coerce=seq)
    edges: ta.Sequence[Edge] = dc.field(coerce=seq)

    id: Id = dc.field(Id('G'), kwonly=True)


class Renderer(disp.Class):

    def __init__(self, out: ta.TextIO) -> None:
        super().__init__()

        self._out = out

    __call__ = disp.property()

    def __call__(self, item: Item) -> None:  # noqa
        raise TypeError(item)

    def __call__(self, item: Raw) -> None:  # noqa
        self._out.write(item.raw)

    def __call__(self, item: Text) -> None:  # noqa
        self._out.write(html.escape(item.text))

    def __call__(self, item: Cell) -> None:  # noqa
        self._out.write('<td>')
        self(item.value)
        self._out.write('</td>')

    def __call__(self, item: Row) -> None:  # noqa
        self._out.write('<tr>')
        for cell in item.cells:
            self(cell)
        self._out.write('</tr>')

    def __call__(self, item: Table) -> None:  # noqa
        self._out.write('<table>')
        for row in item.rows:
            self(row)
        self._out.write('</table>')

    def __call__(self, item: Id) -> None:  # noqa
        self._out.write(f'"{item.id}"')

    def __call__(self, item: Attrs) -> None:  # noqa
        if item.attrs:
            self._out.write('[')
            for i, (k, v) in enumerate(item.attrs.items()):
                if i:
                    self._out.write(', ')
                self._out.write(k)
                self._out.write('=<')
                self(v)
                self._out.write('>')
            self._out.write(']')

    def __call__(self, item: Edge) -> None:  # noqa
        self(item.left)
        self._out.write(' -> ')
        self(item.right)
        if item.attrs.attrs:
            self._out.write(' ')
            self(item.attrs)
        self._out.write(';\n')

    def __call__(self, item: Node) -> None:  # noqa
        self(item.id)
        if item.attrs.attrs:
            self._out.write(' ')
            self(item.attrs)
        self._out.write(';\n')

    def __call__(self, item: Graph) -> None:  # noqa
        self._out.write('digraph ')
        self(item.id)
        self._out.write(' {\n')
        for node in item.nodes:
            self(node)
        for edge in item.edges:
            self(edge)
        self._out.write('}\n')


def render(item: Item) -> str:
    out = io.StringIO()
    Renderer(out)(item)
    return out.getvalue()


def open_dot(gv: str, *, timeout: float = 30 * 60.) -> None:
    stdout, _ = subprocess.Popen(
        ['dot', '-Tpdf'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    ).communicate(
        input=gv.encode('utf-8'),
        timeout=timeout,
    )

    with oos.tmp_file() as pdf:
        pdf.file.write(stdout)
        pdf.file.flush()

        _, _ = subprocess.Popen(
            ['open', pdf.name],
        ).communicate(
            timeout=timeout,
        )


def test_dot():
    print(render(Value.of('hi')))
    print(render(Value.of([['a', 'b'], ['c', 'd']])))

    def print_and_open(no):
        print(no)
        gv = render(no)
        print(gv)
        open_dot(gv)

    print_and_open(Graph(
        [
            Node('a', {'shape': 'box'}),
            Node('b', {'label': [['a', 'b'], ['c', 'd']]}),
        ],
        [
            Edge('a', 'b'),
        ],
    ))
