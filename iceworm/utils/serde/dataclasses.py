import typing as ta
import weakref

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import reflect as rfl

from .serde import deserialize
from .serde import deserializer
from .serde import get_serde
from .serde import serialize
from .serde import Serialized
from .serde import serializer


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


def dataclass_fields_serializer(cls: type) -> Serialized:
    sers = {}
    for fn, fs in _get_dataclass_field_type_map(cls).items():
        sers[fn] = (fs, serializer(rfl.spec(fs.cls)))
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


def serialize_dataclass(obj: T, *, spec: ta.Optional[rfl.Spec] = None, no_custom: bool = False) -> Serialized:
    custom = get_serde(type(obj)) if not no_custom else None
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
    custom = get_serde(cls) if not no_custom else None
    if custom is not None and custom.handles_dataclass_polymorphism:
        return custom.deserialize(ser)
    if _is_monomorphic_dataclass(cls):
        dcls = cls
    else:
        [[n, ser]] = check.isinstance(ser, ta.Mapping).items()
        dcls = check.isinstance(get_subclass_map(cls)[n], type)
    custom = get_serde(dcls) if not no_custom else None
    if custom is not None:
        return custom.deserialize(ser)
    else:
        return deserialize_dataclass_fields(ser, dcls)
