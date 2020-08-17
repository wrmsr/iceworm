import enum
import typing as ta

from omnibus import dataclasses as dc

from ...utils import build_enum_value_map
from ...utils import seq
from .base import Expr
from .base import Identifier
from .base import Node
from .base import String
from .base import TypeSpec


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


BINARY_OP_MAP: ta.Mapping[str, BinaryOp] = build_enum_value_map(BinaryOp)


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


UNARY_OP_MAP: ta.Mapping[str, UnaryOp] = build_enum_value_map(UnaryOp)


class UnaryExpr(Expr):
    op: UnaryOp
    value: Expr


class Interval(Expr):
    value: Expr


class CaseItem(Node):
    when: Expr
    then: Expr


class Case(Expr):
    value: ta.Optional[Expr]
    items: ta.Sequence[CaseItem] = dc.field(coerce=seq)
    default: ta.Optional[Expr] = None


class Cast(Expr):
    value: Expr
    type: TypeSpec


class CastCall(Expr):
    value: Expr
    type: TypeSpec


class Traversal(Expr):
    value: Expr
    keys: ta.Sequence[Expr] = dc.field(coerce=seq)


class IsNull(Expr):
    value: Expr
    not_: bool = False


class LikeKind(enum.Enum):
    LIKE = 'like'
    ILIKE = 'ilike'
    RLIKE = 'rlike'


LIKE_KIND_MAP: ta.Mapping[str, LikeKind] = build_enum_value_map(LikeKind)


class Like(Expr):
    kind: LikeKind
    value: Expr
    patterns: ta.Sequence[Expr] = dc.field(coerce=seq)
    not_: bool = False
    any: bool = False
    escape: ta.Optional[Expr] = None


class Date(Expr):
    value: String


class Extract(Expr):
    part: Identifier
    value: Expr


class InList(Expr):
    needle: Expr
    haystack: ta.Sequence[Expr] = dc.field(coerce=seq)
    not_: bool = False


class Between(Expr):
    value: Expr
    lower: Expr
    upper: Expr
