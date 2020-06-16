import typing as ta

from omnibus import dataclasses as dc


class Node(dc.Enum):
    pass


class Expr(Node, abstract=True):
    pass


class Identifier(Expr):
    name: str


class Integer(Expr):
    value: int


class SelectItem(Node):
    expr: Expr


class Table(Node):
    name: Identifier


class Select(Node):
    items: ta.Sequence[SelectItem]
    table: ta.Optional[Table]
