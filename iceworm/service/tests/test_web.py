import time
import typing as ta
import urllib.request

from omnibus import http
from omnibus import inject as inj
from omnibus import lifecycles as lc

from .. import inject
from .. import web
from ...tests.helpers import run_with_timeout
from ...utils import inject as utinj


def test_web():
    port = 8181

    server: http.wsgiref.WsgiServer = None
    with web.build_app_context() as app:
        def fn0():
            nonlocal server
            server = http.wsgiref.ThreadSpawningWsgiRefServer(
                http.bind.TcpBinder(
                    http.bind.TcpBinder.Config('0.0.0.0', port)
                ),
                app,
            )
            server.run()

        def fn1():
            time.sleep(0.5)
            while True:
                try:
                    url = f'http://localhost:{port}/status'
                    req = urllib.request.Request(url, method='GET')
                    with urllib.request.urlopen(req) as resp:
                        data = resp.read()
                        print(data)
                    if resp.status == 200:
                        server.shutdown()
                        return
                except Exception:
                    pass
                time.sleep(0.1)

        run_with_timeout(fn0, fn1)


class TestApp:
    ENDPOINTS = [web.Endpoint('GET', '/x')]

    def __call__(self, environ: http.Environ, start_response: http.StartResponse) -> ta.Iterable[bytes]:
        start_response(200, [])
        return []


def test_inject():
    binder = inj.create_binder()
    inject.install(binder)

    binder.bind(TestApp)
    inject.bind_handler_endpoints(binder, TestApp)

    binder.bind(lc.LifecycleManager, as_eager_singleton=True)
    binder.bind_provision_listener(utinj.LifecycleRegistrar())

    injector = inj.create_injector(binder)
    web_app = injector[web.App]
    with lc.context_manage(injector[lc.LifecycleManager]):
        print(web_app)
