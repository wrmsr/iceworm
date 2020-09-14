import typing as ta

from omnibus import properties

from .. import elements as els
from .reflect import ReflectReferencedTablesProcessor
from .reflect import TableDependenciesAnalysis
from .targets import Rows
from .targets import Table


class JoinSplittingProcessor(els.InstanceElementProcessor):

    @classmethod
    def dependencies(cls) -> ta.Iterable[ta.Type[els.ElementProcessor]]:
        return {*super().dependencies(), ReflectReferencedTablesProcessor}

    class Instance(els.InstanceElementProcessor.Instance['JoinSplittingProcessor']):

        @properties.cached
        def matches(self) -> ta.Iterable[els.Element]:
            # return [
            #     e
            #     for e in self.input.get_type_set(Rows)
            #     for deps in [self.input.analyze(TableDependenciesAnalysis)[e]]
            #     for tdeps in [set(deps.name_sets_by_table)]
            #     for deptbls in [[check.isinstance(self.input[i], Table) for i in tdeps]]
            #     for cids in [{t. for t in deptbls}]
            # ]
            raise NotImplementedError

        @properties.cached
        def output(self) -> ta.Iterable[els.Element]:
            raise NotImplementedError
