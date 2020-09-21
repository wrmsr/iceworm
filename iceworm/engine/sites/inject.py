import typing as ta

from omnibus import check
from omnibus import inject as inj

from .. import elements as els
from .sites import SiteProcessor


def _install_elements(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    els.inject.bind_element_processor(binder, SiteProcessor, els.Phases.SITES)

    return binder


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    binder.new_set_binder(ta.Callable[[inj.Binder], None], annotated_with='elements').bind(to_instance=_install_elements)  # noqa

    return binder
