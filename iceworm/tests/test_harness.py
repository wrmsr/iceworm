"""
TODO:
 - pytest injector scopes:
  - lifecycle callbacks
 - still use pytest for parameterization
 - 'harness' dep?
 - inj mods reg in conftests?
  - watch imports
"""
import abc
import contextlib
import typing as ta

from _pytest.fixtures import FixtureRequest # noqa
from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import inject as inj
from omnibus import lang
import omnibus.inject.scopes  # noqa
import pytest


T = ta.TypeVar('T')


class PytestScope(lang.AutoEnum):
    SESSION = ...
    PACKAGE = ...
    MODULE = ...
    CLASS = ...
    FUNCTION = ...


class PytestScopeScope(inj.scopes.Scope, lang.Abstract, lang.Sealed):

    def __init__(self) -> None:
        super().__init__()

        self._request_key = inj.Key(FixtureRequest, self.pytest_scope())
        self._state: ta.Optional[PytestScopeScope.State] = None

    class State(dc.Pure):
        request: FixtureRequest
        values: ta.MutableMapping[inj.types.Binding, ta.Any] = dc.field(default_factory=ocol.IdentityKeyDict)

    @abc.abstractclassmethod
    def pytest_scope(cls) -> PytestScope:
        raise NotImplementedError

    def enter(self, request: FixtureRequest) -> None:
        check.none(self._state)
        self._state = self.State(request)

    def exit(self) -> None:
        check.not_none(self._state)
        self._state = None

    def provide(self, binding: inj.types.Binding[T]) -> T:
        check.not_none(self._state)
        if binding.key == self._request_key:
            return self._state.request
        try:
            return self._state.values[binding]
        except KeyError:
            value = self._state.values[binding] = binding.provider()
            return value

    _subclass_map: ta.Mapping[PytestScope, ta.Type['PytestScopeScope']] = {}

    @classmethod
    def _subclass(cls, s: PytestScope):
        @classmethod  # noqa
        def pytest_scope(cls) -> PytestScope:  # noqa
            return s
        check.isinstance(s, PytestScope)
        check.not_in(s, cls._subclass_map)
        scls = type(
            s.name.lower().capitalize() + cls.__name__,
            (cls, lang.Final),
            {
                'pytest_scope': pytest_scope,
                '__module__': cls.__module__,
            },
        )
        cls._subclass_map[s] = scls
        return scls


SessionScope = PytestScopeScope._subclass(PytestScope.SESSION)
PackageeScope = PytestScopeScope._subclass(PytestScope.PACKAGE)
ModuleScope = PytestScopeScope._subclass(PytestScope.MODULE)
ClassScope = PytestScopeScope._subclass(PytestScope.CLASS)
FunctionScope = PytestScopeScope._subclass(PytestScope.FUNCTION)


class Harness:

    def __init__(self) -> None:
        super().__init__()

        binder = inj.create_binder()
        for pss in PytestScopeScope._subclass_map.values():
            binder._elements.append(inj.types.ScopeBinding(pss))
            binder.bind(FixtureRequest, annotated_with=pss.pytest_scope(), in_=pss)

        self._injector = inj.create_injector(binder)

        self._scopes: ta.Mapping[PytestScope, PytestScopeScope] = {
            s.pytest_scope(): self._injector._scopes[s]
            for s in PytestScopeScope._subclass_map.values()
        }

    def enter_scope(self, scope: PytestScope, request: FixtureRequest) -> None:
        self._scopes[scope].enter(request)

    def exit_scope(self, scope: PytestScope) -> None:
        self._scopes[scope].exit()

    def __getitem__(
            self,
            target: ta.Union[inj.Key[T], ta.Type[T]],
    ) -> T:
        return self._injector[target]

    @contextlib.contextmanager
    def scope_manager(self, scope: PytestScope, request: FixtureRequest) -> ta.Generator[None, None, None]:
        check.isinstance(request, FixtureRequest)
        self.enter_scope(scope, request)
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
    req: FixtureRequest = HARNESS[inj.Key(FixtureRequest, PytestScope.FUNCTION)]
    print(req.function)
