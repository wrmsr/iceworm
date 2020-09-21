"""
TODO:
 - Driver * does not create injector *
  - EngineScope? SiteScope? seeded with ConnectionSet?
"""
import abc
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import inject as inj
from omnibus import lang
import omnibus.inject.scopes  # noqa

from . import processors
from . import queries
from .base import Element
from .collections import ElementSet
from .phases import PHASES
from .phases import Phase
from .phases import PhasePair
from .phases import Phases
from .phases import SUB_PHASES
from .phases import SubPhases
from .processing import ElementProcessingDriver
from .processing import ElementProcessor


T = ta.TypeVar('T')


class _Scope(inj.Scope, lang.Abstract, lang.Sealed):

    class State(dc.Data, final=True):
        values: ta.MutableMapping[inj.Binding, ta.Any] = dc.field(default_factory=ocol.IdentityKeyDict, frozen=True)  # noqa
        frozen: bool = False

    @abc.abstractclassmethod
    def phase_pair(cls) -> PhasePair:
        raise NotImplementedError

    def provide(self, binding: inj.Binding[T]) -> T:
        drv = inj.Injector.current[InjectionElementProcessingDriver]
        state = drv._scope_states[self]
        if binding.key == inj.Key(Phase):
            return self.phase_pair().phase
        try:
            return state.values[binding]
        except KeyError:
            check.state(not state.frozen)
            value = state.values[binding] = binding.provider()
            return value

    _subclass_map: ta.Mapping[PhasePair, ta.Type['_Scope']] = {}

    @classmethod
    def _subclass_one(cls, pp: PhasePair) -> ta.Type['_Scope']:
        check.isinstance(pp, PhasePair)
        check.not_in(pp, cls._subclass_map)
        scls = type(
            pp.name + '_' + cls.__name__,
            (cls, lang.Final),
            {
                'phase_pair': classmethod(lambda _: pp),
                '__module__': cls.__module__,
            },
        )
        cls._subclass_map[pp] = scls
        return scls

    @classmethod
    def _subclass(
            cls,
            p: Phase,
    ) -> ta.Tuple[
        ta.Type['_Scope'],
        ta.Type['_Scope'],
        ta.Type['_Scope'],
    ]:
        return tuple(
            cls._subclass_one(PhasePair(p, sp))
            for sp in SUB_PHASES
        )


PreBootstrap, Bootstrap, PostBootstrap = _Scope._subclass(Phases.BOOTSTRAP)
PreSites, Sites, PostSites = _Scope._subclass(Phases.SITES)
PreRules, Rules, PostRules = _Scope._subclass(Phases.RULES)
PreConnectors, Connectors, PostConnectors = _Scope._subclass(Phases.CONNECTORS)
PreTargets, Targets, PostTargets = _Scope._subclass(Phases.TARGETS)
PreFinalize, Finalize, PostFinalize = _Scope._subclass(Phases.FINALIZE)


class _CurrentScope(inj.Scope, lang.Final):

    def provide(self, binding: inj.Binding[T]) -> T:
        if binding.key == inj.Key(ElementSet):
            return check.isinstance(inj.Injector.current[InjectionElementProcessingDriver]._elements, ElementSet)
        else:
            raise NotImplementedError


class _Eager(dc.Pure):
    key: inj.Key


class InjectionElementProcessingDriver:

    def __init__(self, *binders: inj.Binder) -> None:
        super().__init__()

        binder = inj.create_binder()
        for s in _Scope._subclass_map.values():
            binder._elements.append(inj.types.ScopeBinding(s))
            binder.new_set_binder(_Eager, annotated_with=s.phase_pair(), in_=s)
            if s.phase_pair().sub_phase == SubPhases.MAIN:
                binder.new_set_binder(ElementProcessor, annotated_with=s.phase_pair().phase, in_=s)

        binder.bind(InjectionElementProcessingDriver, to_instance=self)

        binder._elements.append(inj.types.ScopeBinding(_CurrentScope))
        binder.bind_callable(lambda: lang.raise_(RuntimeError), key=inj.Key(ElementSet), in_=_CurrentScope)

        binder.bind_class(ElementProcessingDriver, assists={'processor_factory'})

        self._injector = inj.create_injector(binder, *binders)

        self._scopes: ta.Mapping[PhasePair, _Scope] = {
            s.phase_pair(): self._injector._scopes[s]
            for s in _Scope._subclass_map.values()
        }
        self._scope_states: ta.Mapping[_Scope, _Scope.State] = {}

        self._elements: ta.Optional[ElementSet] = None

    def __getitem__(
            self,
            target: ta.Union[inj.Key[T], ta.Type[T]],
    ) -> T:
        return self._injector[target]

    def run(self, elements: ta.Iterable[Element]) -> ElementSet:
        def enter(s: _Scope) -> None:
            check.not_in(s, self._scope_states)
            self._scope_states[s] = _Scope.State()
            eags = self._injector[inj.Key(ta.AbstractSet[_Eager], s.phase_pair())]
            for eag in eags:
                self._injector[eag.key]  # noqa

        def freeze(s: _Scope) -> None:
            state = self._scope_states[s]
            check.state(not state.frozen)
            state.frozen = True

        def exit(s: _Scope) -> None:
            del self._scope_states[s]

        cur_phase: ta.Optional[Phase] = None

        def fac(elements: ElementSet, phase: Phase) -> ta.Iterable[ElementProcessor]:
            nonlocal cur_phase

            if cur_phase is not None:
                self._elements = elements
                enter(self._scopes[PhasePair(cur_phase, SubPhases.POST)])
                self._elements = None
                freeze(self._scopes[PhasePair(cur_phase, SubPhases.POST)])

                exit(self._scopes[PhasePair(cur_phase, SubPhases.MAIN)])
                exit(self._scopes[PhasePair(cur_phase, SubPhases.PRE)])

            cur_phase = phase

            enter(self._scopes[PhasePair(cur_phase, SubPhases.PRE)])
            enter(self._scopes[PhasePair(cur_phase, SubPhases.MAIN)])

            return self._injector[inj.Key(ta.AbstractSet[ElementProcessor], phase)]

        with self._injector._CURRENT(self._injector):
            epd = self._injector[ta.Callable[..., ElementProcessingDriver]](processor_factory=fac)
        elements = epd.process(elements)

        return elements


def get_scope(phase_pair: PhasePair) -> ta.Type[inj.Scope]:
    check.isinstance(phase_pair, PhasePair)
    return _Scope._subclass_map[phase_pair]


def get_phases(phases: ta.Union[Phase, ta.Iterable[Phase]]) -> ta.AbstractSet[Phase]:
    if isinstance(phases, Phase):
        return {phases}
    elif isinstance(phases, ta.Iterable):
        return {check.isinstance(p, Phase) for p in phases}
    else:
        raise TypeError(phases)


def bind_element_processor(
        binder: inj.Binder,
        cls: ta.Type[ElementProcessor],
        phases: ta.Union[Phase, ta.Iterable[Phase]],
) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, ElementProcessor)

    for phase in get_phases(phases):
        check.isinstance(phase, Phase)
        scope = get_scope(PhasePair(phase, SubPhases.MAIN))

        binder.bind(cls, annotated_with=phase, in_=scope)
        binder.new_set_binder(ElementProcessor, annotated_with=phase, in_=scope).bind(to=inj.Key(cls, phase))


def bind_post_eager(
        binder: inj.Binder,
        key: ta.Union[inj.Key, ta.Type],
        phases: ta.Union[Phase, ta.Iterable[Phase]],
) -> None:
    check.isinstance(binder, inj.Binder)
    if not isinstance(key, inj.Key):
        key = inj.Key(key)

    for phase in get_phases(phases):
        phase_pair = PhasePair(phase, SubPhases.POST)
        scope = get_scope(phase_pair)

        binder.new_set_binder(_Eager, annotated_with=phase_pair, in_=scope).bind(to_instance=_Eager(key))


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    bind_element_processor(binder, queries.QueryParsingElementProcessor, Phases.TARGETS)
    bind_element_processor(binder, processors.IdGeneratorProcessor, PHASES)

    return binder
