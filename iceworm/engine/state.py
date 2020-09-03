"""
TODO:
 - * decree: multitenant out the gate - allows mvcc shit *
 - just gen from dc's
  - data is serde'd json, marked fields are cols, indexes added from class metadata
 - refs table?
  - want gc
   - no constraints but offline?
 - composite pk, world_id (just world?), auto-added when querying, prefixed in indices
  - composite pk anyway below that - 'implicit' pk components?
  - state.PrimaryKey([str]), state.Index([str])
 - _meta: revision, host, pid - same as query tags, likely more - world info
 - dc anns like nodal/serde, ignored for heap
 - atom? running txns?

tables:
 - worlds
 - targets
  - one per type?
  - invalidations?
   - ranges?
   - historical invalidations? pending? handled? cleared at max interval according to scheds?
"""
import abc
import typing as ta

from omnibus import check
from omnibus import lang

from ..utils import unique_dict


StrMap = ta.Mapping[str, ta.Any]
Key = StrMap
KeyTup = ta.Sequence[ta.Any]
Obj = ta.Any
ObjCls = ta.Type[Obj]


class ObjMapper:

    def __init__(self, cls: ObjCls, key_fields: ta.Sequence[str]) -> None:
        super().__init__()

        self._cls = check.isinstance(cls, type)
        self._key_fields = [check.isinstance(f, str) for f in check.not_isinstance(key_fields, str)]
        self._key_fields_set = set(self._key_fields)

    @property
    def cls(self) -> ObjCls:
        return self._cls

    @property
    def key_fields(self) -> ta.Sequence[str]:
        return self._key_fields

    def obj_to_key_tup(self, obj: Obj) -> KeyTup:
        if type(obj) is not self._cls:
            raise TypeError(obj, self._cls)
        return tuple(getattr(obj, f) for f in self._key_fields)

    def obj_to_key(self, obj: Obj) -> Key:
        if type(obj) is not self._cls:
            raise TypeError(obj, self._cls)
        return {f: getattr(obj, f) for f in self._key_fields}

    def key_to_key_tup(self, key: Key) -> KeyTup:
        if set(key) != self._key_fields_set:
            raise KeyError(key, self._key_fields_set)
        return tuple(key[f] for f in self._key_fields)


class ObjStore(lang.Abstract):

    @abc.abstractmethod
    def key(self, obj: Obj) -> Key:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, cls: ObjCls, key: Key) -> Obj:
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, obj: ObjCls) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, cls: ObjCls, key: Key) -> None:
        raise NotImplementedError


class HeapObjStore(ObjStore):

    def __init__(self, mappers: ta.Iterable[ObjMapper]) -> None:
        super().__init__()

        self._mappers_by_cls = unique_dict((sm.cls, sm) for sm in mappers for _ in [check.isinstance(sm, ObjMapper)])
        self._objs_by_key_tup_by_cls: ta.Dict[ta.Dict[KeyTup, Obj]] = {}

    def key(self, obj: Obj) -> Key:
        return self._mappers_by_cls[type(obj)].obj_to_key(obj)

    def get(self, cls: ObjCls, key: Key) -> Obj:
        kt = self._mappers_by_cls[cls].key_to_key_tup(key)
        return check.isinstance(self._objs_by_key_tup_by_cls[cls][kt], cls)

    def put(self, obj: ObjCls) -> None:
        cls = type(obj)
        kt = self._mappers_by_cls[cls].obj_to_key_tup(obj)
        self._objs_by_key_tup_by_cls.setdefault(cls, {})[kt] = obj

    def delete(self, cls: ObjCls, key: Key) -> None:
        kt = self._mappers_by_cls[cls].key_to_key_tup(key)
        del self._objs_by_key_tup_by_cls[cls][kt]


class SqlObjStore(ObjStore):

    class Adapter(lang.Abstract):
        pass

    class PostgresAdapter(Adapter):
        pass

    def __init__(self, adapter: Adapter) -> None:
        super().__init__()

        self._adapter = check.isinstance(adapter, SqlObjStore.Adapter)

    def key(self, obj: Obj) -> Key:
        raise NotImplementedError

    def get(self, cls: ObjCls, key: Key) -> Obj:
        raise NotImplementedError

    def put(self, obj: ObjCls) -> None:
        raise NotImplementedError

    def delete(self, cls: ObjCls, key: Key) -> None:
        raise NotImplementedError
