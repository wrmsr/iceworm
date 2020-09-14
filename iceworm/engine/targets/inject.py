from omnibus import check
from omnibus import inject as inj

from .. import elements as els
from .infer import InferTableProcessor
from .reflect import ReflectReferencedTablesProcessor


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    els.inject.bind_element_processor(binder, InferTableProcessor, els.Phases.TARGETS)
    els.inject.bind_element_processor(binder, ReflectReferencedTablesProcessor, els.Phases.TARGETS)

    return binder
