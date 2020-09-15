from omnibus import code as ocode
from omnibus import properties

from .processing import Analysis


class IdGen(Analysis):
    @properties.cached
    @property
    def name_gen(self) -> ocode.NameGenerator:
        return ocode.name_generator(unavailable_names=set(self.elements.by_id))

    def __call__(self, prefix: str = '') -> str:
        return self.name_gen(prefix)
