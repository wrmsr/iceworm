"""
TODO:
 - glaring unresolved ambiguity between selecting from mats and tbls

table -> invalidation -> rows -> refresh -> ...
  |
  V
materializations
"""
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties

from .. import connectors as ctrs
from .. import elements as els
from .. import ops
from .. import targets as tars
from ... import metadata as md
from ...trees import rendering as ren
from ...types import QualifiedName
from ..utils import parse_simple_select_table
from ..utils import parse_simple_select_tables


class PlanningElementProcessor(els.InstanceElementProcessor):

    def __init__(
            self,
            ctors: ctrs.ConnectorSet,
    ) -> None:
        super().__init__()

        self._ctors = check.isinstance(ctors, ctrs.ConnectorSet)

    @classmethod
    def phases(cls) -> ta.Iterable[els.Phase]:
        return [els.Phases.PLAN]

    @property
    def ctors(self) -> ctrs.ConnectorSet:
        return self._ctors

    class Instance(els.InstanceElementProcessor.Instance['PlanningElementProcessor']):

        @properties.cached
        @property
        def matches(self) -> ta.Iterable[els.Element]:
            return [
                e
                for e in self.input.get_type_set(tars.Target)
                if self.owner not in e.meta.get(els.ProcessedBy, els.ProcessedBy.EMPTY).processors
            ]

        def _build_rows_op(self, rows: tars.Rows, dst: QualifiedName) -> ops.Op:
            query = ren.render_query(rows.query)

            try:
                src_name = parse_simple_select_table(query, star=True)
            except ValueError:
                pass
            else:
                src_query = f"select * from {'.'.join(src_name[1:])}"
                return ops.InsertIntoSelect(dst, src_name[0], src_query)

            try:
                tbl_names = parse_simple_select_tables(query)
                if tbl_names:
                    raise ValueError
            except ValueError:
                pass
            else:
                return ops.InsertIntoEval(dst, query)

            raise ValueError(rows)

        @properties.stateful_cached
        @property
        def output(self) -> ta.Iterable[els.Element]:
            plan = []

            tbl_qn_sets_by_id = {}
            for mat in self.input.get_type_set(tars.Materialization):
                tbl_qn_sets_by_id.setdefault(mat.table.id, set()).add(QualifiedName([mat.connector.id, *mat.name]))

            for ele in self.input.get_type_set(tars.Table):
                for dst in tbl_qn_sets_by_id.get(ele.id, []):
                    ctr = self.owner._ctors[dst[0]]
                    if not isinstance(ctr, ctrs.impls.sql.SqlConnector):
                        continue
                    mdt = check.isinstance(ele.md, md.Table)
                    plan.extend([
                        ops.DropTable(dst),
                        ops.CreateTable(dc.replace(mdt, name=dst)),
                    ])

            row_sets_by_table_id = {}
            for ele in self.input.get_type_set(tars.Rows):
                row_sets_by_table_id.setdefault(ele.table.id, ocol.IdentitySet()).add(ele)

            table_deps = {
                ele.table.id: {
                    e.id
                    for e in self.input.analyze(tars.StrictTableDependenciesAnalysis)[ele].name_sets_by_table
                }
                for ele in self.input.get_type_set(tars.Rows)
            }

            topo = [id for step in ocol.toposort(table_deps) for id in sorted(step)]
            for tbl_id in topo:
                for rows in row_sets_by_table_id.get(tbl_id, []):
                    for dst in tbl_qn_sets_by_id.get(rows.table.id, []):
                        plan.append(self._build_rows_op(rows, dst))

            # return ops.List(plan)
            raise NotImplementedError
