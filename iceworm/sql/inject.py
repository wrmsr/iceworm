import typing as ta

from omnibus import check
from omnibus import inject as inj

from . import postgres
from . import snowflake
from ..utils import configable as cfgabl
from .adapter import Adapter


def bind_adapter_impl(binder: inj.Binder, cls: ta.Type[Adapter]) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, Adapter)

    cfgabl.bind_impl(binder, Adapter, cls)


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    bind_adapter_impl(binder, postgres.PostgresAdapter)
    bind_adapter_impl(binder, snowflake.SnowflakeAdapter)

    cfgabl.bind_factory(binder, Adapter)

    return binder
