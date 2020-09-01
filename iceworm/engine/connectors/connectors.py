"""
TODO:
 - virtual vs physical tables
 - physical tables requiring refresh
 - incremental vs total physical tables
 - materialized vs unmaterialized virtuals
 - ** dataclass interop ** - dc->tbl, query
  - just return object refs? jsonize?
  - support snowflake json garbage on objects

Def conns:
 - sql - snow + pg (+ incl internal state storage pg, 'self')
 - kafka
 - dynamo
 - system - conns, nodes, running ops, etc
 - mongo
 - redis

Alt conns:
 - salesforce
 - pagerduty
 - jira
 - gsheets
 - slack
 - github
"""
import abc
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import defs
from omnibus import lang

from ... import metadata as md
from ...types import QualifiedName
from ...utils import unique_dict


ConnectorT = ta.TypeVar('ConnectorT')

Row = ta.Mapping[str, ta.Any]
RowGen = ta.Generator[Row, None, None]


class RowSource(lang.Abstract):

    @abc.abstractmethod
    def produce_rows(self) -> RowGen:
        raise NotImplementedError


class RowSink(lang.Abstract):

    @abc.abstractmethod
    def consume_rows(self, rows: ta.Iterable[Row]) -> None:
        raise NotImplementedError


class Connector(lang.Abstract, ta.Generic[ConnectorT]):

    def __init__(self, name: str) -> None:
        super().__init__()

        self._name = check.not_empty(check.isinstance(name, str))

    defs.repr('name')

    @property
    def name(self) -> str:
        return self._name

    def close(self) -> None:
        pass

    @abc.abstractmethod
    def connect(self) -> 'Connection[ConnectorT]':
        raise NotImplementedError


class Connection(lang.Abstract, ta.Generic[ConnectorT]):

    def __init__(self, ctor: ConnectorT) -> None:
        super().__init__()

        self._ctor: ConnectorT = check.isinstance(ctor, Connector)

        self._reflect_cache: ta.MutableMapping[QualifiedName, ta.Optional[md.Object]] = {}

    defs.repr('ctor')

    @property
    def ctor(self) -> ConnectorT:
        return self._ctor

    def close(self) -> None:
        pass

    @abc.abstractmethod
    def create_row_source(self, query: str) -> RowSource:
        raise NotImplementedError

    @abc.abstractmethod
    def create_row_sink(self, table: QualifiedName) -> RowSink:
        raise NotImplementedError

    def reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        if names is not None:
            check.not_isinstance(names, (str, QualifiedName))
            ret = {}
            missing = set()

            for name in names:
                check.isinstance(name, QualifiedName)
                try:
                    obj = self._reflect_cache[name]
                except KeyError:
                    missing.add(name)
                else:
                    if obj is not None:
                        ret[name] = obj

            if missing:
                new = self._reflect(missing)
                for name, obj in new.items():
                    check.not_in(name, ret)
                    check.not_in(name, self._reflect_cache)
                    ret[name] = self._reflect_cache[name] = obj

            return ret

        else:
            raise NotImplementedError

    @abc.abstractmethod
    def _reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        raise NotImplementedError


class ConnectorSet(ta.Iterable[Connector]):

    def __init__(self, ctors: ta.Iterable[Connector]) -> None:
        super().__init__()

        self._ctors = [check.isinstance(e, Connector) for e in ctors]

        self._ctors_by_name: ta.Mapping[str, Connector] = unique_dict((c.name, c) for c in self._ctors)

    @classmethod
    def of(cls, it: ta.Iterable[Connector]) -> 'ConnectorSet':
        if isinstance(it, cls):
            return it
        else:
            return cls(it)

    def __iter__(self) -> ta.Iterator[Connector]:
        return iter(self._ctors)

    def __contains__(self, name: str) -> bool:
        return check.isinstance(name, str) in self._ctors_by_name

    def __getitem__(self, name: str) -> Connector:
        return self._ctors_by_name[check.isinstance(name, str)]

    def close(self) -> None:
        for ctor in self._ctors:
            ctor.close()


class ConnectionSet(ta.Iterable[Connection]):

    def __init__(self, ctors: ConnectorSet) -> None:
        super().__init__()

        self._ctors = check.isinstance(ctors, ConnectorSet)

        self._conns_by_ctor: ta.MutableMapping[Connector, Connection] = ocol.IdentityKeyDict()

    def __iter__(self) -> ta.Iterator[Connection]:
        return iter(self._conns_by_ctor.values())

    def __contains__(self, name: str) -> bool:
        check.isinstance(name, str)
        try:
            ctor = self._ctors[name]
        except KeyError:
            return False
        return ctor in self._conns_by_ctor

    def __getitem__(self, name: str) -> Connection:
        ctor = self._ctors[check.isinstance(name, str)]
        try:
            return self._conns_by_ctor[ctor]
        except KeyError:
            conn = self._conns_by_ctor[ctor] = ctor.connect()
            return conn

    def close(self) -> None:
        for conn in self._conns_by_ctor.values():
            conn.close()
