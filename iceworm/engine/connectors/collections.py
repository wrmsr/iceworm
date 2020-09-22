"""
TODO:
 - lifecycle
"""
import typing as ta

from omnibus import check
from omnibus import collections as ocol

from .. import elements as els
from ... import metadata as md
from ...types import QualifiedName
from ...utils import set_dict
from ...utils import unique_dict
from .base import Connection
from .base import Connector
from .mirrors import Mirror


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


class ConnectionSet(ta.Iterable[Connection], Mirror):

    def __init__(self, ctors: ConnectorSet) -> None:
        super().__init__()

        self._ctors = check.isinstance(ctors, ConnectorSet)

        self._conns_by_ctor: ta.MutableMapping[Connector, Connection] = ocol.IdentityKeyDict()

    @property
    def connectors(self) -> ConnectorSet:
        return self._ctors

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

    def reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        qns_by_cn = set_dict(names, lambda qn: qn[0], lambda qn: qn[1:])
        ret = {}
        for cn, qns in qns_by_cn.items():
            conn = self[cn]
            objs = conn.reflect(qns)
            ret.update({QualifiedName([cn, *k]): v for k, v in objs.items()})
        return ret

    def close(self) -> None:
        for conn in self._conns_by_ctor.values():
            conn.close()
