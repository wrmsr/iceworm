import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import properties

from .. import elements as els
from ... import metadata as md
from ...trees import transforms as ttfm
from ...types import QualifiedName
from .reflect import ReflectReferencedTablesProcessor
from .reflect import StrictTableDependenciesAnalysis
from .targets import Materialization
from .targets import Rows
from .targets import Table


class JoinSplittingProcessor(els.InstanceElementProcessor):

    @classmethod
    def cls_dependencies(cls) -> ta.Iterable[ta.Type[els.Dependable]]:
        return {
            *super().cls_dependencies(),

            # FIXME: real dep is StrictTableDependenciesAnalysis, remove when driver understands analysis deps
            ReflectReferencedTablesProcessor,

            StrictTableDependenciesAnalysis,
        }

    class Instance(els.InstanceElementProcessor.Instance['JoinSplittingProcessor']):

        @properties.cached
        def src_connector_ids_by_rows(self) -> els.ElementMap[Rows, ta.AbstractSet[els.Id]]:
            return els.ElementMap(
                (e, cids)
                for e in self.input.get_type_set(Rows)
                for deps in [self.input.analyze(StrictTableDependenciesAnalysis).by_rows[e]]
                for cids in [{qn[0] for qns in deps.name_sets_by_table.values() for qn in qns}]
            )

        @properties.cached
        def matches(self) -> ta.Iterable[els.Element]:
            return [e for e, cids in self.src_connector_ids_by_rows.items() if len(cids) > 1]

        @properties.cached
        def output(self) -> ta.Iterable[els.Element]:
            lst = []
            for e in self.input:
                if e in self.matches:
                    lst.extend(
                        dc.replace(ne, meta={els.Origin: els.Origin(e)})
                        for ne in self.split_join(e)
                    )
                else:
                    lst.append(e)
            return lst

        def split_join(self, rows: Rows) -> ta.Sequence[els.Element]:
            ret = []
            stda = self.input.analyze(StrictTableDependenciesAnalysis)
            dst_qn = check.single(stda.name_sets_by_table[rows.table])
            src_qns = {check.single(ns) for ns in stda.by_rows[rows].name_sets_by_table.values()}
            for src_qn in src_qns:
                if src_qn[0] == dst_qn[0]:
                    continue
                src_tbl = stda.tables_by_name[src_qn]
                new_qn = QualifiedName([dst_qn[0], '__' + src_qn[1]])
                new_tbl = Table(
                    '/'.join(new_qn),
                    md=dc.replace(
                        check.isinstance(src_tbl.md, md.Table),
                        name=new_qn[1:],
                    ),
                )
                ret.extend([
                    new_tbl,
                    Rows(new_tbl, f'select * from {src_qn.dotted}'),
                    Materialization(new_tbl, dst_qn[0], [new_qn[1]]),
                ])
                rows = dc.replace(
                    rows,
                    query=ttfm.ReplaceNamesTransformer({src_qn: new_qn})(rows.query.root),
                    meta={els.Origin: els.Origin(rows)},
                )
            return [rows, *ret]
