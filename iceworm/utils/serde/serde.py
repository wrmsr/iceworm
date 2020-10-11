"""
TODO:
 - ** (serializers|deserializers)_by_spec
 - strict mode
 - replace with builtin omni generic impl
 - extensible serde Contexts? want pluggable datatypes, -> Datatype.of
 - recursive custom serde?
 - allow_empty? system: {{}}
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

    @property
    def handles_dataclass_polymorphism(self) -> bool:
        return False

    @abc.abstractmethod
    def serialize(self, obj: T) -> ta.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def deserialize(self, ser: ta.Any) -> T:
        raise NotImplementedError


class _DataclassFieldSerde(dc.Pure):
    cls: ta.Any
    ignore_if: ta.Optional[ta.Callable[[ta.Any], bool]] = dc.field(None, kwonly=True)


SubclassMap = ta.Mapping[ta.Union[str, type], ta.Union[type, str]]  # FIXME: gross


_DataclassFieldSerdeMap = ta.Mapping[str, _DataclassFieldSerde]


class _SerdeState(dc.Pure):

    serdes_by_cls: ta.MutableMapping[type, Serde] = dc.field(
        default_factory=weakref.WeakKeyDictionary)

    subclass_map_resolvers_by_cls: ta.MutableMapping[type, ta.Callable[[type], SubclassMap]] = dc.field(
        default_factory=weakref.WeakKeyDictionary)

    subclass_maps_by_cls: ta.MutableMapping[type, SubclassMap] = dc.field(
        default_factory=weakref.WeakKeyDictionary)

    is_monomorphic_dataclass_by_cls: ta.MutableMapping[type, bool] = dc.field(
        default_factory=weakref.WeakKeyDictionary)

    field_type_maps_by_dataclass: ta.MutableMapping[type, _DataclassFieldSerdeMap] = dc.field(
        default_factory=weakref.WeakKeyDictionary)


_STATE = _SerdeState()


def serde_for(*clss):
    def inner(obj):
        if isinstance(obj, type):
            sd = obj()
        else:
            sd = obj
        check.isinstance(sd, Serde)
        for c in clss:
            check.not_in(c, _STATE.serdes_by_cls)
            _STATE.serdes_by_cls[c] = sd
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


def subclass_map_resolver_for(*clss):
    def inner(fn):
        check.callable(fn)
        for c in clss:
            check.not_in(c, _STATE.subclass_map_resolvers_by_cls)
            _STATE.subclass_map_resolvers_by_cls[c] = fn
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
        if lang.Abstract not in cur.__bases__:
            n = None
            if dc.is_dataclass(cur):
                n = dc.metadatas_dict(cur).get(Name)
                if callable(n):
                    n = n(cur)
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
        return _STATE.subclass_maps_by_cls[cls]
    except KeyError:
        try:
            bld = _STATE.subclass_map_resolvers_by_cls[cls]
        except KeyError:
            bld = build_subclass_map
        dct = _STATE.subclass_maps_by_cls[cls] = bld(cls)
        return dct


def _is_monomorphic_dataclass(cls: type) -> bool:
    try:
        return _STATE.is_monomorphic_dataclass_by_cls[cls]
    except KeyError:
        scm = get_subclass_map(cls)
        scmcls = {k: v for k, v in scm.items() if isinstance(k, type)}
        ret = False
        if len(scmcls) == 1 and list(scmcls) == [cls] and lang.Final in cls.__bases__:
            ret = True
        _STATE.is_monomorphic_dataclass_by_cls[cls] = ret
        return ret


def _get_dataclass_field_type_map(dcls: type) -> _DataclassFieldSerdeMap:
    if not isinstance(dcls, type) or not dc.is_dataclass(dcls):
        raise TypeError(dcls)
    try:
        return _STATE.field_type_maps_by_dataclass[dcls]
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
        _STATE.field_type_maps_by_dataclass[dcls] = dct
        return dct


def serialize_dataclass_fields(obj: T) -> Serialized:
    ser = {}
    for fn, fs in _get_dataclass_field_type_map(type(obj)).items():
        v = getattr(obj, fn)
        if fs.ignore_if is not None and fs.ignore_if(v):
            continue
        ser[fn] = serialize(v, spec=rfl.spec(fs.cls))
    return ser


def serialize_dataclass(obj: T, *, spec: ta.Optional[rfl.Spec] = None, no_custom: bool = False) -> Serialized:
    custom = _STATE.serdes_by_cls.get(type(obj)) if not no_custom else None
    if custom is not None:
        if custom.handles_dataclass_polymorphism:
            return custom.serialize(obj)
        ser = custom.serialize(obj)
    else:
        ser = serialize_dataclass_fields(obj)
    if isinstance(spec, rfl.TypeSpec) and spec.erased_cls is type(obj) and _is_monomorphic_dataclass(spec.erased_cls):
        return ser
    else:
        scm = get_subclass_map(type(obj))
        return {check.isinstance(scm[type(obj)], str): ser}


def serialize(obj: T, spec: ta.Optional[ta.Any] = None) -> Serialized:
    spec = rfl.spec(spec if spec is not None else type(obj))

    if isinstance(spec, rfl.UnionSpec) and spec.optional_arg is not None:
        if obj is None:
            return None
        spec = spec.optional_arg

    if not isinstance(spec, rfl.TypeSpec):
        raise TypeError(spec)

    spec = check.isinstance(spec, rfl.TypeSpec)

    if dc.is_dataclass(spec.erased_cls):
        return serialize_dataclass(obj, spec=spec)

    elif spec.erased_cls in _STATE.serdes_by_cls:
        serde = _STATE.serdes_by_cls[spec.erased_cls]
        return serde.serialize(obj)

    elif issubclass(spec.erased_cls, collections.abc.Mapping):
        if isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Mapping:
            kspec, vspec = spec.args
        else:
            kspec = vspec = None
        return [[serialize(k, spec=kspec), serialize(v, spec=vspec)] for k, v in obj.items()]

    elif issubclass(spec.erased_cls, (collections.abc.Sequence, collections.abc.Set)) and not issubclass(spec.erased_cls, str):  # noqa
        if isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Sequence:
            [espec] = spec.args
        else:
            espec = None
        return [serialize(e, spec=espec) for e in obj]

    elif issubclass(spec.erased_cls, enum.Enum):
        return obj.name

    elif isinstance(obj, PRIMITIVE_TYPES_TUPLE):
        return obj

    else:
        raise TypeError(obj)


def deserialize_dataclass_fields(ser: ta.Mapping[str, ta.Any], dcls: type) -> T:
    check.isinstance(ser, ta.Mapping)
    fdct = _get_dataclass_field_type_map(dcls)
    kw = {}
    for k, v in ser.items():
        try:
            fs = fdct[k]
        except KeyError:
            raise
        kw[k] = deserialize(v, fs.cls)
    try:
        return dcls(**kw)
    except Exception as e:  # noqa
        raise


def deserialize_dataclass(ser: Serialized, cls: type, *, no_custom: bool = False) -> T:
    oser = ser  # noqa
    custom = _STATE.serdes_by_cls.get(cls) if not no_custom else None
    if custom is not None and custom.handles_dataclass_polymorphism:
        return custom.deserialize(ser)
    if _is_monomorphic_dataclass(cls):
        dcls = cls
    else:
        [[n, ser]] = check.isinstance(ser, ta.Mapping).items()
        dcls = check.isinstance(get_subclass_map(cls)[n], type)
    custom = _STATE.serdes_by_cls.get(dcls) if not no_custom else None
    if custom is not None:
        return custom.deserialize(ser)
    else:
        return deserialize_dataclass_fields(ser, dcls)


def _deserialize(ser: Serialized, spec: rfl.Spec) -> T:
    if isinstance(spec, rfl.UnionSpec) and spec.optional_arg is not None:
        if ser is None:
            return None
        spec = spec.optional_arg

    if isinstance(spec, rfl.TypeSpec) and dc.is_dataclass(spec.erased_cls):
        return deserialize_dataclass(ser, spec.erased_cls)

    elif isinstance(spec, rfl.TypeSpec) and spec.erased_cls in _STATE.serdes_by_cls:
        serde = _STATE.serdes_by_cls[spec.erased_cls]
        return serde.deserialize(ser)

    elif isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Mapping:
        [kspec, vspec] = spec.args
        dct = {}
        if isinstance(ser, str):
            raise TypeError(ser)
        elif isinstance(ser, collections.abc.Mapping):
            for kser, vser in ser.items():
                k, v = deserialize(kser, kspec), deserialize(vser, vspec)
                if k in dct:
                    raise KeyError(k)
                dct[k] = v
        elif isinstance(ser, collections.abc.Sequence):
            for e in ser:
                if not isinstance(e, collections.abc.Sequence) or isinstance(e, str):
                    raise TypeError(e)
                kser, vser = e
                k, v = deserialize(kser, kspec), deserialize(vser, vspec)
                if k in dct:
                    raise KeyError(k)
                dct[k] = v
        else:
            raise TypeError(ser)
        return dct

    elif isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Set:
        [espec] = spec.args
        return {deserialize(e, espec) for e in ser}

    elif isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Sequence:
        [espec] = spec.args
        if not isinstance(ser, collections.abc.Sequence) or isinstance(ser, str):
            raise TypeError(ser)
        return [deserialize(e, espec) for e in ser]

    elif isinstance(spec, rfl.SpecialParameterizedGenericTypeSpec) and spec.erased_cls is collections.abc.Callable:
        if not callable(ser):
            raise TypeError(ser)
        return ser

    elif not isinstance(spec, rfl.NonGenericTypeSpec):
        raise TypeError(spec)

    elif issubclass(spec.erased_cls, enum.Enum):
        if isinstance(ser, str):
            return spec.erased_cls.__members__[ser]
        else:
            raise TypeError(ser)

    elif spec.erased_cls in PRIMITIVE_TYPES:
        if isinstance(ser, spec.erased_cls):
            return ser
        elif isinstance(ser, str):
            return spec.erased_cls(ser)
        else:
            raise TypeError(ser)

    else:
        raise TypeError(spec)


class DeserializationException(Exception):

    def __init__(self, *args, spec: ta.Any, ser: Serialized) -> None:
        super().__init__(*args)

        self.spec = spec
        self.ser = ser

    defs.basic('args', 'spec', 'ser')

    def __str__(self) -> str:
        return repr(self)


_NO_RERAISE = False
# _NO_RERAISE = True


def deserialize(ser: Serialized, spec: ta.Any, no_reraise: bool = False) -> T:
    spec = rfl.spec(spec)
    if no_reraise or _NO_RERAISE:
        return _deserialize(ser, spec)
    else:
        try:
            return _deserialize(ser, spec)
        except Exception as e:
            raise DeserializationException(spec=spec, ser=ser) from e
