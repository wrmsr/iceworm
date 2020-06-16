import typing as ta

from omnibus import dataclasses as dc
from omnibus import lang


class Node(dc.Enum):
    pass


class Expr(Node, abstract=True):
    pass


class BinaryOp(lang.AutoEnum):
    AND = ...
    OR = ...


class BinaryExpr(Expr):
    left: Expr
    op: BinaryOp
    right: Expr


class UnaryOp(lang.AutoEnum):
    NOT = ...


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


class Join(Relation):
    left: Relation
    right: Relation


class Table(Relation):
    name: Identifier


class Select(Node):
    items: ta.Sequence[SelectItem]
    relations: ta.Sequence[Relation]
