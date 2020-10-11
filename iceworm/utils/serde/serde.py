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


class _SerdeState(dc.Pure):

    serdes_by_cls: ta.MutableMapping[type, Serde] = dc.field(
        default_factory=weakref.WeakKeyDictionary)


_STATE = _SerdeState()


def get_serde(cls: type) -> ta.Optional[Serde]:
    check.isinstance(cls, type)
    try:
        return _STATE.serdes_by_cls[cls]
    except KeyError:
        return None


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
        from .dataclasses import serialize_dataclass
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


def _deserialize(ser: Serialized, spec: rfl.Spec) -> T:
    if isinstance(spec, rfl.UnionSpec) and spec.optional_arg is not None:
        if ser is None:
            return None
        spec = spec.optional_arg

    if isinstance(spec, rfl.TypeSpec) and dc.is_dataclass(spec.erased_cls):
        from .dataclasses import deserialize_dataclass
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
