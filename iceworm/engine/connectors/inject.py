import inspect
import typing as ta  # noqa

from omnibus import check
from omnibus import inject as inj
from omnibus import lang

from .. import elements as els
from .collections import Connector
from .collections import ConnectorSet


def install(binder: inj.Binder) -> inj.Binder:
    from . import impls

    # class MISSING(lang.Marker):
    #     pass
    #
    # def provide_sql_connector() -> ta.Callable[[Connector.Config], Connector]:
    #     init = getattr(impls.sql.SqlConnector, '__init__')
    #     prototype = init
    #
    #     sig = inspect.signature(prototype)
    #     kwargs = binder._get_callable_kwargs(prototype)
    #     kwargs_and_defaults = {
    #         k: (binder._get_key(v), (
    #             sig.parameters[k].default
    #             if k in sig.parameters and sig.parameters[k].default is not inspect._empty
    #             else MISSING
    #         ))
    #         for k, v in kwargs.items()
    #         if k != 'config'
    #     }
    #     for k, (v, d) in kwargs_and_defaults.items():
    #         check.isinstance(k, str)
    #         check.isinstance(v, inj.Key)
    #         if d is MISSING:
    #             binder._require_key(v, impls.sql.SqlConnector)
    #
    #     def provide(cfg: Connector.Config) -> Connector:
    #         instance_kwargs = {k: inj.Injector.current.get(v, d) for k, (v, d) in kwargs_and_defaults.items()}
    #         return impls.sql.SqlConnector(cfg, **instance_kwargs)
    #
    #     return provide

    db = binder.new_dict_binder(ta.Type[Connector.Config], ta.Callable[[Connector.Config], Connector])  # noqa
    # db.bind(impls.sql.SqlConnector.Config, to_instance=provide_sql_connector())

    ###

    def provide_connector_set(
            es: els.ElementSet,
            facs: ta.Dict[ta.Type[Connector.Config], ta.Callable[[Connector.Config], Connector]],
    ) -> ConnectorSet:  # noqa
        # facs[impls.sql.SqlConnector.Config](impls.sql.SqlConnector.Config('abc', url='def'))
        return ConnectorSet.of(es.get_type_set(Connector.Config))

    binder.bind_callable(provide_connector_set, in_=els.inject.PostConnectors)
    els.inject.bind_post_eager(binder, ConnectorSet, els.Phases.CONNECTORS)

    return binder
