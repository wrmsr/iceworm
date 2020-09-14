import functools
import typing as ta

from omnibus import check
from omnibus import http
from omnibus import inject as inj

from . import web


def provide_binder(config: http.bind.Binder.Config) -> http.bind.Binder:
    if isinstance(config, http.bind.TcpBinder.Config):
        return http.bind.TcpBinder(config)
    elif isinstance(config, http.bind.UnixBinder.Config):
        return http.bind.UnixBinder(config)
    else:
        raise TypeError(config)


def bind_handler_endpoints(
        binder: inj.Binder,
        app: ta.Any,
        endpoints: ta.Optional[ta.Iterable[web.Endpoint]] = None,
) -> None:
    check.isinstance(binder, inj.Binder)

    if endpoints is not None:
        endpoints = {check.isinstance(endpoint, web.Endpoint) for endpoint in endpoints}
    elif isinstance(app, type) and 'ENDPOINTS' in app.__dict__:
        endpoints = {check.isinstance(endpoint, web.Endpoint) for endpoint in app.ENDPOINTS}
    else:
        raise ValueError('Must provide endpoints')

    def provide(endpoints, app):
        return web.Handler(endpoints, app)

    epp = functools.partial(provide, endpoints)
    binder.bind_callable(epp, key=inj.Key(app, web.Endpoint), kwargs={'app': app})
    binder.new_set_binder(web.Handler).bind(to=inj.Key(app, web.Endpoint))


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    binder.bind(web.App, as_eager_singleton=True)
    binder.new_set_binder(web.Handler)

    for app in [
        web.OkApp,
        web.BoomApp,
        web.FaviconApp,
        web.StatusApp,
    ]:
        binder.bind(app)
        bind_handler_endpoints(binder, app)

    return binder
