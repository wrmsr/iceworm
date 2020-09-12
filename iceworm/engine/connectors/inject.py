import typing as ta  # noqa

from omnibus import inject as inj

from .. import connectors as ctrs
from .. import elements as els


def install(binder: inj.Binder) -> inj.Binder:
    def provide_connector_set(es: els.ElementSet) -> ctrs.ConnectorSet:
        return ctrs.ConnectorSet.of(es.get_type_set(ctrs.Connector.Config))

    binder.bind_callable(provide_connector_set, in_=els.inject.PostConnectors)
    els.inject.bind_post_eager(binder, ctrs.ConnectorSet, els.Phases.CONNECTORS)

    return binder
