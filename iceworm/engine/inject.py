import typing as ta

from omnibus import check
from omnibus import inject as inj

from . import connectors
from . import elements
from . import ops
from . import rules
from . import sites
from . import targets


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    binder.new_set_binder(ta.Callable[[inj.Binder], None], annotated_with='elements')
    binder.new_set_binder(ta.Callable[[inj.Binder], None], annotated_with='execution')

    connectors.inject.install(binder)
    elements.inject.install(binder)
    ops.inject.install(binder)
    rules.inject.install(binder)
    sites.inject.install(binder)
    targets.inject.install(binder)

    return binder
