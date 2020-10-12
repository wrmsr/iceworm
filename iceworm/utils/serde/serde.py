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


Serializer = ta.Callable[[T],  Serialized]
Deserializer = ta.Callable[[Serialized], T]


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


class SerdeGen(lang.Abstract):

    @abc.abstractmethod
    def match(self, spec: rfl.Spec) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def serializer(self, spec: rfl.Spec) -> Serializer:
        raise NotImplementedError

    @abc.abstractmethod
    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        raise NotImplementedError


class _SerdeState(dc.Pure):

    serde_gens: ta.MutableSequence[SerdeGen] = dc.field(
        default_factory=list)

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


def serde_gen(obj):
    if isinstance(obj, type):
        sd = obj()
    else:
        sd = obj
    check.isinstance(sd, SerdeGen)
    _STATE.serde_gens.append(sd)
    return obj


class AutoSerdeGen(SerdeGen, lang.Abstract):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        check.state(cls.__bases__ == (AutoSerdeGen,))
        serde_gen(cls)


class OptionalSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.UnionSpec) and spec.optional_arg is not None

    def serializer(self, spec: rfl.Spec) -> Serializer:
        eser = serializer(spec.optional_arg)
        return lambda obj: None if obj is None else eser(obj)

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        edes = deserializer(spec.optional_arg)
        return lambda ser: None if ser is None else edes(ser)


class AnySerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.AnySpec)

    def serializer(self, spec: rfl.Spec) -> Serializer:
        def ser(obj):
            if isinstance(obj, PRIMITIVE_TYPES_TUPLE):
                return obj
            else:
                raise TypeError(obj)
        return ser

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        def des(ser):
            if isinstance(ser, PRIMITIVE_TYPES_TUPLE):
                return ser
            else:
                raise TypeError(ser)
        return des


class DataclassSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.TypeSpec) and dc.is_dataclass(spec.erased_cls)

    def serializer(self, spec: rfl.Spec) -> Serializer:
        from .dataclasses import serialize_dataclass
        return lambda obj: serialize_dataclass(obj, spec.erased_cls)

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        from .dataclasses import deserialize_dataclass
        return lambda ser: deserialize_dataclass(ser, spec.erased_cls)


class CustomSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.TypeSpec) and spec.erased_cls in _STATE.serdes_by_cls

    def serializer(self, spec: rfl.Spec) -> Serializer:
        serde = _STATE.serdes_by_cls[spec.erased_cls]
        return lambda obj: serde.serialize(obj)

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        serde = _STATE.serdes_by_cls[spec.erased_cls]
        return lambda ser: serde.deserialize(ser)


def serializer(spec: ta.Optional[ta.Any]) -> Serializer:
    spec = rfl.spec(spec)

    for sg in _STATE.serde_gens:
        if sg.match(spec):
            return sg.serializer(spec)

    if isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Mapping:
        kspec, vspec = spec.args
        kser, vser = serializer(kspec), serializer(vspec)
        return lambda obj: [[kser(k), vser(v)] for k, v in obj.items()]

    if (
            isinstance(spec, rfl.GenericTypeSpec) and
            spec.erased_cls in (collections.abc.Sequence, collections.abc.Set)
    ):
        [espec] = spec.args
        eser = serializer(espec)
        return lambda obj: [eser(e) for e in obj]

    if isinstance(spec, rfl.TupleTypeSpec):
        esers = [serializer(e) for e in spec.args]
        def ser(obj):  # noqa
            if not isinstance(obj, tuple) or len(obj) != esers:
                raise TypeError(obj)
            return[s(e) for s, e in zip(esers, obj)]
        return ser

    if issubclass(spec.erased_cls, enum.Enum):
        return lambda obj: obj.name

    if issubclass(spec.erased_cls, PRIMITIVE_TYPES_TUPLE):
        return lambda obj: obj

    raise TypeError(spec)


def serialize(obj: T, spec: ta.Optional[ta.Any] = None) -> Serialized:
    return serializer(spec if spec is not None else type(obj))(obj)


def deserializer(spec: ta.Any) -> Deserializer:
    spec = rfl.spec(spec)

    for sg in _STATE.serde_gens:
        if sg.match(spec):
            return sg.deserializer(spec)

    if isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Mapping:
        [kspec, vspec] = spec.args
        kdes, vdes = deserializer(kspec), deserializer(vspec)
        def des(ser):  # noqa
            dct = {}
            if isinstance(ser, str):
                raise TypeError(ser)
            elif isinstance(ser, collections.abc.Mapping):
                for kser, vser in ser.items():
                    k, v = kdes(kser), vdes(vser)
                    if k in dct:
                        raise KeyError(k)
                    dct[k] = v
            elif isinstance(ser, collections.abc.Sequence):
                for e in ser:
                    if not isinstance(e, collections.abc.Sequence) or isinstance(e, str):
                        raise TypeError(e)
                    kser, vser = e
                    k, v = kdes(kser), vdes(vser)
                    if k in dct:
                        raise KeyError(k)
                    dct[k] = v
            else:
                raise TypeError(ser)
            return dct
        return des

    if isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Set:
        [espec] = spec.args
        edes = deserializer(espec)
        return lambda ser: {edes(e) for e in ser}

    if isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Sequence:
        [espec] = spec.args
        edes = deserializer(espec)
        def des(ser):  # noqa
            if not isinstance(ser, collections.abc.Sequence) or isinstance(ser, str):
                raise TypeError(ser)
            return [edes(e) for e in ser]
        return des

    if isinstance(spec, rfl.TupleTypeSpec):
        edess = [serializer(e) for e in spec.args]
        def des(ser):  # noqa
            if isinstance(ser, str) or len(ser) != edess:
                raise TypeError(ser)
            return[d(e) for d, e in zip(edess, ser)]
        return des

    if isinstance(spec, rfl.SpecialParameterizedGenericTypeSpec) and spec.erased_cls is collections.abc.Callable:
        return lambda ser: check.callable(ser)

    if not isinstance(spec, rfl.NonGenericTypeSpec):
        raise TypeError(spec)

    if isinstance(spec, rfl.TypeSpec) and issubclass(spec.erased_cls, enum.Enum):
        return lambda ser: spec.erased_cls.__members__[check.isinstance(ser, str)]

    if isinstance(spec, rfl.TypeSpec) and spec.erased_cls in PRIMITIVE_TYPES:
        def des(ser):
            if isinstance(ser, spec.erased_cls):
                return ser
            elif isinstance(ser, str):
                return spec.erased_cls(ser)
            else:
                raise TypeError(ser)
        return des

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
        return deserializer(spec)(ser)
    else:
        try:
            return deserializer(spec)(ser)
        except Exception as e:
            raise DeserializationException(spec=spec, ser=ser) from e
