import collections.abc
import enum

from omnibus import check
from omnibus import reflect as rfl

from .serde import AutoSerdeGen
from .serde import deserializer
from .serde import serializer
from .types import Deserializer
from .types import PRIMITIVE_TYPES_TUPLE
from .types import Serializer


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


class MappingSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Mapping

    def serializer(self, spec: rfl.Spec) -> Serializer:
        kspec, vspec = spec.args
        kser, vser = serializer(kspec), serializer(vspec)
        return lambda obj: [[kser(k), vser(v)] for k, v in obj.items()]

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
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


class SequenceSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Sequence

    def serializer(self, spec: rfl.Spec) -> Serializer:
        [espec] = spec.args
        eser = serializer(espec)
        return lambda obj: [eser(e) for e in obj]

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        [espec] = spec.args
        edes = deserializer(espec)
        def des(ser):  # noqa
            if not isinstance(ser, collections.abc.Sequence) or isinstance(ser, str):
                raise TypeError(ser)
            return [edes(e) for e in ser]
        return des


class SetSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.GenericTypeSpec) and spec.erased_cls is collections.abc.Set

    def serializer(self, spec: rfl.Spec) -> Serializer:
        [espec] = spec.args
        eser = serializer(espec)
        return lambda obj: [eser(e) for e in obj]

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        [espec] = spec.args
        edes = deserializer(espec)
        return lambda ser: {edes(e) for e in ser}


class TupleSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.TupleTypeSpec)

    def serializer(self, spec: rfl.Spec) -> Serializer:
        esers = [serializer(e) for e in spec.args]
        def ser(obj):  # noqa
            if not isinstance(obj, tuple) or len(obj) != esers:
                raise TypeError(obj)
            return[s(e) for s, e in zip(esers, obj)]
        return ser

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        edess = [deserializer(e) for e in spec.args]
        def des(ser):  # noqa
            if isinstance(ser, str) or len(ser) != edess:
                raise TypeError(ser)
            return[d(e) for d, e in zip(edess, ser)]
        return des


class EnumSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.NonGenericTypeSpec) and issubclass(spec.erased_cls, enum.Enum)

    def serializer(self, spec: rfl.Spec) -> Serializer:
        return lambda obj: obj.name

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        return lambda ser: spec.erased_cls.__members__[check.isinstance(ser, str)]


class PrimitiveSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.NonGenericTypeSpec) and issubclass(spec.erased_cls, PRIMITIVE_TYPES_TUPLE)

    def serializer(self, spec: rfl.Spec) -> Serializer:
        return lambda obj: obj

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        def des(ser):
            if isinstance(ser, spec.erased_cls):
                return ser
            elif isinstance(ser, str):
                return spec.erased_cls(ser)
            else:
                raise TypeError(ser)
        return des


class CallableSerdeGen(AutoSerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return (
                isinstance(spec, rfl.SpecialParameterizedGenericTypeSpec)
                and spec.erased_cls is collections.abc.Callable
        )

    def serializer(self, spec: rfl.Spec) -> Serializer:
        raise TypeError

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        return lambda ser: check.callable(ser)
