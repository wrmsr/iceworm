import time
import urllib.request

from omnibus import http

from .. import web
from ...tests.helpers import run_with_timeout


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
