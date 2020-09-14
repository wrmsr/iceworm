import typing as ta

from omnibus import code as ocode
from omnibus import dataclasses as dc
from omnibus import properties

from .base import Element
from .base import Origin
from .processing import InstanceElementProcessor


class IdGeneratorProcessor(InstanceElementProcessor):

    class Instance(InstanceElementProcessor.Instance['IdGeneratorProcessor']):

        @properties.cached
        @property
        def name_gen(self) -> ocode.NameGenerator:
            return ocode.name_generator(unavailable_names=set(self.input.by_id))

        @properties.cached
        def matches(self) -> ta.Iterable[Element]:
            return [e for e in self.input if e.id is None]

        @properties.cached
        def output(self) -> ta.Iterable[Element]:
            return [
                dc.replace(
                    e,
                    id=self.name_gen(f'_{type(e).__name__}_'),
                    meta={Origin: Origin(e)},
                )
                if e.id is None else e
                for e in self.input
            ]
