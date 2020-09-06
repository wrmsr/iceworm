import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from . import connectors as ctrs
from . import elements as els
from . import ops
from . import targets as tars
from .. import metadata as md


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

    def plan(self, invalidated_tables: ta.Iterable[els.Id] = None) -> ops.Op:
        invalidated_tables = {check.isinstance(t, els.Id) for t in check.not_isinstance(invalidated_tables, str)}
        plan = []

        tbl_qn_sets_by_id = {}
        for mat in self._elements.get_element_type_set(tars.Materialization):
            tbl_qn_sets_by_id.setdefault(mat.table.id, set()).add(mat.dst)

        for ele in self._elements:
            if isinstance(ele, tars.Table):
                if ele.id in invalidated_tables:
                    for dst in tbl_qn_sets_by_id.get(ele.id, []):
                        ctr = self._ctors[dst[0]]
                        if not isinstance(ctr, ctrs.sql.SqlConnector):
                            continue
                        mdt = check.isinstance(ele.md, md.Table)
                        plan.extend([
                            ops.DropTable(dst),
                            ops.CreateTable(dc.replace(mdt, name=dst)),
                        ])

            elif isinstance(ele, tars.Rows):
                if ele.table.id in invalidated_tables:
                    for dst in tbl_qn_sets_by_id.get(ele.table.id, []):
                        plan.append(ops.InsertIntoSelect(dst, ele.query))

        return ops.List(plan)
