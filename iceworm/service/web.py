"""
TODO:
 - ui
 - 'acknowledgable' alerts / warnings - 'do not auto backfill if table bigger than …'
"""
import contextlib
import logging
import time
import typing as ta

from omnibus import dataclasses as dc
from omnibus import http
from omnibus import logs
from omnibus.http.types import Self

from . import resources
from .. import protos


log = logging.getLogger(__name__)


class BoomException(Exception):
    pass


@protos.proto()
class WebServiceStatus(dc.Pure):
    uptime: float


class App(http.App):

    def __init__(self) -> None:
        super().__init__()

        self._start_time: ta.Optional[float] = None

    def __enter__(self: Self) -> Self:
        super().__enter__()
        self._start_time = time.time()
        return self

    def __call__(self, environ: http.Environ, start_response: http.StartResponse) -> ta.Iterable[bytes]:
        method = environ.get('REQUEST_METHOD')
        path = environ.get('PATH_INFO')

        if path == '/ok':
            start_response(http.consts.STATUS_OK, [])
            return []

        elif path == '/boom':
            raise BoomException

        elif method == 'GET':
            if path == '/favicon.ico':
                response_body = resources.favicon()
                response_headers = [
                    ('Content-Type', http.consts.CONTENT_ICON),
                    ('Content-Length', str(len(response_body))),
                ]
                start_response(http.consts.STATUS_OK, response_headers)
                return [response_body]

            elif path == '/status':
                status = WebServiceStatus(time.time() - self._start_time)

                from ..protos._gen import iceworm_pb2 as pb2
                status_pb = pb2.WebServiceStatus()
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

        else:
            start_response(http.consts.STATUS_METHOD_NOT_ALLOWED, [])
            return []

        start_response(http.consts.STATUS_NOT_FOUND, [])
        return []


def main():
    with contextlib.ExitStack() as es:
        app = es.enter_context(App())
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


if __name__ == '__main__':
    logs.configure_standard_logging(logging.INFO)
    main()
