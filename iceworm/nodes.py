import enum
import typing as ta

from omnibus import dataclasses as dc


class Node(dc.Enum, sealed=True):
    pass


class Expr(Node, abstract=True):
    pass


class BinaryOp(enum.Enum):
    AND = 'and'
    OR = 'or'

    EQ = '='
    NE = '!='
    NEX = '<>'
    LT = '<'
    LTE = '<='
    GT = '>'
    GTE = '>='

    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'


BINARY_OP_MAP: ta.Mapping[str, BinaryOp] = {v.value: v for v in BinaryOp.__members__.values()}


LOGIC_OPS: ta.AbstractSet[BinaryOp] = frozenset([
    BinaryOp.AND,
    BinaryOp.OR,
])


CMP_OPS: ta.AbstractSet[BinaryOp] = frozenset([
    BinaryOp.EQ,
    BinaryOp.NE,
    BinaryOp.NEX,
    BinaryOp.LT,
    BinaryOp.LTE,
    BinaryOp.GT,
    BinaryOp.GTE,
])


ARITH_OPS: ta.AbstractSet[BinaryOp] = frozenset([
    BinaryOp.ADD,
    BinaryOp.SUB,
    BinaryOp.MUL,
    BinaryOp.DIV,
    BinaryOp.MOD,
])


class BinaryExpr(Expr):
    left: Expr
    op: BinaryOp
    right: Expr


class UnaryOp(enum.Enum):
    NOT = 'not'

    PLUS = '+'
    MINUS = '-'


UNARY_OP_MAP: ta.Mapping[str, UnaryOp] = {v.value: v for v in UnaryOp.__members__.values()}


class UnaryExpr(Expr):
    op: UnaryOp
    value: Expr


class Identifier(Expr):
    name: str


class Integer(Expr):
    value: int


class String(Expr):
    value: str


class FunctionCall(Expr):
    name: Identifier
    args: ta.Sequence[Expr]


class Null(Expr):
    pass


class Relation(Node, abstract=True):
    pass


class Join(Relation):
    left: Relation
    right: Relation
    condition: ta.Optional[Expr] = None


class Table(Relation):
    name: Identifier


class GroupBy(Node):
    exprs: ta.Sequence[Expr]


class SelectItem(Node, abstract=True):
    pass


class AllSelectItem(SelectItem):
    pass


class ExprSelectItem(Node):
    expr: Expr
    label: ta.Optional[Identifier] = None


class Select(Node):
    items: ta.Sequence[SelectItem]
    relations: ta.Sequence[Relation]
    where: ta.Optional[Expr] = None
    group_by: ta.Optional[GroupBy] = None
