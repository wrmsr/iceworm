import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties

from .. import elements as els
from .reflect import ReflectReferencedTablesProcessor
from .reflect import TableDependenciesAnalysis
from .targets import Rows
from .targets import Table


class JoinSplittingProcessor(els.InstanceElementProcessor):

    @classmethod
    def cls_dependencies(cls) -> ta.Iterable[ta.Type[els.ElementProcessor]]:
        return {*super().cls_dependencies(), ReflectReferencedTablesProcessor}

    class Instance(els.InstanceElementProcessor.Instance['JoinSplittingProcessor']):

        @properties.cached
        def connector_ids_by_rows(self) -> els.ElementMap[Rows, ta.AbstractSet[els.Id]]:
            return els.ElementMap(
                (e, cids)
                for e in self.input.get_type_set(Rows)
                for deps in [self.input.analyze(TableDependenciesAnalysis)[e]]
                for cids in [{qn[0] for qns in deps.name_sets_by_table.values() for qn in qns}]
            )

        @properties.cached
        def matches(self) -> ta.Iterable[els.Element]:
            return [e for e, cids in self.connector_ids_by_rows.items() if len(cids) > 1]

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

        def split_join(self, ele: Rows) -> ta.Sequence[els.Element]:
            return [ele]
