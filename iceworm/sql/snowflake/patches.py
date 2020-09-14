"""
TODO:
 - purge the dumbass arrow libs
  - chunk_downloader.py -> from .arrow_context import ArrowConverterContext - fucking idiots
   - ** lazy_import, do what omni does for mypy **
"""
import importlib.machinery
import sys

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


def _is_instance_or_subclass(obj, cls):
    return (isinstance(obj, type) and issubclass(obj, cls)) or isinstance(obj, cls)


class SnowflakePathFinder(importlib.machinery.PathFinder):

    @classmethod
    def _get_spec(cls, fullname, path, target=None):
        namespace_path = []
        for entry in path:
            if not isinstance(entry, (str, bytes)):
                continue
            finder = cls._path_importer_cache(entry)
            if finder is not None:
                if isinstance(finder, importlib.machinery.FileFinder):
                    finder = importlib.machinery.FileFinder(
                        finder.path,
                        *[
                            (i, [s]) for s, i in finder._loaders
                            if not _is_instance_or_subclass(i, importlib.machinery.ExtensionFileLoader)
                        ]
                    )
                if hasattr(finder, 'find_spec'):
                    spec = finder.find_spec(fullname, target)
                else:
                    spec = cls._legacy_get_spec(fullname, finder)
                if spec is None:
                    continue
                if spec.loader is not None:
                    return spec
                portions = spec.submodule_search_locations
                if portions is None:
                    raise ImportError('spec missing loader')
                namespace_path.extend(portions)
        else:
            return None

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if not fullname.startswith('mypy.') and fullname != 'mypy':
            return None
        if path is None:
            path = sys.path
        spec = cls._get_spec(fullname, path, target)
        if spec is None:
            return None
        elif spec.loader is None:
            namespace_path = spec.submodule_search_locations
            if namespace_path:
                spec.origin = None
                spec.submodule_search_locations = importlib.machinery._NamespacePath(
                    fullname,
                    namespace_path,
                    cls._get_spec,
                )
                return spec
            else:
                return None
        else:
            return spec


@lang.cached_nullary
def install_import_hook():
    for i, e in enumerate(sys.meta_path):
        if _is_instance_or_subclass(e, importlib.machinery.PathFinder):
            break
    sys.meta_path.insert(i, SnowflakePathFinder)
    sys.path_importer_cache.clear()
    importlib.invalidate_caches()
