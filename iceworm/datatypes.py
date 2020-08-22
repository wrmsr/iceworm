"""
TODO:
 - sqla bidir adapter (postgres specifically)
 - bottom type for null const?
"""
import typing as ta

from omnibus import dataclasses as dc

from .utils import seq


class Datatype(dc.Enum):
    ALIASES: ta.ClassVar[ta.AbstractSet[str]] = frozenset()


class Number(Datatype):
    ALIASES: ta.ClassVar = {
        'bigint',
        'int',
        'integer',
        'numeric',
        'smallint',
    }


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
        'float',
        'float4',
        'float8',
        'real',
    }


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


class Boolean(Datatype):
    pass


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
