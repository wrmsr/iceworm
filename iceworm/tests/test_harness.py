"""
TODO:
 - pytest injector scopes:
  - lifecycle callbacks
 - still use pytest for parameterization
 - 'harness' dep?
 - inj mods reg in conftests?
  - watch imports
"""
import contextlib
import typing as ta

from _pytest.fixtures import FixtureRequest # noqa
from omnibus import check
from omnibus import inject as inj
from omnibus import lang
import pytest


class PytestScope(lang.AutoEnum):
    SESSION = ...
    PACKAGE = ...
    MODULE = ...
    CLASS = ...
    FUNCTION = ...


class Harness:

    def enter_scope(self, scope: PytestScope) -> None:
        print(f'entered {scope}')

    def exit_scope(self, scope: PytestScope) -> None:
        print(f'exited {scope}')

    @contextlib.contextmanager
    def scope_manager(self, scope: PytestScope, request: FixtureRequest) -> ta.Generator[None, None, None]:
        check.isinstance(request, FixtureRequest)
        self.enter_scope(scope)
        try:
            yield
        finally:
            self.exit_scope(scope)


HARNESS = Harness()


@pytest.yield_fixture(scope='session', autouse=True)
def _scope_listener_session(request):
    with HARNESS.scope_manager(PytestScope.SESSION, request):
        yield


@pytest.yield_fixture(scope='package', autouse=True)
def _scope_listener_package(request):
    with HARNESS.scope_manager(PytestScope.PACKAGE, request):
        yield


@pytest.yield_fixture(scope='module', autouse=True)
def _scope_listener_module(request):
    with HARNESS.scope_manager(PytestScope.MODULE, request):
        yield


@pytest.yield_fixture(scope='class', autouse=True)
def _scope_listener_class(request):
    with HARNESS.scope_manager(PytestScope.CLASS, request):
        yield


@pytest.yield_fixture(scope='function', autouse=True)
def _scope_listener_function(request):
    with HARNESS.scope_manager(PytestScope.FUNCTION, request):
        yield


def provider():
    def inner(fn):
        def new(cls):
            return fn()
        cls = type(fn.__name__, (), {'__new__': new})
        return cls
    return inner


@provider()
def some_url():
    return 'a url'


@pytest.mark.xfail()
def test_harness():
    bnd = inj.create_binder()
    bnd.bind(some_url)
    ij = inj.create_injector(bnd)
    assert ij[some_url] == 'a url'
    with pytest.raises(Exception):
        ij[5]  # noqa


def test_harness_2():
    pass
