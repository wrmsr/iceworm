import typing as ta

from omnibus import check
from omnibus import inject as inj

from .. import elements as els
from .planning import PlanningElementProcessor


def _install_elements(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    els.inject.bind_element_processor(binder, PlanningElementProcessor, els.Phases.PLAN)

    return binder


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    els.inject.bind_elements_module(binder, _install_elements)

    return binder
