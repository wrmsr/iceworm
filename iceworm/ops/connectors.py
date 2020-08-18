"""
TODO:
 - virtual vs physical tables
 - physical tables requiring refresh
 - incremental vs total physical tables
 - materialized vs unmaterialized virtuals

Def conns:
 - kafka
 - dynamo
 - system
 - mongo

Alt conns:
 - salesforce
 - pagerduty
 - jira
"""
import abc
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import defs
from omnibus import lang

from ..types import QualifiedName
from ..utils import unique_dict


ConnectorT = ta.TypeVar('ConnectorT')

Row = ta.Mapping[str, ta.Any]
RowGen = ta.Generator[Row, None, None]


class RowSpec(dc.Enum):
    pass


class TableRowSpec(RowSpec):
    table: QualifiedName = dc.field(coerce=QualifiedName.of)


class QueryRowSpec(RowSpec):
    query: str


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

    def __init__(self, connector: ConnectorT) -> None:
        super().__init__()

        self._connector: ConnectorT = check.isinstance(connector, Connector)

    @property
    def connector(self) -> ConnectorT:
        return self._connector

    def close(self) -> None:
        pass

    @abc.abstractmethod
    def create_row_source(self, spec: RowSpec) -> RowSource:
        raise NotImplementedError

    @abc.abstractmethod
    def create_row_sink(self, table: QualifiedName) -> RowSink:
        raise NotImplementedError


class ConnectorSet(ta.Iterable[Connector]):

    def __init__(self, connectors: ta.Iterable[Connector]) -> None:
        super().__init__()

        self._connectors = list(connectors)
        self._connectors_by_name = unique_dict((c.name, c) for c in self._connectors)

    def __iter__(self) -> ta.Iterator[Connector]:
        return iter(self._connectors)

    def __getitem__(self, name: str) -> Connector:
        return self._connectors_by_name[name]

    def close(self) -> None:
        for ctor in self._connectors:
            ctor.close()


class ConnectionSet(ta.Iterable[Connection]):

    def __init__(self, connectors: ConnectorSet) -> None:
        super().__init__()

        self._connectors = check.isinstance(connectors, ConnectorSet)
        self._connections_by_connector: ta.MutableMapping[Connector, Connection] = ocol.IdentityKeyDict()

    def __iter__(self) -> ta.Iterator[Connection]:
        return iter(self._connections_by_connector.values())

    def __getitem__(self, name: str) -> Connection:
        ctor = self._connectors[name]
        try:
            return self._connections_by_connector[ctor]
        except KeyError:
            conn = self._connections_by_connector[ctor] = ctor.connect()
            return conn

    def close(self) -> None:
        for conn in self._connections_by_connector.values():
            conn.close()
