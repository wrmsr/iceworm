import typing as ta
import weakref

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import reflect as rfl

from .serde import deserializer
from .serde import Deserializer
from .serde import get_serde
from .serde import serde_gen
from .serde import SerdeGen
from .serde import Serialized
from .serde import serializer
from .serde import Serializer


T = ta.TypeVar('T')


class Ignore(lang.Marker):
    pass


class GetType(lang.Marker):
    pass


class Name(lang.Marker):
    pass


class Aliases(lang.Marker):
    pass


class _DataclassFieldSerde(dc.Pure):
    cls: ta.Any
    ignore_if: ta.Optional[ta.Callable[[ta.Any], bool]] = dc.field(None, kwonly=True)


SubclassMap = ta.Mapping[ta.Union[str, type], ta.Union[type, str]]  # FIXME: gross


_DataclassFieldSerdeMap = ta.Mapping[str, _DataclassFieldSerde]


class _DataclassSerdeState(dc.Pure):

    subclass_map_resolvers_by_cls: ta.MutableMapping[type, ta.Callable[[type], SubclassMap]] = dc.field(
        default_factory=weakref.WeakKeyDictionary)

    subclass_maps_by_cls: ta.MutableMapping[type, SubclassMap] = dc.field(
        default_factory=weakref.WeakKeyDictionary)

    is_monomorphic_dataclass_by_cls: ta.MutableMapping[type, bool] = dc.field(
        default_factory=weakref.WeakKeyDictionary)

    field_type_maps_by_dataclass: ta.MutableMapping[type, _DataclassFieldSerdeMap] = dc.field(
        default_factory=weakref.WeakKeyDictionary)

    # serializers_by_cls: ta.MutableMapping[type, Serializer] = dc.field(
    #     default_factory=weakref.WeakKeyDictionary)

    # deserializers_by_cls: ta.MutableMapping[type, Deserializer] = dc.field(
    #     default_factory=weakref.WeakKeyDictionary)


_STATE = _DataclassSerdeState()


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
            ignore_if = None
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


def dataclass_fields_serializer(cls: type) -> Serializer:
    sers = {}
    for fn, fs in _get_dataclass_field_type_map(cls).items():
        sers[fn] = (fs, serializer(fs.cls))
    def ser(obj):  # noqa
        dct = {}
        for fn, (fs, fser) in sers.items():
            v = getattr(obj, fn)
            if fs.ignore_if is not None and fs.ignore_if(v):
                continue
            dct[fn] = fser(v)
        return dct
    return ser


def serialize_dataclass_fields(obj: T) -> Serialized:
    return dataclass_fields_serializer(type(obj))(obj)


def dataclass_serializer(cls: type, no_custom: bool = False) -> Serializer:
    custom = get_serde(cls) if not no_custom else None
    if custom is not None and custom.handles_polymorphism:
        return custom.serialize

    if _is_monomorphic_dataclass(cls):
        return custom.serialize if custom is not None else dataclass_fields_serializer(cls)

    scm = {}
    for scls, snam in get_subclass_map(cls).items():
        if not isinstance(scls, type):
            continue

        custom = get_serde(scls) if not no_custom else None
        if custom is not None and custom.handles_polymorphism:
            ser = custom.serialize
        else:
            sser = custom.serialize if custom is not None else dataclass_fields_serializer(scls)
            ser = (lambda snam, sser: lambda obj: {snam: sser(obj)})(snam, sser)

        scm[scls] = ser

    return lambda obj: scm[type(obj)](obj)


def serialize_dataclass(obj: T, cls: ta.Optional[type] = None, *, no_custom: bool = False) -> Serialized:
    return dataclass_serializer(cls if cls is not None else type(obj), no_custom=no_custom)(obj)


def dataclass_fields_deserializer(dcls: type) -> Deserializer:
    fdct = _get_dataclass_field_type_map(dcls)
    desers = {fn: deserializer(fs.cls) for fn, fs in fdct.items()}

    def des(ser):
        check.isinstance(ser, ta.Mapping)
        kw = {}
        for k, v in ser.items():
            fd = desers[k]
            kw[k] = fd(v)
        try:
            return dcls(**kw)
        except Exception as e:  # noqa
            raise

    return des


def deserialize_dataclass_fields(ser: ta.Mapping[str, ta.Any], dcls: type) -> T:
    return dataclass_fields_deserializer(dcls)(ser)


def dataclass_deserializer(cls: type, *, no_custom: bool = False) -> Deserializer:
    custom = get_serde(cls) if not no_custom else None
    if custom is not None and custom.handles_polymorphism:
        return custom.deserialize

    if _is_monomorphic_dataclass(cls):
        return custom.deserialize if custom is not None else dataclass_fields_deserializer(cls)

    scm = {}
    for scls, snam in get_subclass_map(cls).items():
        if not isinstance(scls, type):
            continue

        custom = get_serde(scls) if not no_custom else None
        scm[snam] = custom.deserialize if custom is not None else dataclass_fields_deserializer(scls)

    def des(ser):
        [[n, ser]] = check.isinstance(ser, ta.Mapping).items()
        return scm[n](ser)

    return des


def deserialize_dataclass(ser: Serialized, cls: type, *, no_custom: bool = False) -> T:
    return dataclass_deserializer(cls, no_custom=no_custom)(ser)


@serde_gen(priority=True)
class DataclassSerdeGen(SerdeGen):

    def match(self, spec: rfl.Spec) -> bool:
        return isinstance(spec, rfl.TypeSpec) and dc.is_dataclass(spec.erased_cls)

    def serializer(self, spec: rfl.Spec) -> Serializer:
        return lambda obj: serialize_dataclass(obj, spec.erased_cls)

    def deserializer(self, spec: rfl.Spec) -> Deserializer:
        return lambda ser: deserialize_dataclass(ser, spec.erased_cls)
