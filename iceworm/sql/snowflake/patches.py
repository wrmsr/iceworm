"""
TODO:
 - purge the dumbass arrow libs
  - chunk_downloader.py -> from .arrow_context import ArrowConverterContext - fucking idiots
   - ** lazy_import, do what omni does for mypy **
"""
from omnibus import lang


@lang.cached_nullary
def patch_ssl_wrapper():
    from snowflake.connector import ssl_wrap_socket

    import threading
    local = threading.local()

    def ssl_wrap_socket_with_ocsp(*args, **kwargs):
        local.depth = getattr(local, 'depth', 0) + 1
        if local.depth >= 3:
            raise RuntimeError('snowflake ssl monkeypatch will infinitely recurse')
        try:
            return _ssl_wrap_socket_with_ocsp(*args, **kwargs)
        finally:
            local.depth -= 1

    _ssl_wrap_socket_with_ocsp = ssl_wrap_socket.ssl_wrap_socket_with_ocsp
    ssl_wrap_socket.ssl_wrap_socket_with_ocsp = ssl_wrap_socket_with_ocsp

    def inject_into_urllib3():
        ssl_wrap_socket.connection_.ssl_wrap_socket = ssl_wrap_socket_with_ocsp

    ssl_wrap_socket.inject_into_urllib3 = inject_into_urllib3

    if ssl_wrap_socket.connection_.ssl_wrap_socket == _ssl_wrap_socket_with_ocsp:
        ssl_wrap_socket.connection_.ssl_wrap_socket = ssl_wrap_socket_with_ocsp
