from omnibus import check
from omnibus import inject as inj

from . import infer
from . import reflect
from .. import elements as els


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    els.inject.bind_element_processor(binder, infer.InferTableProcessor, els.Phases.TARGETS)
    els.inject.bind_element_processor(binder, reflect.ReflectReferencedTablesProcessor, els.Phases.TARGETS)
    els.inject.bind_element_processor(binder, reflect.ReflectTablesProcessor, els.Phases.TARGETS)

    return binder
