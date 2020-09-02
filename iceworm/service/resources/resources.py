import functools

from omnibus import lang
import pkg_resources


def _read(name: str) -> bytes:
    package = __package__
    if '/' in name:
        dirname, _, name = name.rpartition('/')
        package += '.'.join(dirname.split('/'))
    with pkg_resources.resource_stream(package, name) as f:
        return f.read()


@functools.lru_cache()
def read(name: str) -> bytes:
    return _read(name)


@functools.lru_cache()
def reads(name: str) -> str:
    return _read(name).decode('UTF-8')


@lang.cached_nullary
def favicon() -> bytes:
    return read('favicon.ico')
