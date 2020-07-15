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


SelfNode = ta.TypeVar('SelfNode', bound='Node')
NodeGen = ta.Generator['Node', None, None]
NodeMapper = ta.Callable[['Node'], 'Node']


class Node(dc.Enum, sealed=True):

    @property
    def children(self) -> NodeGen:
        for fld in dc.fields(self):
            val = getattr(self, fld.name)
            if isinstance(val, Node):
                yield val
            elif isinstance(val, collections.abc.Sequence):
                yield from (item for item in val if isinstance(item, Node))

    def map(self: SelfNode, fn: NodeMapper) -> SelfNode:
        kw = {}
        for fld in dc.fields(self):
            val = getattr(self, fld.name)
            if isinstance(val, Node):
                kw[fld.name] = fn(val)
            elif isinstance(val, collections.abc.Sequence):
                kw[fld.name] = [fn(item) if isinstance(item, Node) else item for item in val]
        return dc.replace(self, **kw)


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


class FirstOrLast(enum.Enum):
    FIRST = 'first'
    LAST = 'last'


class SortItem(Node):
    value: Expr
    direction: ta.Optional[Direction] = None
    nulls: ta.Optional[FirstOrLast] = None


class Precedence(enum.Enum):
    PRECEDING = 'preceding'
    FOLLOWING = 'following'


class FrameBound(Node, abstract=True):
    pass


class NumFrameBound(FrameBound):
    num: int
    precedence: Precedence


class UnboundedFrameBound(FrameBound):
    precedence: Precedence


class CurrentRowFrameBound(FrameBound):
    pass


class Frame(Node, abstract=True):
    pass


class RowsOrRange(enum.Enum):
    ROWS = 'rows'
    RANGE = 'range'


class SingleFrame(Node):
    rows_or_range: RowsOrRange
    bound: FrameBound


class DoubleFrame(Node):
    rows_or_range: RowsOrRange
    min: FrameBound
    max: FrameBound


class Over(Node):
    partition_by: ta.Sequence[Expr] = ()
    order_by: ta.Sequence[SortItem] = ()
    frame: ta.Optional[Frame] = None


class StarExpr(Expr):
    pass


class Kwarg(Node):
    name: Identifier
    value: Expr


class IgnoreOrRespect(enum.Enum):
    IGNORE = 'ignore'
    RESPECT = 'respect'


class FunctionCall(Node):
    name: QualifiedNameNode
    args: ta.Sequence[Expr] = ()
    kwargs: ta.Sequence[Kwarg] = ()
    set_quantifier: ta.Optional['SetQuantifier'] = None
    nulls: ta.Optional[IgnoreOrRespect] = None
    within_group: ta.Sequence[SortItem] = ()
    over: ta.Optional[Over] = None


class FunctionCallExpr(Expr):
    call: FunctionCall


class LastValue(Expr):
    value: Expr
    nulls: ta.Optional[IgnoreOrRespect] = None
    over: ta.Optional[Over] = None


class Null(Expr):
    pass


class ETrue(Expr):
    pass


class EFalse(Expr):
    pass


class Interval(Expr):
    value: Expr


class CaseItem(Node):
    when: Expr
    then: Expr


class Case(Expr):
    value: ta.Optional[Expr]
    items: ta.Sequence[CaseItem]
    default: ta.Optional[Expr] = None


class Colon(Expr):
    value: Expr
    name: Identifier


class Bracket(Expr):
    value: Expr
    index: Expr


class TypeSpec(Node):
    name: Identifier
    args: ta.Sequence[Expr] = ()


class Cast(Expr):
    value: Expr
    type: TypeSpec


class CastCall(Expr):
    value: Expr
    type: TypeSpec


class IsNull(Expr):
    value: Expr
    not_: bool = False


class LikeKind(enum.Enum):
    LIKE = 'like'
    ILIKE = 'ilike'
    RLIKE = 'rlike'


LIKE_KIND_MAP: ta.Mapping[str, LikeKind] = {v.value: v for v in LikeKind.__members__.values()}


class Like(Expr):
    kind: LikeKind
    value: Expr
    patterns: ta.Sequence[Expr]
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
    haystack: ta.Sequence[Expr]
    not_: bool = False


class InSelect(Expr):
    needle: Expr
    haystack: 'Selectable'
    not_: bool = False


class Between(Expr):
    value: Expr
    lower: Expr
    upper: Expr


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
    using: ta.Optional[ta.Sequence[Identifier]] = None


class Pivot(Relation):
    relation: Relation
    func: QualifiedNameNode
    pivot_col: Identifier
    value_col: Identifier
    values: ta.Sequence[Expr]


class Unpivot(Relation):
    relation: Relation
    value_col: Identifier
    name_col: Identifier
    pivot_cols: ta.Sequence[Identifier]


class Lateral(Relation):
    relation: Relation


class FunctionCallRelation(Relation):
    call: FunctionCall


class Table(Relation):
    name: QualifiedNameNode


class AliasedRelation(Relation):
    relation: Relation
    alias: Identifier
    columns: ta.Sequence[Identifier] = ()


class SelectItem(Node, abstract=True):
    pass


class AllSelectItem(SelectItem):
    pass


class IdentifierAllSelectItem(SelectItem):
    identifier: Identifier


class ExprSelectItem(Node):
    value: Expr
    label: ta.Optional[Identifier] = None


class SetQuantifier(enum.Enum):
    DISTINCT = 'distinct'
    ALL = 'all'


SET_QUANTIFIER_MAP: ta.Mapping[str, SetQuantifier] = {v.value: v for v in SetQuantifier.__members__.values()}


class Grouping(Node, abstract=True):
    pass


class FlatGrouping(Grouping):
    items: ta.Sequence[Expr]


class GroupingSet(Node):
    items: ta.Sequence[Expr]


class SetsGrouping(Grouping):
    sets: ta.Sequence[GroupingSet]


class Selectable(Node, abstract=True):
    pass


class Select(Selectable):
    items: ta.Sequence[SelectItem]
    relations: ta.Sequence[Relation] = ()
    where: ta.Optional[Expr] = None
    top_n: ta.Optional[Integer] = None
    set_quantifier: ta.Optional[SetQuantifier] = None
    group_by: ta.Optional[Grouping] = None
    having: ta.Optional[Expr] = None
    qualify: ta.Optional[Expr] = None
    order_by: ta.Optional[ta.Sequence[SortItem]] = None
    limit: ta.Optional[int] = None


class Cte(Node):
    name: Identifier
    select: 'Selectable'


class CteSelect(Selectable):
    ctes: ta.Sequence[Cte]
    select: Selectable


class UnionItem(Node):
    right: Selectable
    set_quantifier: SetQuantifier = None


class UnionSelect(Selectable):
    left: Selectable
    items: ta.Sequence[UnionItem]


class SelectExpr(Expr):
    select: 'Selectable'


class SelectRelation(Relation):
    select: 'Selectable'


class JinjaExpr(Expr):
    text: str


class JinjaRelation(Relation):
    text: str


class InJinja(Expr):
    needle: Expr
    text: str
    not_: bool = False
