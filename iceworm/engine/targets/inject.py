import typing as ta

from omnibus import check
from omnibus import inject as inj

from . import infer
from . import joins
from . import reflect
from .. import elements as els


def _install_elements(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    els.inject.bind_element_processor(binder, infer.InferTableProcessor, els.Phases.TARGETS)
    els.inject.bind_element_processor(binder, joins.JoinSplittingProcessor, els.Phases.TARGETS)
    els.inject.bind_element_processor(binder, reflect.ReflectReferencedTablesProcessor, els.Phases.TARGETS)
    els.inject.bind_element_processor(binder, reflect.ReflectTablesProcessor, els.Phases.TARGETS)

    return binder


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    binder.new_set_binder(ta.Callable[[inj.Binder], None], annotated_with='elements').bind(to_instance=_install_elements)  # noqa

    return binder
