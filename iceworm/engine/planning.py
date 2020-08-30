import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import properties

from . import connectors as ctrs
from . import ops
from . import targets as tars
from .. import metadata as md


class TargetPlanner:

    def __init__(
            self,
            targets: ta.Iterable[tars.Target],
            ctors: ta.Iterable[ctrs.Connector],
    ) -> None:
        super().__init__()

        self._targets = tars.TargetSet.of(targets)
        self._ctors = ctrs.ConnectorSet.of(ctors)

    @property
    def targets(self) -> tars.TargetSet:
        return self._targets

    @property
    def ctors(self) -> ctrs.ConnectorSet:
        return self._ctors

    @properties.cached
    def plan(self) -> ops.Op:
        plan = []

        for tar in self._targets:
            if isinstance(tar, tars.Table):
                mdt = check.isinstance(tar.md, md.Table)
                plan.extend([
                    ops.DropTable(tar.name),
                    ops.CreateTable(dc.replace(mdt, name=tar.name)),
                ])
            elif isinstance(tar, tars.Rows):
                plan.append(ops.InsertIntoSelect(tar.table, tar.query))

        return ops.List(plan)
