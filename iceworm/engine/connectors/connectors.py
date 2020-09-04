"""
TODO:
 - ** are conn confs TARGETS? **
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
import weakref

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import defs
from omnibus import lang

from ... import metadata as md
from ...types import QualifiedName
from ...utils import serde
from ...utils import unique_dict
from ...utils.nodal import NodalDataclass

ConnectorT = ta.TypeVar('ConnectorT', bound='Connector')
ConnectorConfigT = ta.TypeVar('ConnectorConfigT', bound='Connector.Config')

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


class ListRowSource(RowSource):

    def __init__(self, rows: ta.Iterable[Row]) -> None:
        super().__init__()

        self._rows = list(rows)

    @property
    def rows(self) -> ta.List[Row]:
        return self._rows

    def produce_rows(self) -> RowGen:
        yield from self._rows


class ListRowSink(RowSink):

    def __init__(self, rows: ta.Optional[ta.List[Row]] = None) -> None:
        super().__init__()

        self._rows = rows if rows is not None else []

    @property
    def rows(self) -> ta.List[Row]:
        return self._rows

    def __iter__(self) -> ta.Iterator[Row]:
        return iter(self._rows)

    def consume_rows(self, rows: ta.Iterable[Row]) -> None:
        self._rows.extend(rows)


class Connector(lang.Abstract, ta.Generic[ConnectorT, ConnectorConfigT]):

    class Config(dc.Enum, NodalDataclass['Connector.Config']):

        @classmethod
        def _nodal_cls(cls) -> ta.Type['Connector.Config']:
            return Connector.Config

        def __init_subclass__(cls, **kwargs) -> None:
            super().__init_subclass__(**kwargs)

            check.state(cls.__name__ == 'Config')
            ocn, _ = cls.__qualname__.split('.')
            check.state(ocn.endswith('Connector'))

        name: str = dc.field(check=lambda s: isinstance(s, str) and s)

    CLS_MAP: ta.Mapping[str, ta.Type['Connector']] = weakref.WeakValueDictionary()
    CONFIG_CLS_MAP: ta.Mapping[ta.Type[Config], ta.Type['Connector']] = weakref.WeakValueDictionary()

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        if lang.Abstract not in cls.__bases__:
            check.state(cls.__name__.endswith('Connector'))
            n = check.not_empty(lang.decamelize(cls.__name__[:-9]))
            check.not_in(n, Connector.CLS_MAP)
            cfcls = check.issubclass(cls.Config, Connector.Config)
            check.not_in(cfcls, Connector.CONFIG_CLS_MAP)
            Connector.CLS_MAP[n] = cls
            Connector.CONFIG_CLS_MAP[cfcls] = cls

    def __init__(self, config: ConnectorConfigT) -> None:
        super().__init__()

        self._config: ConnectorConfigT = check.isinstance(config, Connector.Config)

    defs.repr('name')

    @property
    def config(self) -> ConnectorConfigT:
        return self._config

    @property
    def name(self) -> str:
        return self._config.name

    def close(self) -> None:
        pass

    @abc.abstractmethod
    def connect(self) -> 'Connection[ConnectorT]':
        raise NotImplementedError

    @classmethod
    def of(cls, obj: ta.Union['Connector', Config]) -> 'Connector':
        if isinstance(obj, Connector):
            return obj
        elif isinstance(obj, Connector.Config):
            return cls.CONFIG_CLS_MAP[type(obj)](obj)
        else:
            raise TypeError(obj)


@serde.subclass_map_resolver_for(Connector.Config)
def _build_connector_config_subclass_map(cls: type) -> ta.Mapping[ta.Union[str, type], ta.Union[str, type]]:
    check.state(cls is Connector.Config)
    dct = {}
    for n, ccls in Connector.CLS_MAP.items():
        cfcls = check.issubclass(ccls.Config, Connector.Config)
        dct[n] = cfcls
        dct[cfcls] = n
    return dct


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
    def of(cls, it: ta.Iterable[ta.Union[Connector, Connector.Config]]) -> 'ConnectorSet':
        if isinstance(it, cls):
            return it
        else:
            return cls((Connector.of(o) for o in it))

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
