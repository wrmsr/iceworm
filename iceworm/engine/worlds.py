import contextlib
import typing as ta

from omnibus import check

from . import connectors as ctrs
from . import targets as tars
from .. import metadata as md
from ..types import QualifiedName


class World:

    def __init__(self, ctors: ta.Iterable[ctrs.Connector], targets: ta.Iterable[tars.Target]) -> None:
        super().__init__()

        self._ctors = ctrs.ConnectorSet.of(ctors)
        self._targets = tars.TargetSet.of(targets)

        self._views_by_name: ta.MutableMapping[QualifiedName, View] = {}

    @property
    def ctors(self) -> ctrs.ConnectorSet:
        return self._ctors

    @property
    def targets(self) -> tars.TargetSet:
        return self._targets

    def reflect(self, name: QualifiedName) -> ta.Sequence[md.Object]:
        objs = []

        if len(name) > 1 and name[0] in self._ctors:
            ctor = self._ctors[name[0]]
            with contextlib.closing(ctor.connect()) as conn:
                connobjs = conn.reflect([QualifiedName(name[1:])])
                if connobjs:
                    objs.append(check.single(connobjs.values()))

        for ctor in self._ctors:
            with contextlib.closing(ctor.connect()) as conn:
                connobjs = conn.reflect([name])
                if connobjs:
                    objs.extend(connobjs.values())

        return objs
