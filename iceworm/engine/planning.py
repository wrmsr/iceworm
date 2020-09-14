"""
TODO:
 -
"""
import typing as ta

from omnibus import check
from omnibus import collections as ocol
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

    def plan(self, invalidated_tables: ta.Iterable[els.Id] = None) -> ops.Op:
        invalidated_tables = {check.isinstance(t, els.Id) for t in check.not_isinstance(invalidated_tables, str)}
        plan = []

        tbl_qn_sets_by_id = {}
        for mat in self._elements.get_type_set(tars.Materialization):
            tbl_qn_sets_by_id.setdefault(mat.table.id, set()).add(QualifiedName([mat.connector.id, *mat.name]))

        for ele in self._elements.get_type_set(tars.Table):
            if ele.id not in invalidated_tables:
                continue
            for dst in tbl_qn_sets_by_id.get(ele.id, []):
                ctr = self._ctors[dst[0]]
                if not isinstance(ctr, ctrs.impls.sql.SqlConnector):
                    continue
                mdt = check.isinstance(ele.md, md.Table)
                plan.extend([
                    ops.DropTable(dst),
                    ops.CreateTable(dc.replace(mdt, name=dst)),
                ])

        row_sets_by_table_id = {}
        for ele in self._elements.get_type_set(tars.Rows):
            row_sets_by_table_id.setdefault(ele.table.id, ocol.IdentitySet()).add(ele)

        table_deps = {
            ele.table.id: set(tars.get_table_deps(ele).name_sets_by_table_id)
            for ele in self._elements.get_type_set(tars.Rows)
        }

        topo = [id for step in ocol.toposort(table_deps) for id in sorted(step)]
        for tbl_id in topo:
            if tbl_id not in invalidated_tables:
                continue
            for rows in row_sets_by_table_id.get(tbl_id, []):
                for dst in tbl_qn_sets_by_id.get(rows.table.id, []):
                    plan.append(ops.InsertIntoSelect(dst, rows.query))

        return ops.List(plan)
