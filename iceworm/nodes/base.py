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
from ..utils import NodalDataclass
from ..utils import build_dc_repr
from ..utils import build_enum_value_map
from ..utils import seq


SelfNode = ta.TypeVar('SelfNode', bound='Node')
NodeGen = ta.Generator['Node', None, None]
NodeMapper = ta.Callable[['Node'], 'Node']


class Node(dc.Enum, NodalDataclass['Node'], reorder=True, repr=False, sealed='package'):

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

    @classmethod
    def _nodal_cls(cls) -> ta.Type['Node']:
        return Node


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
        elif isinstance(obj, str):
            raise TypeError(obj)
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
