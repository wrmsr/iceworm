import typing as ta  # noqa

from omnibus import check
from omnibus import inject as inj
from omnibus.configs import inject as cfgs_inj

from . import impls
from .. import elements as els
from .collections import ConnectionSet  # noqa
from .collections import Connector
from .collections import ConnectorSet
from .mirrors import Mirror  # noqa


def bind_connector_impl(binder: inj.Binder, impl_cls: ta.Type[Connector]) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(impl_cls, Connector)

    cfgs_inj.bind_impl(binder, Connector, impl_cls)


def _install_elements(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    cfgs_inj.bind_factory(binder, Connector)

    bind_connector_impl(binder, impls.computed.ComputedConnector)
    bind_connector_impl(binder, impls.dual.DualConnector)
    bind_connector_impl(binder, impls.files.FileConnector)
    bind_connector_impl(binder, impls.sql.SqlConnector)
    bind_connector_impl(binder, impls.system.SystemConnector)

    els.inject.bind_element_processor(binder, impls.files.MountPathProcessor, els.Phases.CONNECTORS)

    def provide_connector_set(
            es: els.ElementSet,
            fac: ta.Callable[..., Connector],
    ) -> ConnectorSet:
        lst = []
        for cfg in es.get_type_set(Connector.Config):
            ctor = fac(config=cfg)
            lst.append(ctor)
        return ConnectorSet.of(lst)

    binder.bind_callable(provide_connector_set, in_=els.inject.PostConnectors)
    els.inject.bind_post_eager(binder, ConnectorSet, els.Phases.CONNECTORS)

    # binder.bind(Mirror, to=ConnectionSet)

    return binder


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    els.inject.bind_elements_module(binder, _install_elements)

    return binder
