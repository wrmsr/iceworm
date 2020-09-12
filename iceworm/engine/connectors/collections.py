import typing as ta

from omnibus import check
from omnibus import collections as ocol

from .. import elements as els
from ...utils import unique_dict
from .base import Connector
from .base import Connection


class ConnectorSet(ta.Iterable[Connector]):

    def __init__(self, ctors: ta.Iterable[Connector]) -> None:
        super().__init__()

        self._ctors = [check.isinstance(e, Connector) for e in ctors]

        self._ctors_by_id: ta.Mapping[els.Id, Connector] = unique_dict((c.id, c) for c in self._ctors)

    @classmethod
    def of(cls, it: ta.Iterable[ta.Union[Connector, Connector.Config]]) -> 'ConnectorSet':
        if isinstance(it, cls):
            return it
        else:
            return cls((Connector.of(o) for o in it))

    def __iter__(self) -> ta.Iterator[Connector]:
        return iter(self._ctors)

    def __contains__(self, id: els.Id) -> bool:
        return check.isinstance(id, els.Id) in self._ctors_by_id

    def __getitem__(self, id: els.Id) -> Connector:
        return self._ctors_by_id[check.isinstance(id, els.Id)]

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

    def __contains__(self, id: els.Id) -> bool:
        check.isinstance(id, els.Id)
        try:
            ctor = self._ctors[id]
        except KeyError:
            return False
        return ctor in self._conns_by_ctor

    def __getitem__(self, id: els.Id) -> Connection:
        ctor = self._ctors[check.isinstance(id, els.Id)]
        try:
            return self._conns_by_ctor[ctor]
        except KeyError:
            conn = self._conns_by_ctor[ctor] = ctor.connect()
            return conn

    def close(self) -> None:
        for conn in self._conns_by_ctor.values():
            conn.close()
