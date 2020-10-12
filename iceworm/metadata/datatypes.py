"""
TODO:
 - * nullary singletons via __new__ *
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
from omnibus import reflect as rfl

from ..utils import seq
from ..utils import serde


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

NUMBER = Number()
INT = Int()
INTEGER = Integer()
NUMERIC = Numeric()
SMALLINT = Smallint()


class Decimal(Datatype):
    pass


DECIMAL = Decimal()


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


FLOAT = Float()


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

CHAR = Char()
CHARACTER = Character()
STRING = String()
TEXT = Text()


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


BINARY = Binary()


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


BOOLEAN = Boolean()


class Date(Datatype):
    pass


DATE = Date()


class Time(Datatype):
    pass


TIME = Time()


class TimestampNtz(Datatype):
    ALIASES: ta.ClassVar = {
        'datetime',
    }


Datetime = TimestampNtz

TIMESTAMP_NTZ = TimestampNtz()
DATETIME = Datetime()


class TimestampLtz(Datatype):
    pass


TIMESTAMP_LTZ = TimestampLtz()


class TimestampTz(Datatype):
    pass


TIMESTAMP_TZ = TimestampTz()


class Variant(Datatype):
    pass


class Object(Datatype):
    pass


class Array(Datatype):
    pass


VARIANT = Variant()
OBJECT = Object()
ARRAY = Array()


class Geography(Datatype):
    pass


GEOGRAPHY = Geography()


class TableType(Datatype):
    columns: ta.Sequence[ta.Tuple[str, Datatype]] = dc.field(
        coerce=seq, check=lambda l: all(isinstance(k, str) and isinstance(v, Datatype) for k, v in l))


class DatatypeSerde(serde.AutoSerde[Datatype]):

    @property
    def handles_dataclass_polymorphism(self) -> bool:
        return True

    def serialize(self, obj: Datatype) -> ta.Any:
        return serde.serialize_dataclass(obj, spec=rfl.spec(Datatype), no_custom=True)

    def deserialize(self, ser: ta.Any) -> Datatype:
        if isinstance(ser, str):
            cls = Datatype.CLS_MAP[ser]
            return cls()
        return serde.deserialize_dataclass(ser, Datatype, no_custom=True)


@serde.subclass_map_resolver_for(Datatype)
def _build_datatype_subclass_map(cls: type) -> ta.Mapping[ta.Union[str, type], ta.Union[str, type]]:
    check.state(cls is Datatype)
    dct = dict(serde.build_subclass_map(Datatype))
    for k, v in list(dct.items()):
        for a in getattr(v, 'ALIASES', []):
            check.not_in(a, dct)
            dct[a] = v
    return dct
