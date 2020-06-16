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


class FunctionCall(Expr):
    name: Identifier
    args: ta.Sequence[Expr]


class SelectItem(Node):
    expr: Expr


class Relation(Node, abstract=True):
    pass


class Table(Relation):
    name: Identifier


class Select(Node):
    items: ta.Sequence[SelectItem]
    relations: ta.Sequence[Relation]
