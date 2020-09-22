"""
TODO:
 - glaring unresolved ambiguity between selecting from mats and tbls
 - ** NOT NECESSARILY FORCED TO REFRESH ALL MATERIALIZATIONS TOGETHER... **
 - baked anns? materializations <-> rows?

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
from .elements import Materializer


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
        def matches(self) -> ta.AbstractSet[els.Element]:
            matr_mat_ids = {matr.target.id for matr in self.input.get_type_set(Materializer)}
            return ocol.IdentitySet([
                mat
                for mat in self.input.get_type_set(tars.Materialization)
                if mat.id not in matr_mat_ids
            ])

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
            rows_sets_by_table_id = {}
            for rows in self.input.get_type_set(tars.Rows):
                rows_sets_by_table_id.setdefault(rows.table.id, ocol.IdentitySet()).add(rows)

            mat_sets_by_table_id = {}
            for mat in self.input.get_type_set(tars.Materialization):
                mat_sets_by_table_id.setdefault(mat.table.id, ocol.IdentitySet()).add(mat)

            ret = list(self.input)
            for mat in self.input.get_type_set(tars.Materialization):
                ctr = self.owner._ctors[mat.connector.id]
                if not isinstance(ctr, ctrs.impls.sql.SqlConnector):
                    # FIXME: lol
                    matr = Materializer(mat, [], ops.List([]))
                    ret.append(matr)
                    continue

                dst = QualifiedName([mat.connector.id, *mat.name])
                tbl = self.input[mat.table]
                mdt = check.isinstance(tbl.md, md.Table)
                plan = [
                    ops.DropTable(dst),
                    ops.CreateTable(dc.replace(mdt, name=dst)),
                ]

                srcs: ta.Set[els.Id] = set()
                for rows in rows_sets_by_table_id.get(mat.table.id, []):
                    plan.append(self._build_rows_op(rows, dst))
                    for src_tbl in self.input.analyze(tars.StrictTableDependenciesAnalysis).by_rows[rows].name_sets_by_table:  # noqa
                        for src_mat in mat_sets_by_table_id.get(src_tbl.id):
                            srcs.add(src_mat.id)

                matr = Materializer(mat, srcs, ops.List(plan))
                ret.append(matr)

            return ret
