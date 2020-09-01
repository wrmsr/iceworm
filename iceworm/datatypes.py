"""
TODO:
 - sqla bidir adapter (postgres specifically)
 - bottom type for null const?
 - annotations?
  - NonNull? Nullable?
 - serde aliases - subclass map thing
 - serde types as just strings
"""
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from .utils import seq
from .utils import serde


class Datatype(dc.Enum):
    ALIASES: ta.ClassVar[ta.AbstractSet[str]] = frozenset()

    @property
    def py_type(self) -> type:
        raise TypeError

    @property
    def is_equatable(self) -> bool:
        return False

    @property
    def is_sortable(self) -> bool:
        return False


class Number(Datatype):
    ALIASES: ta.ClassVar = {
        'bigint',
        'int',
        'integer',
        'numeric',
        'smallint',
    }

    @property
    def py_type(self) -> type:
        return int

    @property
    def is_equatable(self) -> bool:
        return True

    @property
    def is_sortable(self) -> bool:
        return True


Bigint = Number
Int = Number
Integer = Number
Numeric = Number
Smallint = Number


class Decimal(Datatype):
    pass


class Float(Datatype):
    ALIASES: ta.ClassVar = {
        'double precision',
        'double',
        'float4',
        'float8',
        'real',
    }

    @property
    def py_type(self) -> type:
        return float

    @property
    def is_sortable(self) -> bool:
        return True


class Varchar(Datatype):
    ALIASES: ta.ClassVar = {
        'char',
        'character',
        'string',
        'text',
    }


Char = Varchar
Character = Varchar
String = Varchar
Text = Varchar


class Binary(Datatype):
    ALIASES: ta.ClassVar = {
        'varbinary'
    }

    @property
    def py_type(self) -> type:
        return bytes

    @property
    def is_equatable(self) -> bool:
        return True

    @property
    def is_sortable(self) -> bool:
        return True


class Boolean(Datatype):

    @property
    def py_type(self) -> type:
        return bool

    @property
    def is_equatable(self) -> bool:
        return True

    @property
    def is_sortable(self) -> bool:
        return True


class Date(Datatype):
    pass


class Time(Datatype):
    pass


class TimestampNtz(Datatype):
    ALIASES: ta.ClassVar = {
        'datetime',
    }


Datetime = TimestampNtz


class TimestampLtz(Datatype):
    pass


class TimestampTz(Datatype):
    pass


class Variant(Datatype):
    pass


class Object(Datatype):
    pass


class Array(Datatype):
    pass


class Geography(Datatype):
    pass


class Table(Datatype):
    columns: ta.Sequence[ta.Tuple[str, Datatype]] = dc.field(
        coerce=seq, check=lambda l: all(isinstance(k, str) and isinstance(v, Datatype) for k, v in l))


def _build_datatype_subclass_map(cls: type) -> ta.Mapping[ta.Union[str, type], ta.Union[str, type]]:
    check.state(cls is Datatype)
    dct = serde.build_subclass_map(Datatype)
    for k, v in list(dct.items()):
        for a in getattr(v, 'ALIASES', []):
            check.not_in(a, dct)
            dct[a] = v
    return dct


serde.SUBCLASS_MAP_RESOLVERS_BY_CLS[Datatype] = _build_datatype_subclass_map
