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
    def handles_polymorphism(self) -> bool:
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


class DeserializationException(Exception):

    def __init__(self, *args, spec: ta.Any, ser: Serialized) -> None:
        super().__init__(*args)

        self.spec = spec
        self.ser = ser

    defs.basic('args', 'spec', 'ser')

    def __str__(self) -> str:
        return repr(self)


class _SerdeState:

    def __init__(self) -> None:
        super().__init__()

        self._priority_serde_gens: ta.MutableSequence[SerdeGen] = []
        self._serde_gens: ta.MutableSequence[SerdeGen] = []
        self._serdes_by_cls: ta.MutableMapping[type, Serde] = weakref.WeakKeyDictionary()

    def register_serde(self, cls: type, serde: Serde) -> None:
        check.isinstance(cls, type)
        check.isinstance(serde, Serde)
        check.not_in(cls, self._serdes_by_cls)
        self._serdes_by_cls[cls] = serde

    def get_serde(self, cls: type) -> ta.Optional[Serde]:
        check.isinstance(cls, type)
        try:
            return self._serdes_by_cls[cls]
        except KeyError:
            return None

    def register_serde_gen(self, serde_gen: SerdeGen, priority: bool = False) -> None:
        check.isinstance(serde_gen, SerdeGen)
        if priority:
            self._priority_serde_gens.append(serde_gen)
        else:
            self._serde_gens.append(serde_gen)

    def get_serde_gen(self, spec: ta.Any) -> ta.Optional[SerdeGen]:
        spec = rfl.spec(spec)
        for g in self._priority_serde_gens:
            if g.match(spec):
                return g
        matches = [g for g in self._serde_gens if g.match(spec)]
        if matches:
            return check.single(matches)
        else:
            return None

    def serializer(self, spec: ta.Optional[ta.Any]) -> Serializer:
        spec = rfl.spec(spec)
        gen = self.get_serde_gen(spec)
        if gen is not None:
            return gen.serializer(spec)
        raise TypeError(spec)

    def serialize(self, obj: T, spec: ta.Optional[ta.Any] = None) -> Serialized:
        return self.serializer(spec if spec is not None else type(obj))(obj)

    def deserializer(self, spec: ta.Any) -> Deserializer:
        spec = rfl.spec(spec)
        gen = self.get_serde_gen(spec)
        if gen is not None:
            return gen.deserializer(spec)
        raise TypeError(spec)

    _NO_RERAISE = False
    # _NO_RERAISE = True

    def deserialize(self, ser: Serialized, spec: ta.Any, no_reraise: bool = False) -> T:
        spec = rfl.spec(spec)
        if no_reraise or self._NO_RERAISE:
            return self.deserializer(spec)(ser)
        else:
            try:
                return self.deserializer(spec)(ser)
            except Exception as e:
                raise DeserializationException(spec=spec, ser=ser) from e


_STATE = _SerdeState()


def serde_for(*clss):
    def inner(obj):
        if isinstance(obj, type):
            sd = obj()
        else:
            sd = obj
        for c in clss:
            _STATE.register_serde(c, sd)
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


def serde_gen(*, priority: bool = False):
    def inner(obj):
        if isinstance(obj, type):
            sd = obj()
        else:
            sd = obj
        _STATE.register_serde_gen(sd, priority=priority)
        return obj
    return inner


class AutoSerdeGen(SerdeGen, lang.Abstract):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        check.state(cls.__bases__ == (AutoSerdeGen,))
        serde_gen()(cls)


get_serde = _STATE.get_serde
get_serde_gen = _STATE.get_serde_gen
serializer = _STATE.serializer
serialize = _STATE.serialize
deserializer = _STATE.deserializer
deserialize = _STATE.deserialize
