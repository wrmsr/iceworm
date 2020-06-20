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
    CONCAT = '||'


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
    BinaryOp.CONCAT,
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


class QualifiedName(Expr):
    parts: ta.Sequence[Identifier]


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


class JoinType(enum.Enum):
    DEFAULT = ''
    INNER = 'inner'
    LEFT = 'left'
    LEFT_OUTER = 'left outer'
    RIGHT = 'right'
    RIGHT_OUTER = 'right outer'
    FULL = 'full'
    FULL_OUTER = 'full outer'
    CROSS = 'cross'
    NATURAL = 'natural'


JOIN_TYPE_MAP: ta.Mapping[str, JoinType] = {v.value: v for v in JoinType.__members__.values()}


class Join(Relation):
    left: Relation
    type: JoinType
    right: Relation
    condition: ta.Optional[Expr] = None


class Table(Relation):
    name: QualifiedName


class AliasedRelation(Relation):
    relation: Relation
    alias: Identifier


class GroupBy(Node):
    exprs: ta.Sequence[Expr]


class SelectItem(Node, abstract=True):
    pass


class AllSelectItem(SelectItem):
    pass


class ExprSelectItem(Node):
    expr: Expr
    label: ta.Optional[Identifier] = None


class SetQuantifier(enum.Enum):
    DISTINCT = 'distinct'
    ALL = 'all'


SET_QUANTIFIER_MAP: ta.Mapping[str, SetQuantifier] = {v.value: v for v in SetQuantifier.__members__.values()}


class Cte(Node):
    name: Identifier
    select: 'Select'


class Select(Node):
    items: ta.Sequence[SelectItem]
    relations: ta.Sequence[Relation]
    where: ta.Optional[Expr] = None
    ctes: ta.Optional[ta.Sequence[Cte]] = None
    set_quantifier: ta.Optional[SetQuantifier] = None
    group_by: ta.Optional[GroupBy] = None
