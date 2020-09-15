import typing as ta

from omnibus import dataclasses as dc
from omnibus import properties

from .analyses import IdGen
from .base import Element
from .base import Origin
from .processing import InstanceElementProcessor


class IdGeneratorProcessor(InstanceElementProcessor):

    class Instance(InstanceElementProcessor.Instance['IdGeneratorProcessor']):

        @properties.cached
        def matches(self) -> ta.Iterable[Element]:
            return [e for e in self.input if e.id is None]

        @properties.cached
        def output(self) -> ta.Iterable[Element]:
            ng = self.input.analyze(IdGen).name_gen
            return [
                dc.replace(
                    e,
                    id=ng(f'_{type(e).__name__}_'),
                    meta={Origin: Origin(e)},
                )
                if e.id is None else e
                for e in self.input
            ]
