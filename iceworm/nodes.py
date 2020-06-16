import typing as ta

from omnibus import dataclasses as dc
from omnibus import lang


class Node(dc.Enum):
    pass


class Expr(Node, abstract=True):
    pass


class BinaryOp(lang.ValueEnum):
    AND = 'and'
    OR = 'or'


class BinaryExpr(Expr):
    left: Expr
    op: BinaryOp
    right: Expr


class UnaryOp(lang.ValueEnum):
    NOT = 'not'


class UnaryExpr(Expr):
    op: UnaryOp
    value: Expr


class Identifier(Expr):
    name: str


class Integer(Expr):
    value: int


class FunctionCall(Expr):
    name: Identifier
    args: ta.Sequence[Expr]


class SelectItem(Node):
    expr: Expr
    label: ta.Optional[Identifier] = None


class Relation(Node, abstract=True):
    pass


class Table(Relation):
    name: Identifier


class Select(Node):
    items: ta.Sequence[SelectItem]
    relations: ta.Sequence[Relation]
