"""
TODO:
 - sqla bidir adapter
"""
import typing as ta

from omnibus import dataclasses as dc


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
