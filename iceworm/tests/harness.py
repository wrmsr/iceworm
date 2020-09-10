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
import warnings
import weakref

from _pytest.fixtures import FixtureRequest # noqa
from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import inject as inj
from omnibus import lang
from omnibus import lifecycles as lc
import omnibus.inject.scopes  # noqa
import pytest


T = ta.TypeVar('T')


class Scope(lang.AutoEnum):
    SESSION = ...
    PACKAGE = ...
    MODULE = ...
    CLASS = ...
    FUNCTION = ...


SCOPES: ta.Sequence[Scope] = list(Scope)


class _InjectorScope(inj.scopes.Scope, lang.Abstract, lang.Sealed):

    def __init__(self) -> None:
        super().__init__()

        self._request_key = inj.Key(FixtureRequest, self.pytest_scope())
        self._state: ta.Optional[_InjectorScope.State] = None

    class State(dc.Pure):
        request: FixtureRequest
        values: ta.MutableMapping[inj.types.Binding, ta.Any] = dc.field(default_factory=ocol.IdentityKeyDict)

    @abc.abstractclassmethod
    def pytest_scope(cls) -> Scope:
        raise NotImplementedError

    def enter(self, request: FixtureRequest) -> None:
        check.none(self._state)
        check.state(request.scope == self.pytest_scope().name.lower())
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

    _subclass_map: ta.Mapping[Scope, ta.Type['_InjectorScope']] = {}

    @classmethod
    def _subclass(cls, s: Scope):
        @classmethod  # noqa
        def pytest_scope(cls) -> Scope:  # noqa
            return s
        check.isinstance(s, Scope)
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


Session = _InjectorScope._subclass(Scope.SESSION)
Packagee = _InjectorScope._subclass(Scope.PACKAGE)
Module = _InjectorScope._subclass(Scope.MODULE)
Class = _InjectorScope._subclass(Scope.CLASS)
Function = _InjectorScope._subclass(Scope.FUNCTION)


class _ScopeProvisionListener:

    def __init__(self) -> None:
        super().__init__()

        self._stack = []

    class Entry(ta.NamedTuple):
        binding: inj.types.Binding
        scope: ta.Optional[Scope]

    def __call__(self, injector, key, fn):
        binding = check.isinstance(injector.get_binding(key), inj.types.Binding)
        if issubclass(binding.scoping, _InjectorScope):
            scope = binding.scoping.pytest_scope()
        else:
            scope = None

        if self._stack:
            cur = self._stack[-1]
            if scope is not None:
                check.not_none(cur.scope)
                check.state(scope.value <= cur.scope.value)
                scope = min(scope, cur.scope, key=lambda s: s.value)
            else:
                if issubclass(binding.scoping, _CurrentInjectorScope):
                    scope = check.not_none(cur.scope)

        elif scope is not None:
            # TODO: check early that scope is active
            pass

        else:
            for iscope in injector._scopes.values():
                if isinstance(iscope, _InjectorScope) and iscope._state is not None:
                    ipscope = iscope.pytest_scope()
                    if scope is None:
                        scope = ipscope
                    else:
                        scope = max(scope, ipscope, key=lambda s: s.value)

        ent = self.Entry(binding, scope)
        self._stack.append(ent)
        try:
            return fn()
        finally:
            popped = self._stack.pop()
            check.state(popped is ent)


class _CurrentInjectorScope(inj.scopes.Scope, lang.Final):

    def provide(self, binding: inj.types.Binding[T]) -> T:
        check.state(binding.key.annotation is None)
        injector = inj.Injector.current
        spl = injector[_ScopeProvisionListener]
        scope = check.not_none(spl._stack[-1].scope)
        new_key = inj.Key(binding.key.type, scope)
        return injector[new_key]


class _LifecycleRegistrar:

    def __init__(self) -> None:
        super().__init__()
        self._seen = weakref.WeakSet()

    def __call__(self, injector: inj.Injector, key, fn):
        instance = fn()
        if (
                isinstance(instance, lc.Lifecycle) and
                not isinstance(instance, lc.LifecycleManager) and
                instance not in self._seen
        ):
            binding = check.isinstance(injector.get_binding(key), inj.types.Binding)
            scope = check.issubclass(binding.scoping, _InjectorScope)
            man = injector.get(inj.Key(lc.LifecycleManager, scope.pytest_scope()))
            man.add(instance)
            self._seen.add(instance)
        return instance


class _Eager(dc.Pure):
    key: inj.Key


class Harness:

    def __init__(self, *binders: inj.Binder) -> None:
        super().__init__()

        binder = inj.create_binder()
        binder.bind(Harness, to_instance=self)

        for pss in _InjectorScope._subclass_map.values():
            binder._elements.append(inj.types.ScopeBinding(pss))
            binder.bind(FixtureRequest, annotated_with=pss.pytest_scope(), in_=pss)
            binder.bind(lc.LifecycleManager, annotated_with=pss.pytest_scope(), in_=pss)
            binder.new_set_binder(_Eager, annotated_with=pss.pytest_scope(), in_=pss)

        spl = _ScopeProvisionListener()
        binder.bind(_ScopeProvisionListener, to_instance=spl)
        binder.bind_provision_listener(spl)

        binder.bind_provision_listener(_LifecycleRegistrar())

        binder._elements.append(inj.types.ScopeBinding(_CurrentInjectorScope))
        binder.bind(FixtureRequest, in_=_CurrentInjectorScope)
        binder.bind(lc.LifecycleManager, in_=_CurrentInjectorScope)

        self._injector = inj.create_injector(binder, *binders)

        self._scopes: ta.Mapping[Scope, _InjectorScope] = {
            s.pytest_scope(): self._injector._scopes[s]
            for s in _InjectorScope._subclass_map.values()
        }

    def __enter__(self):
        return self

    def __exit__(self, et, e, tb):
        for s in self._scopes.values():
            if s._state is not None:
                warnings.warn(f'Scope {s.pytest_scope()} is still active')

    def __getitem__(
            self,
            target: ta.Union[inj.Key[T], ta.Type[T]],
    ) -> T:
        return self._injector[target]

    @contextlib.contextmanager
    def scope_manager(self, scope: Scope, request: FixtureRequest) -> ta.Generator[None, None, None]:
        check.isinstance(request, FixtureRequest)
        self._scopes[scope].enter(request)
        try:
            lm = self._injector[inj.Key(lc.LifecycleManager, scope)]
            with lc.context_manage(lm):
                eags = self._injector[inj.Key(ta.Set[_Eager], scope)]
                for eag in eags:
                    self._injector[eag.key]  # noqa
                yield
        finally:
            self._scopes[scope].exit()


@pytest.yield_fixture(scope='session', autouse=True)
def harness() -> ta.Generator[Harness, None, None]:
    with Harness(*_HARNESS_BINDERS) as harness:
        yield harness


@pytest.yield_fixture(scope='session', autouse=True)
def _scope_listener_session(harness, request):
    with harness.scope_manager(Scope.SESSION, request):
        yield


@pytest.yield_fixture(scope='package', autouse=True)
def _scope_listener_package(harness, request):
    with harness.scope_manager(Scope.PACKAGE, request):
        yield


@pytest.yield_fixture(scope='module', autouse=True)
def _scope_listener_module(harness, request):
    with harness.scope_manager(Scope.MODULE, request):
        yield


@pytest.yield_fixture(scope='class', autouse=True)
def _scope_listener_class(harness, request):
    with harness.scope_manager(Scope.CLASS, request):
        yield


@pytest.yield_fixture(scope='function', autouse=True)
def _scope_listener_function(harness, request):
    with harness.scope_manager(Scope.FUNCTION, request):
        yield


_HARNESS_BINDERS = []


def register(obj: T) -> T:
    if isinstance(obj, inj.Binder):
        _HARNESS_BINDERS.append(obj)
    else:
        raise TypeError(obj)
    return obj


def bind(scope: ta.Type[_InjectorScope], *, eager: bool = False):
    def inner(obj):
        check.isinstance(obj, type)
        binder = register(inj.create_binder())
        binder.bind(obj, in_=scope)
        if eager:
            sb = binder.new_set_binder(_Eager, annotated_with=scope.pytest_scope(), in_=scope)
            sb.bind(to_instance=_Eager(inj.Key(obj)))
        return obj
    check.issubclass(scope, _InjectorScope)
    return inner
