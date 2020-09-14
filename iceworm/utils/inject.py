import typing as ta
import weakref

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import inject as inj
from omnibus import lifecycles as lc


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
