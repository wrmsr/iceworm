import abc
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import inject as inj
from omnibus import lang
import omnibus.inject.scopes  # noqa

from .. import elements as els


T = ta.TypeVar('T')


class _InjectorScope(inj.scopes.Scope, lang.Abstract, lang.Sealed):

    def __init__(self) -> None:
        super().__init__()

        self._state: ta.Optional[_InjectorScope.State] = None

    class State(dc.Pure):
        values: ta.MutableMapping[inj.types.Binding, ta.Any] = dc.field(default_factory=ocol.IdentityKeyDict)

    @abc.abstractclassmethod
    def phase(cls) -> els.processing.Phase:
        raise NotImplementedError

    def enter(self) -> None:
        check.none(self._state)
        self._state = self.State()

    def exit(self) -> None:
        check.not_none(self._state)
        self._state = None

    def provide(self, binding: inj.types.Binding[T]) -> T:
        check.not_none(self._state)
        if binding.key == inj.Key(els.processing.Phase):
            return self.phase()
        try:
            return self._state.values[binding]
        except KeyError:
            value = self._state.values[binding] = binding.provider()
            return value

    _subclass_map: ta.Mapping[els.processing.Phase, ta.Type['_InjectorScope']] = {}

    @classmethod
    def _subclass(cls, p: els.processing.Phase):
        check.isinstance(p, els.processing.Phase)
        check.not_in(p, cls._subclass_map)
        scls = type(
            p.name.lower().capitalize() + cls.__name__,
            (cls, lang.Final),
            {
                'phase': classmethod(lambda _: p),
                '__module__': cls.__module__,
            },
            )
        cls._subclass_map[p] = scls
        return scls


Bootstrap = _InjectorScope._subclass(els.processing.Phases.BOOTSTRAP)
Sites = _InjectorScope._subclass(els.processing.Phases.SITES)
Rules = _InjectorScope._subclass(els.processing.Phases.RULES)
Connectors = _InjectorScope._subclass(els.processing.Phases.CONNECTORS)
Targets = _InjectorScope._subclass(els.processing.Phases.TARGETS)
Finalize = _InjectorScope._subclass(els.processing.Phases.FINALIZE)
