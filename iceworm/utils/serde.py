"""
TODO:
 - replace with builtin omni generic impl
"""
import collections.abc
import enum
import typing as ta
import weakref

from omnibus import dataclasses as dc
from omnibus import defs
from omnibus import lang
from omnibus import reflect as rfl


class Ignore(lang.Marker):
    pass


T = ta.TypeVar('T')


Primitive = ta.Union[
    None,
    bool,
    float,
    int,
    str,
]

PRIMITIVE_TYPES: ta.AbstractSet[type] = frozenset(Primitive.__args__)
PRIMITIVE_TYPES_TUPLE = tuple(PRIMITIVE_TYPES)


MappingKey = ta.Union[int, str]


Serializable = ta.Union[
    Primitive,
    enum.Enum,
    ta.Optional['Serializable'],
    ta.Sequence['Serializable'],
    ta.AbstractSet['Serializable'],
    ta.Mapping[MappingKey, 'Serializable'],
]

Serialized = ta.Union[
    Primitive,
    ta.Optional['Serialized'],
    ta.List['Serialized'],
    ta.Dict[str, 'Serialized'],
]


_SubclassMap = ta.Mapping[str, type]
_SUBCLASS_MAPS_BY_CLS: ta.MutableMapping[type, _SubclassMap] = weakref.WeakKeyDictionary()


def _get_subclass_map(cls: type) -> _SubclassMap:
    if not isinstance(cls, type):
        raise TypeError(cls)
    try:
        return _SUBCLASS_MAPS_BY_CLS[cls]
    except KeyError:
        dct = {}
        todo = {cls}
        seen = set()
        while todo:
            cur = todo.pop()
            if cur in seen:
                continue
            seen.add(cur)
            n = cur.__name__
            try:
                existing = dct[n]
            except KeyError:
                pass
            else:
                if existing is not cur:
                    raise NameError(n)
            dct[n] = cur
            todo.update(cur.__subclasses__())
        _SUBCLASS_MAPS_BY_CLS[cls] = dct
        return dct


_DataclassFieldTypeMap = ta.Mapping[str, ta.Any]
_FIELD_TYPE_MAPS_BY_DATACLASS: ta.MutableMapping[type, _DataclassFieldTypeMap] = weakref.WeakKeyDictionary()


def _get_dataclass_field_type_map(dcls: type) -> _DataclassFieldTypeMap:
    if not isinstance(dcls, type) or not dc.is_dataclass(dcls):
        raise TypeError(dcls)
    try:
        return _FIELD_TYPE_MAPS_BY_DATACLASS[dcls]
    except KeyError:
        th = ta.get_type_hints(dcls)
        dct = _FIELD_TYPE_MAPS_BY_DATACLASS[dcls] = {
            f.name: th[f.name]
            for f in dc.fields(dcls)
            if not f.metadata.get(Ignore)
        }
        return dct


def serialize(obj: T) -> Serialized:
    if dc.is_dataclass(obj):
        dct = {fn: serialize(getattr(obj, fn)) for fn in _get_dataclass_field_type_map(type(obj))}
        return {type(obj).__name__: dct}

    elif isinstance(obj, collections.abc.Mapping):
        return [[serialize(k), serialize(v)] for k, v in obj.items()]

    elif isinstance(obj, (collections.abc.Sequence, collections.abc.Set)) and not isinstance(obj, str):
        return [serialize(e) for e in obj]

    elif isinstance(obj, enum.Enum):
        return obj.name

    elif isinstance(obj, PRIMITIVE_TYPES_TUPLE):
        return obj

    else:
        raise TypeError(obj)


def _deserialize(ser: Serialized, cls: ta.Type[T]) -> T:
    if rfl.is_generic(cls) and cls.__origin__ is ta.Union:
        args = cls.__args__
        if len(args) != 2 or type(None) not in args:
            raise TypeError(cls)
        [ecls] = [a for a in args if a not in (None, type(None))]
        if ser is None:
            return None
        cls = ecls

    if rfl.is_generic(cls) and cls.__origin__ is collections.abc.Mapping:
        [kcls, vcls] = cls.__args__
        if not isinstance(ser, collections.abc.Sequence) or isinstance(ser, str):
            raise TypeError(ser)
        dct = {}
        for e in ser:
            if not isinstance(e, collections.abc.Sequence) or isinstance(e, str):
                raise TypeError(e)
            kser, vser = e
            k, v = deserialize(kser, kcls), deserialize(vser, vcls)
            if k in dct:
                raise KeyError(k)
            dct[k] = v
        return dct

    elif rfl.is_generic(cls) and cls.__origin__ is collections.abc.Set:
        [ecls] = cls.__args__
        if not isinstance(ser, collections.abc.Sequence):
            raise TypeError(ser)
        return {deserialize(e, ecls) for e in ser}

    elif rfl.is_generic(cls) and cls.__origin__ is collections.abc.Sequence:
        [ecls] = cls.__args__
        if not isinstance(ser, collections.abc.Sequence) or isinstance(ser, str):
            raise TypeError(ser)
        return [deserialize(e, ecls) for e in ser]

    elif not isinstance(cls, type):
        raise TypeError(cls)

    elif dc.is_dataclass(cls):
        if not isinstance(ser, collections.abc.Mapping):
            raise TypeError(ser)
        [[n, dct]] = ser.items()
        dcls = _get_subclass_map(cls)[n]
        fdct = _get_dataclass_field_type_map(dcls)
        kw = {}
        for k, v in dct.items():
            fcls = fdct[k]
            kw[k] = deserialize(v, fcls)
        return dcls(**kw)

    elif issubclass(cls, enum.Enum):
        if isinstance(ser, str):
            return cls.__members__[ser]
        else:
            raise TypeError(ser)

    elif cls in PRIMITIVE_TYPES:
        if isinstance(ser, cls):
            return ser
        elif isinstance(ser, str):
            return cls(ser)
        else:
            raise TypeError(ser)

    else:
        raise TypeError(cls)


class DeserializationException(Exception):

    def __init__(self, *args, cls: ta.Type[T], ser: Serialized) -> None:
        super().__init__(*args)

        self.cls = cls
        self.ser = ser

    defs.basic('args', 'cls', 'ser')

    def __str__(self) -> str:
        return repr(self)


def deserialize(ser: Serialized, cls: ta.Type[T]) -> T:
    try:
        return _deserialize(ser, cls)
    except Exception as e:
        raise DeserializationException(cls=cls, ser=ser) from e
