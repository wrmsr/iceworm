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
from omnibus import lang

from .utils import seq
from .utils import serde


class Datatype(dc.Enum):
    ALIASES: ta.ClassVar[ta.AbstractSet[str]] = frozenset()

    CLS_MAP: ta.ClassVar[ta.Mapping[str, ta.Type['Datatype']]] = {}

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        if lang.Abstract not in cls.__bases__:
            for n in [cls.__name__.lower()] + list(cls.ALIASES):
                check.not_in(n, Datatype.CLS_MAP)
                Datatype.CLS_MAP[n] = cls

    @property
    def py_type(self) -> type:
        raise TypeError

    @property
    def is_equatable(self) -> bool:
        return False

    @property
    def is_sortable(self) -> bool:
        return False

    @classmethod
    def of(cls, obj: 'Datatype') -> 'Datatype':
        if isinstance(obj, Datatype):
            return obj
        else:
            raise TypeError(obj)


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


class DatatypeSerde(serde.AutoSerde[Datatype]):

    def serialize(self, obj: Datatype) -> ta.Any:
        return serde.serialize_dataclass(obj)

    def deserialize(self, ser: ta.Any) -> Datatype:
        if isinstance(ser, str):
            cls = Datatype.CLS_MAP[ser]
            return cls()
        return serde.deserialize_dataclass(ser, Datatype)


@serde.subclass_map_resolver_for(Datatype)
def _build_datatype_subclass_map(cls: type) -> ta.Mapping[ta.Union[str, type], ta.Union[str, type]]:
    check.state(cls is Datatype)
    dct = dict(serde.build_subclass_map(Datatype))
    for k, v in list(dct.items()):
        for a in getattr(v, 'ALIASES', []):
            check.not_in(a, dct)
            dct[a] = v
    return dct
