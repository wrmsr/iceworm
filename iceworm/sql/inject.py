import typing as ta

from omnibus import check
from omnibus import inject as inj
from omnibus.configs import inject as cfgs_inj

from . import objman  # noqa
from . import postgres
from . import snowflake
from .adapter import Adapter


def bind_adapter_impl(binder: inj.Binder, cls: ta.Type[Adapter]) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, Adapter)

    cfgs_inj.bind_impl(binder, Adapter, cls)


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    bind_adapter_impl(binder, postgres.PostgresAdapter)
    bind_adapter_impl(binder, snowflake.SnowflakeAdapter)

    cfgs_inj.bind_factory(binder, Adapter)

    # binder.bind_class(objman.ObjectManager, assists={'engine', 'adapter'})

    return binder
