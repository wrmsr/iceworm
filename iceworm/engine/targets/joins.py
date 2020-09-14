import typing as ta

from omnibus import properties

from .. import elements as els
from .reflect import TableDependenciesProcessor


class JoinSplittingProcessor(els.InstanceElementProcessor):

    @classmethod
    def dependencies(cls) -> ta.Iterable[ta.Type[els.ElementProcessor]]:
        return {*super().dependencies(), TableDependenciesProcessor}

    class Instance(els.InstanceElementProcessor.Instance['JoinSplittingProcessor']):

        @properties.cached
        def matches(self) -> ta.Iterable[els.Element]:
            raise NotImplementedError

        @properties.cached
        def output(self) -> ta.Iterable[els.Element]:
            raise NotImplementedError
