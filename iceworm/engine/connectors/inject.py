import typing as ta  # noqa

from omnibus import check
from omnibus import inject as inj

from . import impls
from .. import elements as els
from ...utils import configable as cfgabl
from .collections import Connector
from .collections import ConnectorSet


def bind_connector_factory(binder: inj.Binder, impl_cls: ta.Type[Connector]) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(impl_cls, Connector)

    cfgabl.bind_impl(binder, Connector, impl_cls)


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    cfgabl.bind_dict(binder, Connector)

    bind_connector_factory(binder, impls.computed.ComputedConnector)
    bind_connector_factory(binder, impls.dual.DualConnector)
    bind_connector_factory(binder, impls.files.FileConnector)
    bind_connector_factory(binder, impls.sql.SqlConnector)
    bind_connector_factory(binder, impls.system.SystemConnector)

    def provide_connector_set(
            es: els.ElementSet,
            facs: ta.Mapping[ta.Type[Connector.Config], ta.Callable[..., Connector]],
    ) -> ConnectorSet:
        lst = []
        for cfg in es.get_type_set(Connector.Config):
            fac = facs[type(cfg)]
            ctor = fac(config=cfg)
            lst.append(ctor)
        return ConnectorSet.of(lst)

    binder.bind_callable(provide_connector_set, in_=els.inject.PostConnectors)
    els.inject.bind_post_eager(binder, ConnectorSet, els.Phases.CONNECTORS)

    return binder
