from omnibus import check
from omnibus import inject as inj

from .. import elements as els
from .sites import SiteProcessor


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    els.inject.bind_element_processor(binder, SiteProcessor, els.Phases.SITES)

    return binder
