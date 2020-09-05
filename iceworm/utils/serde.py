"""
TODO:
 - strict mode
 - replace with builtin omni generic impl
 - extensible serde Contexts? want pluggable datatypes, -> Datatype.of
"""
import abc
import collections.abc
import enum
import typing as ta
import weakref

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import defs
from omnibus import lang
from omnibus import reflect as rfl


class Ignore(lang.Marker):
    pass


class GetType(lang.Marker):
    pass


class Name(lang.Marker):
    pass


class Aliases(lang.Marker):
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


class Serde(lang.Abstract, ta.Generic[T]):

    @abc.abstractmethod
    def serialize(self, obj: T) -> ta.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def deserialize(self, ser: ta.Any) -> T:
        raise NotImplementedError


_SERDES_BY_CLS: ta.MutableMapping[type, Serde] = weakref.WeakKeyDictionary()


def serde_for(*clss):
    def inner(obj):
        if isinstance(obj, type):
            sd = obj()
        else:
            sd = obj
        check.isinstance(sd, Serde)
        for c in clss:
            check.not_in(c, _SERDES_BY_CLS)
            _SERDES_BY_CLS[c] = sd
        return obj
    check.arg(all(isinstance(c, type) for c in clss))
    return inner


class AutoSerde(Serde[T], lang.Abstract):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        check.state(cls.__bases__ == (AutoSerde,))
        arg = check.single(rfl.spec(check.single(cls.__orig_bases__)).args)
        ty = check.isinstance(check.isinstance(arg, rfl.NonGenericTypeSpec).cls, type)
        serde_for(ty)(cls)


SubclassMap = ta.Mapping[ta.Union[str, type], ta.Union[type, str]]  # FIXME: gross
_SUBCLASS_MAP_RESOLVERS_BY_CLS: ta.MutableMapping[type, ta.Callable[[type], SubclassMap]] = weakref.WeakKeyDictionary()

_SUBCLASS_MAPS_BY_CLS: ta.MutableMapping[type, SubclassMap] = weakref.WeakKeyDictionary()


def subclass_map_resolver_for(*clss):
    def inner(fn):
        check.callable(fn)
        for c in clss:
            check.not_in(c, _SUBCLASS_MAP_RESOLVERS_BY_CLS)
            _SUBCLASS_MAP_RESOLVERS_BY_CLS[c] = fn
        return fn
    check.arg(all(isinstance(c, type) for c in clss))
    return inner


def format_subclass_name(cls: type) -> str:
    check.isinstance(cls, type)
    return lang.decamelize(cls.__name__)


def build_subclass_map(
        cls: type,
        *,
        name_formatter: ta.Callable[[type], str] = format_subclass_name,
) -> SubclassMap:
    dct = {}
    todo = {cls}
    seen = set()
    while todo:
        cur = todo.pop()
        if cur in seen:
            continue
        seen.add(cur)
        n = None
        if dc.is_dataclass(cls):
            n = dc.metadatas_dict(cls, shallow=True).get(Name)
        if n is None:
            n = name_formatter(cur)
        check.isinstance(n, str)
        check.not_empty(n)
        try:
            existing = dct[n]
        except KeyError:
            pass
        else:
            if existing is not cur:
                raise NameError(n)
        dct[n] = cur
        dct[cur] = n
        todo.update(cur.__subclasses__())
    return dct


def get_subclass_map(cls: type) -> SubclassMap:
    if not isinstance(cls, type):
        raise TypeError(cls)
    try:
        return _SUBCLASS_MAPS_BY_CLS[cls]
    except KeyError:
        try:
            bld = _SUBCLASS_MAP_RESOLVERS_BY_CLS[cls]
        except KeyError:
            bld = build_subclass_map
        dct = _SUBCLASS_MAPS_BY_CLS[cls] = bld(cls)
        return dct


_IS_MONOMORPHIC_DATACLASS_BY_CLS: ta.MutableMapping[type, bool] = weakref.WeakKeyDictionary()


def _is_monomorphic_dataclass(cls: type) -> bool:
    try:
        return _IS_MONOMORPHIC_DATACLASS_BY_CLS[cls]
    except KeyError:
        scm = get_subclass_map(cls)
        scmcls = {k: v for k, v in scm.items() if isinstance(k, type)}
        ret = False
        if len(scmcls) == 1 and list(scmcls) == [cls] and lang.Final in cls.__bases__:
            ret = True
        _IS_MONOMORPHIC_DATACLASS_BY_CLS[cls] = ret
        return ret


class _DataclassFieldSerde(dc.Pure):
    cls: ta.Any
    ignore_if: ta.Optional[ta.Callable[[ta.Any], bool]] = dc.field(None, kwonly=True)


_DataclassFieldSerdeMap = ta.Mapping[str, _DataclassFieldSerde]
_FIELD_TYPE_MAPS_BY_DATACLASS: ta.MutableMapping[type, _DataclassFieldSerdeMap] = weakref.WeakKeyDictionary()


def _get_dataclass_field_type_map(dcls: type) -> _DataclassFieldSerdeMap:
    if not isinstance(dcls, type) or not dc.is_dataclass(dcls):
        raise TypeError(dcls)
    try:
        return _FIELD_TYPE_MAPS_BY_DATACLASS[dcls]
    except KeyError:
        th = ta.get_type_hints(dcls)
        dct = {}
        for f in dc.fields(dcls):
            try:
                ig = f.metadata[Ignore]
            except KeyError:
                ignore_if = None
            else:
                if callable(ig):
                    ignore_if = ig
                elif ig:
                    continue
            if GetType in f.metadata:
                fcls = f.metadata[GetType](dcls)
            else:
                fcls = th[f.name]
            dct[f.name] = _DataclassFieldSerde(fcls, ignore_if=ignore_if)
        _FIELD_TYPE_MAPS_BY_DATACLASS[dcls] = dct
        return dct


def serialize_dataclass(obj: T, *, fcls: ta.Optional[ta.Type] = None) -> Serialized:
    dct = {}
    for fn, fs in _get_dataclass_field_type_map(type(obj)).items():
        v = getattr(obj, fn)
        if fs.ignore_if is not None and fs.ignore_if(v):
            continue
        dct[fn] = serialize(v, fcls=fs.cls)
    if fcls is type(obj) and _is_monomorphic_dataclass(fcls):
        return dct
    else:
        scm = get_subclass_map(type(obj))
        return {check.isinstance(scm[type(obj)], str): dct}


def serialize(obj: T, *, fcls: ta.Optional[ta.Type] = None) -> Serialized:
    if fcls is not None and rfl.is_generic(fcls) and fcls.__origin__ is ta.Union:
        args = fcls.__args__
        if len(args) != 2 or type(None) not in args:
            raise TypeError(fcls)
        [fcls] = [a for a in args if a not in (None, type(None))]

    if type(obj) in _SERDES_BY_CLS:
        serde = _SERDES_BY_CLS[type(obj)]
        return serde.serialize(obj)

    elif dc.is_dataclass(obj):
        return serialize_dataclass(obj, fcls=fcls)

    elif isinstance(obj, collections.abc.Mapping):
        if fcls is not None and rfl.is_generic(fcls) and fcls.__origin__ is collections.abc.Mapping:
            [kfcls, vfcls] = fcls.__args__
        else:
            kfcls = vfcls = None
        return [[serialize(k, fcls=kfcls), serialize(v, fcls=vfcls)] for k, v in obj.items()]

    elif isinstance(obj, (collections.abc.Sequence, collections.abc.Set)) and not isinstance(obj, str):
        if fcls is not None and rfl.is_generic(fcls) and fcls.__origin__ is collections.abc.Sequence:
            [efcls] = fcls.__args__
        else:
            efcls = None
        return [serialize(e, fcls=efcls) for e in obj]

    elif isinstance(obj, enum.Enum):
        return obj.name

    elif isinstance(obj, PRIMITIVE_TYPES_TUPLE):
        return obj

    else:
        raise TypeError(obj)


def deserialize_dataclass(ser: Serialized, cls: type, *, succinct: bool = False) -> T:
    if succinct and _is_monomorphic_dataclass(cls):
        dct = ser
        dcls = cls
    else:
        [[n, dct]] = ser.items()
        dcls = check.isinstance(get_subclass_map(cls)[n], type)
    fdct = _get_dataclass_field_type_map(dcls)
    kw = {}
    for k, v in dct.items():
        try:
            fs = fdct[k]
        except KeyError:
            breakpoint()
            raise
        kw[k] = deserialize(v, fs.cls, succinct=True)
    return dcls(**kw)


def _deserialize(ser: Serialized, cls: ta.Type[T], *, succinct: bool = False) -> T:
    if rfl.is_generic(cls) and cls.__origin__ is ta.Union:
        args = cls.__args__
        if len(args) != 2 or type(None) not in args:
            raise TypeError(cls)
        [ecls] = [a for a in args if a not in (None, type(None))]
        if ser is None:
            return None
        cls = ecls

    if isinstance(cls, type) and cls in _SERDES_BY_CLS:
        serde = _SERDES_BY_CLS[cls]
        return serde.deserialize(ser)

    elif rfl.is_generic(cls) and cls.__origin__ is collections.abc.Mapping:
        [kcls, vcls] = cls.__args__
        dct = {}
        if isinstance(ser, str):
            raise TypeError(ser)
        elif isinstance(ser, collections.abc.Mapping):
            for kser, vser in ser.items():
                k, v = deserialize(kser, kcls, succinct=succinct), deserialize(vser, vcls, succinct=succinct)
                if k in dct:
                    raise KeyError(k)
                dct[k] = v
        elif isinstance(ser, collections.abc.Sequence):
            for e in ser:
                if not isinstance(e, collections.abc.Sequence) or isinstance(e, str):
                    raise TypeError(e)
                kser, vser = e
                k, v = deserialize(kser, kcls, succinct=succinct), deserialize(vser, vcls, succinct=succinct)
                if k in dct:
                    raise KeyError(k)
                dct[k] = v
        else:
            raise TypeError(ser)
        return dct

    elif rfl.is_generic(cls) and cls.__origin__ is collections.abc.Set:
        [ecls] = cls.__args__
        if not isinstance(ser, collections.abc.Sequence):
            raise TypeError(ser)
        return {deserialize(e, ecls, succinct=succinct) for e in ser}

    elif rfl.is_generic(cls) and cls.__origin__ is collections.abc.Sequence:
        [ecls] = cls.__args__
        if not isinstance(ser, collections.abc.Sequence) or isinstance(ser, str):
            raise TypeError(ser)
        return [deserialize(e, ecls, succinct=succinct) for e in ser]

    elif rfl.is_generic(cls) and cls.__origin__ is collections.abc.Callable:
        if not callable(ser):
            raise TypeError(ser)
        return ser

    elif not isinstance(cls, type):
        raise TypeError(cls)

    elif dc.is_dataclass(cls):
        if not isinstance(ser, collections.abc.Mapping):
            raise TypeError(ser)
        return deserialize_dataclass(ser, cls, succinct=succinct)

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


def deserialize(ser: Serialized, cls: ta.Type[T], no_reraise: bool = False, succinct: bool = False) -> T:
    if no_reraise:
        return _deserialize(ser, cls, succinct=succinct)
    else:
        try:
            return _deserialize(ser, cls, succinct=succinct)
        except Exception as e:
            raise DeserializationException(cls=cls, ser=ser) from e
