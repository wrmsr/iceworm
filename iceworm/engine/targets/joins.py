import typing as ta

from omnibus import properties

from .. import elements as els
from .reflect import TableDependenciesProcessor
from .reflect import get_rows_table_deps
from .targets import Materialization
from .targets import Rows
from .targets import Table


class JoinSplittingProcessor(els.InstanceElementProcessor):

    @classmethod
    def dependencies(cls) -> ta.Iterable[ta.Type[els.ElementProcessor]]:
        return {*super().dependencies(), TableDependenciesProcessor}

    class Instance(els.InstanceElementProcessor.Instance['JoinSplittingProcessor']):

        # @properties.cached
        # def matches(self) -> ta.Iterable[els.Element]:
        #     return [
        #         e
        #         for e in self.input.get_type_set(Rows)
        #         for deps in [get_rows_table_deps(e)]
        #         for table_id in deps.name_sets_by_table_id
        #         for
        #     ]

        @properties.cached
        def output(self) -> ta.Iterable[els.Element]:
            pass
