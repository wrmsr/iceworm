import typing as ta
import weakref

from omnibus import check
from omnibus import lang
from omnibus import reflect as rfl

from .serde import AutoSerdeGen
from .types import Deserializer
from .types import Serde
from .types import Serializer


T = ta.TypeVar('T')


class _SimpleSerdeState:

    def __init__(self) -> None:
        super().__init__()

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


_STATE = _SimpleSerdeState()


get_serde = _STATE.get_serde


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


class SimpleSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.TypeSpec) and get_serde(spec.erased_cls) is not None

    def serializer(self, spec: rfl.Spec) -> Serializer:
        serde = get_serde(spec.erased_cls)
        return lambda obj: serde.serialize(obj)

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        serde = get_serde(spec.erased_cls)
        return lambda ser: serde.deserialize(ser)
