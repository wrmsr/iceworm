"""
TODO:
 - enable type checking
"""
import collections.abc
import enum
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import properties

from .types import QualifiedName


NodeGen = ta.Generator['Node', None, None]


class Node(dc.Enum, sealed=True):

    @property
    def children(self) -> NodeGen:
        return
        yield


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

    @property
    def children(self) -> NodeGen:
        yield self.value


class Identifier(Expr):
    name: str

    @classmethod
    def of(cls, obj: ta.Union['Identifier', str]) -> 'Identifier':
        if isinstance(obj, Identifier):
            return cls(obj.name)
        elif isinstance(obj, str):
            return cls(obj)
        else:
            raise TypeError(obj)


class QualifiedNameNode(Expr):
    parts: ta.Sequence[Identifier]

    @properties.cached
    def name(self) -> QualifiedName:
        return QualifiedName(tuple(p.name for p in self.parts))

    @property
    def children(self) -> NodeGen:
        yield from self.parts

    @classmethod
    def of(
            cls,
            obj: ta.Union[
                'QualifiedNameNode',
                QualifiedName,
                ta.Iterable[ta.Union[Identifier, str]],
            ]
    ) -> 'QualifiedNameNode':
        if isinstance(obj, QualifiedNameNode):
            return cls([Identifier.of(p) for p in obj.parts])
        elif isinstance(obj, QualifiedName):
            return cls([Identifier(p) for p in obj])
        elif isinstance(obj, collections.abc.Iterable):
            return cls([Identifier.of(p) for p in check.not_isinstance(obj, str)])
        else:
            raise TypeError(obj)


class Integer(Expr):
    value: int


class Decimal(Expr):
    value: str


class Float(Expr):
    value: str


class String(Expr):
    value: str


class Direction(enum.Enum):
    ASC = 'asc'
    DESC = 'desc'


DIRECTION_MAP: ta.Mapping[str, Direction] = {v.value: v for v in Direction.__members__.values()}


class SortItem(Node):
    value: Expr
    direction: ta.Optional[Direction] = None

    @property
    def children(self) -> NodeGen:
        yield self.value
        if self.direction is not None:
            yield self.direction


class Over(Node):
    order_by: ta.Optional[ta.Sequence[SortItem]] = None

    @property
    def children(self) -> NodeGen:
        if self.order_by is not None:
            yield from self.order_by


class StarExpr(Expr):
    pass


class FunctionCall(Expr):
    name: QualifiedNameNode
    args: ta.Sequence[Expr] = ()
    over: ta.Optional[Over] = None

    @property
    def children(self) -> NodeGen:
        yield self.name
        yield from self.args
        if self.over is not None:
            yield self.over


class Null(Expr):
    pass


class ETrue(Expr):
    pass


class EFalse(Expr):
    pass


class CaseItem(Node):
    when: Expr
    then: Expr

    @property
    def children(self) -> NodeGen:
        yield from [self.when, self.then]


class Case(Expr):
    items: ta.Sequence[CaseItem]
    default: ta.Optional[Expr] = None

    @property
    def children(self) -> NodeGen:
        yield from self.items
        if self.default is not None:
            yield self.default


class Cast(Expr):
    value: Expr
    type: Identifier

    @property
    def children(self) -> NodeGen:
        yield from [self.value, self.type]


class IsNull(Expr):
    value: Expr
    not_: bool = False

    @property
    def children(self) -> NodeGen:
        yield self.value


class Like(Expr):
    value: Expr
    pattern: Expr
    not_: bool = False

    @property
    def children(self) -> NodeGen:
        yield from [self.value, self.pattern]


class InList(Expr):
    needle: Expr
    haystack: ta.Sequence[Expr]
    not_: bool = False

    @property
    def children(self) -> NodeGen:
        yield self.needle
        yield from self.haystack


class InSelect(Expr):
    needle: Expr
    haystack: 'Selectable'
    not_: bool = False

    @property
    def children(self) -> NodeGen:
        yield from [self.needle, self.haystack]


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

    @property
    def children(self) -> NodeGen:
        yield from [self.left, self.right]
        if self.condition is not None:
            yield self.condition


class Pivot(Relation):
    relation: Relation
    func: QualifiedNameNode
    pivot_col: Identifier
    value_col: Identifier
    values: ta.Sequence[Expr]

    @property
    def children(self) -> NodeGen:
        yield from [self.relation, self.func, self.pivot_col, self.values]
        yield from self.values


class Unpivot(Relation):
    relation: Relation
    value_col: Identifier
    name_col: Identifier
    pivot_cols: ta.Sequence[Identifier]

    @property
    def children(self) -> NodeGen:
        yield from [self.relation, self.value_col, self.name_col]
        yield from self.pivot_cols


class Table(Relation):
    name: QualifiedNameNode

    @property
    def children(self) -> NodeGen:
        yield self.name


class AliasedRelation(Relation):
    relation: Relation
    alias: Identifier

    @property
    def children(self) -> NodeGen:
        yield from [self.relation, self.alias]


class SelectItem(Node, abstract=True):
    pass


class AllSelectItem(SelectItem):
    pass


class ExprSelectItem(Node):
    value: Expr
    label: ta.Optional[Identifier] = None

    @property
    def children(self) -> NodeGen:
        yield self.value
        if self.label is not None:
            yield self.label


class SetQuantifier(enum.Enum):
    DISTINCT = 'distinct'
    ALL = 'all'


SET_QUANTIFIER_MAP: ta.Mapping[str, SetQuantifier] = {v.value: v for v in SetQuantifier.__members__.values()}


class GroupItem(Node):
    value: Expr

    @property
    def children(self) -> NodeGen:
        yield self.value


class GroupBy(Node):
    items: ta.Sequence[GroupItem]

    @property
    def children(self) -> NodeGen:
        yield from self.items


class Selectable(Node, abstract=True):
    pass


class Select(Selectable):
    items: ta.Sequence[SelectItem]
    relations: ta.Sequence[Relation] = ()
    where: ta.Optional[Expr] = None
    top_n: ta.Optional[Integer] = None
    set_quantifier: ta.Optional[SetQuantifier] = None
    group_by: ta.Optional[GroupBy] = None
    having: ta.Optional[Expr] = None
    order_by: ta.Optional[ta.Sequence[SortItem]] = None

    @property
    def children(self) -> NodeGen:
        yield from self.items
        yield from self.relations
        if self.where is not None:
            yield self.where
        if self.top_n is not None:
            yield self.top_n
        if self.set_quantifier is not None:
            yield self.set_quantifier
        if self.group_by is not None:
            yield self.group_by
        if self.having is not None:
            yield self.having
        if self.order_by is not None:
            yield from self.order_by


class Cte(Node):
    name: Identifier
    select: 'Selectable'

    @property
    def children(self) -> NodeGen:
        yield from [self.name, self.select]


class CteSelect(Selectable):
    ctes: ta.Sequence[Cte]
    select: Selectable

    @property
    def children(self) -> NodeGen:
        yield from self.ctes
        yield self.select


class UnionItem(Node):
    right: Selectable
    set_quantifier: SetQuantifier = None

    @property
    def children(self) -> NodeGen:
        yield self.right
        if self.set_quantifier is not None:
            yield self.set_quantifier


class UnionSelect(Selectable):
    left: Selectable
    items: ta.Sequence[UnionItem]

    @property
    def children(self) -> NodeGen:
        yield self.left
        yield from self.items


class SelectExpr(Expr):
    select: 'Selectable'

    @property
    def children(self) -> NodeGen:
        yield self.select


class SelectRelation(Relation):
    select: 'Selectable'

    @property
    def children(self) -> NodeGen:
        yield self.select


class JinjaExpr(Expr):
    text: str


class JinjaRelation(Relation):
    text: str


class InJinja(Expr):
    needle: Expr
    text: str
    not_: bool = False

    @property
    def children(self) -> NodeGen:
        yield self.needle
