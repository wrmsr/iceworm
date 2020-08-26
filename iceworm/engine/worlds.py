import contextlib
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from . import connectors as ctrs
from .. import metadata as md
from ..types import QualifiedName
from ..utils import seq


class Materialization(dc.Pure):
    name: ta.Optional[QualifiedName] = dc.field(coerce=QualifiedName.of)


class View(dc.Pure):
    table: md.Table = dc.field(check=lambda o: isinstance(o, md.Table))
    query: str = dc.field(check=lambda o: isinstance(o, str))
    materializations: ta.Sequence[Materialization] = dc.field(
        (), coerce=seq, check=lambda l: all(isinstance(o, Materialization) for o in l))


class World:

    def __init__(self, connectors: ctrs.ConnectorSet) -> None:
        super().__init__()

        self._ctors = check.isinstance(connectors, ctrs.ConnectorSet)

        self._views_by_name: ta.MutableMapping[QualifiedName, View] = {}

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
