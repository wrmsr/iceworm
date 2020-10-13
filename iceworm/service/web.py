"""
TODO:
 - ui
 - 'acknowledgable' alerts / warnings - 'do not auto backfill if table bigger than …'
"""
import contextlib
import logging
import string
import time
import typing as ta

from omnibus import check
from omnibus import collections as col
from omnibus import dataclasses as dc
from omnibus import http
from omnibus import lifecycles as lc

from . import resources
from .. import protos


log = logging.getLogger(__name__)


class Endpoint(dc.Pure):
    method: str = dc.field(check=lambda s: isinstance(s, str) and s and all(c in string.ascii_uppercase for c in s))
    path: str = dc.field(check=lambda s: isinstance(s, str) and s and s.startswith('/'))

    @classmethod
    def of(cls, obj: ta.Union['Endpoint', ta.Tuple[str, str]]) -> 'Endpoint':
        if isinstance(obj, Endpoint):
            return obj
        elif isinstance(obj, tuple):
            method, path = obj
            return Endpoint(method, path)
        else:
            raise TypeError(obj)


class Handler(dc.Pure):
    endpoints: ta.AbstractSet[Endpoint] = dc.field(coerce=lambda l: frozenset(Endpoint.of(e) for e in l))
    app: http.AppLike = dc.field(check=callable)


class OkApp:
    ENDPOINTS = [Endpoint('GET', '/ok')]

    def __call__(self, environ: http.Environ, start_response: http.StartResponse) -> ta.Iterable[bytes]:
        start_response(http.consts.STATUS_OK, [])
        return []


class BoomException(Exception):
    pass


class BoomApp:
    ENDPOINTS = [
        Endpoint('GET', '/boom'),
        Endpoint('POST', '/boom'),
    ]

    def __call__(self, environ: http.Environ, start_response: http.StartResponse) -> ta.Iterable[bytes]:
        raise BoomException


@protos.proto()
class ServiceWebStatus(dc.Pure):
    uptime: float


class StatusApp(lc.ContextManageableLifecycle):
    ENDPOINTS = [Endpoint('GET', '/status')]

    def __init__(self) -> None:
        super().__init__()

        self._start_time: ta.Optional[float] = None

    def _do_lifecycle_start(self) -> None:
        super()._do_lifecycle_start()
        self._start_time = time.time()

    def __call__(self, environ: http.Environ, start_response: http.StartResponse) -> ta.Iterable[bytes]:
        status = ServiceWebStatus(time.time() - self._start_time)

        from ..protos._gen import iceworm_pb2 as pb2
        status_pb = pb2.ServiceWebStatus()
        for fld in dc.fields(status):
            setattr(status_pb, fld.name, getattr(status, fld.name))

        from google.protobuf import json_format as jf
        response_body = jf.MessageToJson(status_pb).encode('utf-8')

        response_headers = [
            ('Content-Type', http.consts.CONTENT_JSON),
            ('Content-Length', str(len(response_body))),
        ]

        start_response(http.consts.STATUS_OK, response_headers)
        return [response_body]


class FaviconApp:
    ENDPOINTS = [Endpoint('GET', '/favicon.ico')]

    def __call__(self, environ: http.Environ, start_response: http.StartResponse) -> ta.Iterable[bytes]:
        response_body = resources.favicon()
        response_headers = [
            ('Content-Type', http.consts.CONTENT_ICON),
            ('Content-Length', str(len(response_body))),
        ]
        start_response(http.consts.STATUS_OK, response_headers)
        return [response_body]


class App(lc.ContextManageableLifecycle):

    def __init__(self, handlers: ta.AbstractSet[Handler]) -> None:
        super().__init__()

        self._handlers = [check.isinstance(h, Handler) for h in handlers]
        self._handlers_by_endpoint = col.unique_dict((e, h) for h in self._handlers for e in h.endpoints)
        self._all_paths = {e.path for h in self._handlers for e in h.endpoints}

    def _do_lifecycle_start(self) -> None:
        super()._do_lifecycle_start()
        log.info('App started')

    def __call__(self, environ: http.Environ, start_response: http.StartResponse) -> ta.Iterable[bytes]:
        method = environ.get('REQUEST_METHOD')
        path = environ.get('PATH_INFO')

        endpoint = Endpoint(method, path)
        try:
            handler = self._handlers_by_endpoint[endpoint]
        except KeyError:
            if path in self._all_paths:
                status = http.consts.STATUS_METHOD_NOT_ALLOWED
            else:
                status = http.consts.STATUS_NOT_FOUND
            start_response(status, [])
            return []
        else:
            return handler.app(environ, start_response)


@contextlib.contextmanager
def build_app_context() -> ta.Generator[App, None, None]:
    with contextlib.ExitStack() as es:
        yield es.enter_context(App({
            Handler(OkApp.ENDPOINTS, OkApp()),
            Handler(BoomApp.ENDPOINTS, BoomApp()),
            Handler(FaviconApp.ENDPOINTS, FaviconApp()),
            Handler(StatusApp.ENDPOINTS, es.enter_context(StatusApp())),
        }))


def main():
    with contextlib.ExitStack() as es:
        app = es.enter_context(build_app_context())
        server = es.enter_context(
            http.wsgiref.ThreadSpawningWsgiRefServer(
                http.bind.TcpBinder(http.bind.TcpBinder.Config('0.0.0.0', 0)),
                app,
            )
        )
        loop = es.enter_context(server.loop_context())
        port = server.binder.port
        log.info(f'Listening on port {port}')
        for _ in loop:
            pass
