"""
https://docs.snowflake.com/en/user-guide/snowsql-start.html#using-a-proxy-server
https://github.com/snowflakedb/snowflake-jdbc
https://github.com/abhinavsingh/proxy.py/tree/develop/proxy
"""
import logging

from omnibus import http
from omnibus import logs


log = logging.getLogger(__name__)


def main():
    def app(environ, start_response):
        log.info(f'Got request: {environ!r}')
        import pprint
        pprint.pprint(environ)
        # buf = environ['wsgi.input'].read()
        start_response(http.consts.STATUS_OK, [])
        return []

    with http.wsgiref.ThreadSpawningWsgiRefServer(
            http.bind.TcpBinder(http.bind.TcpBinder.Config('0.0.0.0', 0)),
            app
    ) as server:
        with server.loop_context() as loop:
            log.info(f'Listening on port {server.binder.port}')
            for _ in loop:
                pass


if __name__ == '__main__':
    logs.configure_standard_logging(logging.INFO)
    main()
