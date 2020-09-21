import functools
import typing as ta
import weakref

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import dynamic as dyn
from omnibus import inject as inj
from omnibus import lang
from omnibus import lifecycles as lc
from omnibus import properties


T = ta.TypeVar('T')


def bind_contextmanager_lifecycle(binder: inj.Binder, target: ta.Union[inj.Key, ta.Type]) -> None:
    binder.bind_callable(
        lc.ContextManagerLifecycle,
        key=inj.Key(lc.ContextManagerLifecycle, target),
        kwargs={'obj': target},
        as_eager_singleton=True,
    )


class LifecycleRegistrar:

    def __init__(self) -> None:
        super().__init__()
        self._seen = ocol.IdentitySet()

    def __call__(self, injector: inj.Injector, key, fn):
        instance = fn()
        if (
                isinstance(instance, lc.Lifecycle) and
                not isinstance(instance, lc.LifecycleManager) and
                instance not in self._seen
        ):
            man = injector.get(lc.LifecycleManager)
            man.add(instance)
            self._seen.add(instance)
        return instance


class _LifecycleRegistrar:

    def __init__(self) -> None:
        super().__init__()

        self._seen = weakref.WeakSet()
        self._stack: ta.List[_LifecycleRegistrar.State] = []

    class State(dc.Pure):
        key: inj.Key
        dependencies: ta.List[ta.Tuple[inj.Binding, ta.Any]] = dc.field(default_factory=list)

    def get_binding_manager_key(self, binding: inj.Binding) -> inj.Key[lc.LifecycleManager]:
        return inj.Key(lc.LifecycleManager)

    def __call__(self, injector: inj.Injector, key, fn):
        st = self.State(key)
        self._stack.append(st)
        try:
            instance = fn()
        finally:
            popped = self._stack.pop()
            check.state(popped is st)

        if isinstance(instance, lc.Lifecycle) and not isinstance(instance, lc.LifecycleManager):
            inst_binding = check.isinstance(injector.get_binding(key), inj.Binding)
            if self._stack:
                self._stack[-1].dependencies.append((inst_binding, instance))

            if instance not in self._seen:
                man_key = self.get_binding_manager_key(inst_binding)
                man: lc.LifecycleManager = injector.get(man_key)
                deps = [o for b, o in st.dependencies]  # if b.scoping == binding.scoping]
                man.add(instance, deps)
                self._seen.add(instance)

        elif self._stack:
            self._stack[-1].dependencies.extend(st.dependencies)

        return instance


class SimpleDynamicScope(inj.Scope, lang.Abstract):

    class _State(ta.NamedTuple):
        seed: ta.Mapping[inj.Key, ta.Any]
        binds: ta.MutableMapping[inj.Binding, ta.Any]

    def provide(self, binding: inj.Binding[T]) -> T:
        vals = self._CURRENT()
        try:
            return vals[binding]
        except KeyError:
            try:
                return vals[binding.key]
            except KeyError:
                val = vals[binding] = binding.provide()
                return val

    @properties.cached_class
    def _CURRENT(cls) -> dyn.Var[_State]:  # noqa
        return dyn.Var()

    @classmethod
    def _seed(cls, injector: inj.Injector, seed: ta.Mapping[ta.Union[type, inj.Key], ta.Any]) -> ta.Mapping[inj.Key, ta.Any]:  # noqa
        return {inj.Key(k) if isinstance(k, type) else check.isinstance(k, inj.Key): v for k, v in seed.items()}

    @properties.cached_class
    def enter(cls):  # noqa
        return functools.partial(_enter_simple_dynamic_scope, cls)

    @classmethod
    def _setup(cls, injector: inj.Injector, state: _State) -> None:
        pass


@dyn.contextmanager
def _enter_simple_dynamic_scope(cls: ta.Type[SimpleDynamicScope], injector: inj.Injector, *args, **kwargs) -> ta.Generator[None, None, None]:  # noqa
    check.isinstance(injector, inj.Injector)
    state = cls._State(
        seed=cls._seed(injector, *args, **kwargs),  # Noqa
        binds=ocol.IdentityKeyDict(),
    )
    with cls._CURRENT(state):
        with inj.Injector._CURRENT(injector):
            cls._setup(injector)
        yield
