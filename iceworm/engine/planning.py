import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from . import connectors as ctrs
from . import elements as els
from . import ops
from . import targets as tars
from .. import metadata as md
from ..types import QualifiedName


class ElementPlanner:

    def __init__(
            self,
            elements: ta.Iterable[els.Element],
            ctors: ta.Iterable[ctrs.Connector],
    ) -> None:
        super().__init__()

        self._elements = els.ElementSet.of(elements)
        self._ctors = ctrs.ConnectorSet.of(ctors)

    @property
    def elements(self) -> els.ElementSet:
        return self._elements

    @property
    def ctors(self) -> ctrs.ConnectorSet:
        return self._ctors

    def plan(self, invalidated_tables: ta.Iterable[QualifiedName] = None) -> ops.Op:
        invalidated_tables = {check.isinstance(t, QualifiedName) for t in invalidated_tables}
        plan = []

        for ele in self._elements:
            if isinstance(ele, tars.Table):
                if ele.name in invalidated_tables:
                    mdt = check.isinstance(ele.md, md.Table)
                    plan.extend([
                        ops.DropTable(ele.name),
                        ops.CreateTable(dc.replace(mdt, name=ele.name)),
                    ])

            elif isinstance(ele, tars.Rows):
                if ele.table in invalidated_tables:
                    plan.append(ops.InsertIntoSelect(ele.table, ele.query))

        return ops.List(plan)
