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
from omnibus import dynamic as dyn
from omnibus import inject as inj
from omnibus import lang
import omnibus.inject.scopes  # noqa

from . import processors
from . import queries
from . import validations
from .base import Element
from .collections import ElementSet
from .phases import PHASES
from .phases import Phase
from .phases import PhasePair
from .phases import Phases
from .phases import SUB_PHASES
from .phases import SubPhases
from .processing import DriverItem
from .processing import ElementProcessingDriver
from .processing import ElementProcessor


T = ta.TypeVar('T')


class DriverScope(inj.Scope, lang.Final):

    def provide(self, binding: inj.Binding[T]) -> T:
        vals = self._CURRENT()
        try:
            return vals[binding]
        except KeyError:
            try:
                val = vals[binding.key.type]
            except KeyError:
                val = binding.provide()
            vals[binding] = val
            return val

    _CURRENT: dyn.Var[ta.MutableMapping[ta.Union[type, inj.Binding], ta.Any]] = dyn.Var()  # noqa


@dyn.contextmanager
def new_driver_scope(injector: inj.Injector) -> ta.Generator['InjectionElementProcessingDriver', None, None]:
    check.isinstance(injector, inj.Injector)
    vals = ocol.IdentityKeyDict()
    with DriverScope._CURRENT(vals):
        with injector._CURRENT(injector):
            drv = vals[InjectionElementProcessingDriver] = InjectionElementProcessingDriver(injector)
        yield drv


class _PhaseScope(inj.Scope, lang.Abstract, lang.Sealed):

    class State(dc.Data, final=True):
        values: ta.MutableMapping[inj.Binding, ta.Any] = dc.field(default_factory=ocol.IdentityKeyDict, frozen=True)  # noqa
        frozen: bool = False

    @abc.abstractclassmethod
    def phase_pair(cls) -> PhasePair:
        raise NotImplementedError

    def provide(self, binding: inj.Binding[T]) -> T:
        drv = inj.Injector.current[InjectionElementProcessingDriver]
        state = drv._phase_scope_states[self]
        if binding.key == inj.Key(Phase):
            return self.phase_pair().phase
        try:
            return state.values[binding]
        except KeyError:
            check.state(not state.frozen)
            value = state.values[binding] = binding.provider()
            return value

    _subclass_map: ta.Mapping[PhasePair, ta.Type['_PhaseScope']] = {}

    @classmethod
    def _subclass_one(cls, pp: PhasePair) -> ta.Type['_PhaseScope']:
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
        ta.Type['_PhaseScope'],
        ta.Type['_PhaseScope'],
        ta.Type['_PhaseScope'],
    ]:
        return tuple(
            cls._subclass_one(PhasePair(p, sp))
            for sp in SUB_PHASES
        )


PreBootstrap, Bootstrap, PostBootstrap = _PhaseScope._subclass(Phases.BOOTSTRAP)
PreSites, Sites, PostSites = _PhaseScope._subclass(Phases.SITES)
PreRules, Rules, PostRules = _PhaseScope._subclass(Phases.RULES)
PreConnectors, Connectors, PostConnectors = _PhaseScope._subclass(Phases.CONNECTORS)
PreTargets, Targets, PostTargets = _PhaseScope._subclass(Phases.TARGETS)
PrePlan, Plan, PostPlan = _PhaseScope._subclass(Phases.PLAN)
PreFinalize, Finalize, PostFinalize = _PhaseScope._subclass(Phases.FINALIZE)


class _CurrentPhaseScope(inj.Scope, lang.Final):

    def provide(self, binding: inj.Binding[T]) -> T:
        if binding.key == inj.Key(ElementSet):
            return check.isinstance(inj.Injector.current[InjectionElementProcessingDriver]._elements, ElementSet)
        else:
            raise NotImplementedError


class _Eager(dc.Pure):
    key: inj.Key


class InjectionElementProcessingDriver:

    def __init__(self, injector: inj.Injector) -> None:
        super().__init__()

        self._injector = check.isinstance(injector, inj.Injector)

        self._phase_scopes: ta.Mapping[PhasePair, _PhaseScope] = {
            s.phase_pair(): self._injector._scopes[s]
            for s in _PhaseScope._subclass_map.values()
        }
        self._phase_scope_states: ta.Mapping[_PhaseScope, _PhaseScope.State] = {}

        self._elements: ta.Optional[ElementSet] = None

    def __getitem__(
            self,
            target: ta.Union[inj.Key[T], ta.Type[T]],
    ) -> T:
        return self._injector[target]

    def run(self, elements: ta.Iterable[Element]) -> ElementSet:
        def enter(s: _PhaseScope) -> None:
            check.not_in(s, self._phase_scope_states)
            self._phase_scope_states[s] = _PhaseScope.State()
            eags = self._injector[inj.Key(ta.AbstractSet[_Eager], s.phase_pair())]
            for eag in eags:
                self._injector[eag.key]  # noqa

        def freeze(s: _PhaseScope) -> None:
            state = self._phase_scope_states[s]
            check.state(not state.frozen)
            state.frozen = True

        def exit(s: _PhaseScope) -> None:
            del self._phase_scope_states[s]

        cur_phase: ta.Optional[Phase] = None

        def fac(elements: ElementSet, phase: Phase) -> ta.Iterable[DriverItem]:
            nonlocal cur_phase

            if cur_phase is not None:
                self._elements = elements
                enter(self._phase_scopes[PhasePair(cur_phase, SubPhases.POST)])
                self._elements = None
                freeze(self._phase_scopes[PhasePair(cur_phase, SubPhases.POST)])

                exit(self._phase_scopes[PhasePair(cur_phase, SubPhases.MAIN)])
                exit(self._phase_scopes[PhasePair(cur_phase, SubPhases.PRE)])

            cur_phase = phase

            enter(self._phase_scopes[PhasePair(cur_phase, SubPhases.PRE)])
            enter(self._phase_scopes[PhasePair(cur_phase, SubPhases.MAIN)])

            eps = self._injector[inj.Key(ta.AbstractSet[ElementProcessor], phase)]
            vals = self._injector[inj.Key(ta.AbstractSet[ta.Type[validations.Validation]], phase)]
            return [*eps, *vals]

        with self._injector._CURRENT(self._injector):
            epd = self._injector[ta.Callable[..., ElementProcessingDriver]](factory=fac)
        elements = epd.process(elements)

        return elements


def get_phase_scope(phase_pair: PhasePair) -> ta.Type[inj.Scope]:
    check.isinstance(phase_pair, PhasePair)
    return _PhaseScope._subclass_map[phase_pair]


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
        phases: ta.Union[Phase, ta.Iterable[Phase], None] = None,
) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, ElementProcessor)

    if phases is None:
        phases = set(cls.phases())

    for phase in get_phases(phases):
        check.isinstance(phase, Phase)
        scope = get_phase_scope(PhasePair(phase, SubPhases.MAIN))

        binder.bind(cls, annotated_with=phase, in_=scope)
        binder.new_set_binder(ElementProcessor, annotated_with=phase, in_=scope).bind(to=inj.Key(cls, phase))


def bind_validation(
        binder: inj.Binder,
        cls: ta.Type[validations.Validation],
        phases: ta.Union[Phase, ta.Iterable[Phase], None] = None,
) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, validations.Validation)

    if phases is None:
        phases = PHASES

    for phase in get_phases(phases):
        check.isinstance(phase, Phase)
        scope = get_phase_scope(PhasePair(phase, SubPhases.MAIN))

        binder.new_set_binder(ta.Type[validations.Validation], annotated_with=phase, in_=scope).bind(to_instance=cls)


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
        scope = get_phase_scope(phase_pair)

        binder.new_set_binder(_Eager, annotated_with=phase_pair, in_=scope).bind(to_instance=_Eager(key))


def _install_elements(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    for s in _PhaseScope._subclass_map.values():
        binder._elements.append(inj.types.ScopeBinding(s))
        binder.new_set_binder(_Eager, annotated_with=s.phase_pair(), in_=s)
        if s.phase_pair().sub_phase == SubPhases.MAIN:
            binder.new_set_binder(ElementProcessor, annotated_with=s.phase_pair().phase, in_=s)
            binder.new_set_binder(ta.Type[validations.Validation], annotated_with=s.phase_pair().phase, in_=s)

    binder._elements.append(inj.types.ScopeBinding(DriverScope))
    binder.bind(InjectionElementProcessingDriver, in_=DriverScope)

    binder._elements.append(inj.types.ScopeBinding(_CurrentPhaseScope))
    binder.bind_callable(lambda: lang.raise_(RuntimeError), key=inj.Key(ElementSet), in_=_CurrentPhaseScope)

    binder.bind_class(ElementProcessingDriver, assists={'factory'})

    bind_element_processor(binder, queries.QueryParsingElementProcessor, Phases.TARGETS)
    bind_element_processor(binder, processors.IdGeneratorProcessor, PHASES)
    bind_validation(binder, validations.RefValidation)

    return binder


def bind_elements_module(binder: inj.Binder, module: ta.Callable[[inj.Binder], ta.Any]) -> None:
    check.isinstance(binder, inj.Binder)
    check.callable(module)

    binder.new_set_binder(ta.Callable[[inj.Binder], None], annotated_with='elements').bind(to_instance=module)


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    def check_binds(injector: inj.Injector) -> None:
        for s in _PhaseScope._subclass_map.values():
            if s.phase_pair().sub_phase == SubPhases.MAIN:
                check.empty(injector[inj.Key(ta.AbstractSet[ElementProcessor], s.phase_pair().phase)])

    for s in _PhaseScope._subclass_map.values():
        if s.phase_pair().sub_phase == SubPhases.MAIN:
            binder.new_set_binder(ElementProcessor, annotated_with=s.phase_pair().phase)
    binder.bind_callable(check_binds, key=inj.Key(object, check_binds), as_eager_singleton=True)

    bind_elements_module(binder, _install_elements)

    @inj.annotate('elements', mods='elements')
    def provide_elements_injector(injector: inj.Injector, mods: ta.AbstractSet[ta.Callable[[inj.Binder], None]]) -> inj.Injector:  # noqa
        bnd = inj.create_binder()
        for mod in mods:
            mod(bnd)
        return injector.create_child(bnd)

    binder.bind_callable(provide_elements_injector, as_eager_singleton=True)

    return binder
