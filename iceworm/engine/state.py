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
 - codec? for heap referential vs serialized
 - move dc mapping to utils, generalize out - historical state can stay here

tables:
 - worlds
 - elements
  - one per type?
  - invalidations?
   - ranges?
   - historical invalidations? pending? handled? cleared at max interval according to scheds?
"""
import abc
import collections.abc
import typing as ta

from omnibus import check
from omnibus import collections as col
from omnibus import lang
import sqlalchemy as sa

from ..utils import serde


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


class ObjMappers(ta.Iterable[ObjMapper]):

    def __init__(self, mappers: ta.Iterable[ObjMapper]) -> None:
        super().__init__()

        self._mappers_by_cls = col.unique_dict((sm.cls, sm) for sm in mappers for _ in [check.isinstance(sm, ObjMapper)])  # noqa

    @classmethod
    def of(cls, obj: ta.Union['ObjMappers', ta.Iterable[ObjMapper]]) -> 'ObjMappers':
        if isinstance(obj, ObjMappers):
            return obj
        elif isinstance(obj, collections.abc.Iterable):
            return cls(obj)
        else:
            raise TypeError(obj)

    def __iter__(self) -> ta.Iterator[ObjMapper]:
        return iter(self._mappers_by_cls.values())

    def __getitem__(self, cls: ObjCls) -> ObjMapper:
        return self._mappers_by_cls[check.isinstance(cls, type)]

    def key(self, obj: Obj) -> Key:
        return self[type(obj)].obj_to_key(obj)


class ObjStore(lang.Abstract):

    def __init__(self, mappers: ta.Iterable[ObjMapper]) -> None:
        super().__init__()

        self._mappers = ObjMappers.of(mappers)

    @property
    def mappers(self) -> ObjMappers:
        return self._mappers

    def key(self, obj: Obj) -> Key:
        return self._mappers.key(obj)

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
        super().__init__(mappers)

        self._objs_by_key_tup_by_cls: ta.Dict[ta.Dict[KeyTup, Obj]] = {}

    def get(self, cls: ObjCls, key: Key) -> Obj:
        kt = self._mappers[cls].key_to_key_tup(key)
        return check.isinstance(serde.deserialize(self._objs_by_key_tup_by_cls[cls][kt], cls), cls)

    def put(self, obj: ObjCls) -> None:
        cls = type(obj)
        kt = self._mappers[cls].obj_to_key_tup(obj)
        self._objs_by_key_tup_by_cls.setdefault(cls, {})[kt] = serde.serialize(obj)

    def delete(self, cls: ObjCls, key: Key) -> None:
        kt = self._mappers[cls].key_to_key_tup(key)
        del self._objs_by_key_tup_by_cls[cls][kt]


class SqlObjStore(ObjStore):

    class Adapter:
        pass

    class PostgresAdapter(Adapter):
        pass

    def __init__(
            self,
            mappers: ta.Iterable[ObjMapper],
            conn: sa.engine.Connection,
            adapter: Adapter = Adapter(),
    ) -> None:
        super().__init__(mappers)

        self._conn = check.isinstance(conn, sa.engine.Connection)
        self._adapter = check.isinstance(adapter, SqlObjStore.Adapter)

    def get(self, cls: ObjCls, key: Key) -> Obj:
        raise NotImplementedError

    def put(self, obj: ObjCls) -> None:
        raise NotImplementedError

    def delete(self, cls: ObjCls, key: Key) -> None:
        raise NotImplementedError
