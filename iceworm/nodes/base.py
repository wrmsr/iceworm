"""
TODO:
 - enable type checking
 - standardize names (+in g4): Expr not expression, Stmt not statement, Value not val, Rel not rel?
 - enforce field types (children in seqs only)

Visitors / Tools:
 - graphviz gen
"""
import collections.abc
import enum
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties

from .. import serde
from ..types import QualifiedName
from ..utils import build_dc_repr
from ..utils import build_enum_value_map
from ..utils import seq


SelfNode = ta.TypeVar('SelfNode', bound='Node')
NodeGen = ta.Generator['Node', None, None]
NodeMapper = ta.Callable[['Node'], 'Node']


class Node(dc.Enum, reorder=True, repr=False, sealed='package'):

    meta: ta.Mapping[ta.Any, ta.Any] = dc.field(
        ocol.frozendict(),
        kwonly=True,
        repr=False,
        hash=False,
        compare=False,
        coerce=ocol.frozendict,
        metadata={serde.Ignore: True},
    )

    __repr__ = build_dc_repr

    def yield_field_children(self, fld: dc.Field) -> NodeGen:
        val = getattr(self, fld.name)
        if isinstance(val, Node):
            yield val
        elif isinstance(val, collections.abc.Sequence):
            yield from (item for item in val if isinstance(item, Node))

    @property
    def children(self) -> NodeGen:
        for fld in dc.fields(self):
            yield from self.yield_field_children(fld)

    def build_field_map_kwargs(self, fn: NodeMapper, fld: dc.Field) -> ta.Mapping[str, ta.Any]:
        val = getattr(self, fld.name)
        if isinstance(val, Node):
            return {fld.name: fn(val)}
        elif isinstance(val, collections.abc.Sequence) and not isinstance(val, str):
            return {fld.name: ocol.frozenlist([fn(item) if isinstance(item, Node) else item for item in val])}
        else:
            return {}

    def map(self: SelfNode, fn: NodeMapper, **kwargs) -> SelfNode:
        rpl_kw = {**kwargs}
        for fld in dc.fields(self):
            if fld.name in kwargs:
                continue
            for k, v in self.build_field_map_kwargs(fn, fld).items():
                if k in rpl_kw:
                    raise KeyError(k)
                rpl_kw[k] = v
        return dc.replace(self, **rpl_kw)


class Expr(Node, abstract=True):
    pass


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
    parts: ta.Sequence[Identifier] = dc.field(coerce=seq)

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


class Primitive(Expr, abstract=True):
    pass


class Number(Expr, abstract=True):
    pass


class Integer(Number):
    value: int


class Decimal(Number):
    value: str


class Float(Number):
    value: str


class String(Primitive):
    value: str


class StarExpr(Primitive):
    pass


class Null(Primitive):
    pass


class ETrue(Primitive):
    pass


class EFalse(Primitive):
    pass


class TypeSpec(Node):
    name: Identifier
    args: ta.Sequence[Expr] = dc.field((), coerce=seq)


class Direction(enum.Enum):
    ASC = 'asc'
    DESC = 'desc'


DIRECTION_MAP: ta.Mapping[str, Direction] = build_enum_value_map(Direction)


class FirstOrLast(enum.Enum):
    FIRST = 'first'
    LAST = 'last'


class SortItem(Node):
    value: Expr
    direction: ta.Optional[Direction] = None
    nulls: ta.Optional[FirstOrLast] = None


class SetQuantifier(enum.Enum):
    DISTINCT = 'distinct'
    EXCEPT = 'except'
    ALL = 'all'


SET_QUANTIFIER_MAP: ta.Mapping[str, SetQuantifier] = build_enum_value_map(SetQuantifier)
