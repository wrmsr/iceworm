"""
TODO:
 - ** (serializers|deserializers)_by_spec
 - strict mode
 - replace with builtin omni generic impl
 - extensible serde Contexts? want pluggable datatypes, -> Datatype.of
 - recursive custom serde?
 - allow_empty? system: {{}}
"""
import typing as ta
import weakref

from omnibus import check
from omnibus import lang
from omnibus import reflect as rfl

from .types import DeserializationException
from .types import Deserializer
from .types import SerdeGen
from .types import Serialized
from .types import Serializer


T = ta.TypeVar('T')


class _SerdeState:

    def __init__(self) -> None:
        super().__init__()

        self._priority_serde_gens: ta.MutableSequence[SerdeGen] = []
        self._serde_gens: ta.MutableSequence[SerdeGen] = []

        self._serializers_by_spec: ta.MutableMapping[rfl.Spec, Serializer] = weakref.WeakKeyDictionary()
        self._deserializers_by_spec: ta.MutableMapping[rfl.Spec, Deserializer] = weakref.WeakKeyDictionary()

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

        try:
            return self._serializers_by_spec[spec]
        except KeyError:
            pass

        gen = self.get_serde_gen(spec)
        if gen is None:
            raise TypeError(spec)

        ser = gen.serializer(spec)
        self._serializers_by_spec[spec] = ser
        return ser

    def serialize(self, obj: T, spec: ta.Optional[ta.Any] = None) -> Serialized:
        return self.serializer(spec if spec is not None else type(obj))(obj)

    def deserializer(self, spec: ta.Any) -> Deserializer:
        spec = rfl.spec(spec)

        try:
            return self._deserializers_by_spec[spec]
        except KeyError:
            pass

        gen = self.get_serde_gen(spec)
        if gen is None:
            raise TypeError(spec)

        des = gen.deserializer(spec)

        self._deserializers_by_spec[spec] = des
        return des

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


get_serde_gen = _STATE.get_serde_gen
serializer = _STATE.serializer
serialize = _STATE.serialize
deserializer = _STATE.deserializer
deserialize = _STATE.deserialize
