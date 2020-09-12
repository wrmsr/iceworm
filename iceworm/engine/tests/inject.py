import abc
import contextlib
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import inject as inj
from omnibus import lang
import omnibus.inject.scopes  # noqa

from .. import connectors as ctrs
from .. import elements as els
from .. import inference as infr
from .. import rules as rls
from .. import sites
from .test_ops import UrlSecretsReplacer


T = ta.TypeVar('T')


class _InjectorScope(inj.scopes.Scope, lang.Abstract, lang.Sealed):

    def __init__(self) -> None:
        super().__init__()

        self._state: ta.Optional[_InjectorScope.State] = None

    class State(dc.Pure):
        values: ta.MutableMapping[inj.types.Binding, ta.Any] = dc.field(default_factory=ocol.IdentityKeyDict)

    @abc.abstractclassmethod
    def phase_pair(cls) -> els.PhasePair:
        raise NotImplementedError

    def enter(self) -> None:
        check.none(self._state)
        self._state = self.State()

    def exit(self) -> None:
        check.not_none(self._state)
        self._state = None

    def provide(self, binding: inj.types.Binding[T]) -> T:
        check.not_none(self._state)
        if binding.key == inj.Key(els.Phase):
            return self.phase_pair().phase
        try:
            return self._state.values[binding]
        except KeyError:
            value = self._state.values[binding] = binding.provider()
            return value

    _subclass_map: ta.Mapping[els.PhasePair, ta.Type['_InjectorScope']] = {}

    @classmethod
    def _subclass_one(cls, pp: els.PhasePair) -> ta.Type['_InjectorScope']:
        check.isinstance(pp, els.PhasePair)
        check.not_in(pp, cls._subclass_map)
        scls = type(
            pp.name + '_' + cls.__name__,
            (cls, lang.Final,),
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
            p: els.Phase,
    ) -> ta.Tuple[
        ta.Type['_InjectorScope'],
        ta.Type['_InjectorScope'],
        ta.Type['_InjectorScope'],
    ]:
        return tuple(
            cls._subclass_one(els.PhasePair(p, sp))
            for sp in els.SUB_PHASES
        )


PreBootstrap, Bootstrap, PostBootstrap = _InjectorScope._subclass(els.Phases.BOOTSTRAP)
PreSites, Sites, PostSites = _InjectorScope._subclass(els.Phases.SITES)
PreRules, Rules, PostRules = _InjectorScope._subclass(els.Phases.RULES)
PreConnectors, Connectors, PostConnectors = _InjectorScope._subclass(els.Phases.CONNECTORS)
PreTargets, Targets, PostTargets = _InjectorScope._subclass(els.Phases.TARGETS)
PreFinalize, Finalize, PostFinalize = _InjectorScope._subclass(els.Phases.FINALIZE)


class _CurrentInjectorScope(inj.scopes.Scope, lang.Final):

    def provide(self, binding: inj.types.Binding[T]) -> T:
        if binding.key == inj.Key(els.ElementSet):
            return check.isinstance(inj.Injector.current[_Driver]._elements, els.ElementSet)
        else:
            raise NotImplementedError


class _Eager(dc.Pure):
    key: inj.Key


class _Driver:

    def __init__(self, *binders: inj.Binder) -> None:
        super().__init__()

        binder = inj.create_binder()
        for s in _InjectorScope._subclass_map.values():
            binder._elements.append(inj.types.ScopeBinding(s))
            binder.new_set_binder(_Eager, annotated_with=s.phase_pair(), in_=s)
            if s.phase_pair().sub_phase == els.SubPhases.MAIN:
                binder.new_set_binder(els.ElementProcessor, annotated_with=s.phase_pair().phase, in_=s)
                binder.new_set_binder(rls.RuleProcessor, annotated_with=s.phase_pair().phase, in_=s)

        binder.bind(_Driver, to_instance=self)

        binder._elements.append(inj.types.ScopeBinding(_CurrentInjectorScope))
        binder.bind_callable(lambda: lang.raise_(RuntimeError), key=inj.Key(els.ElementSet), in_=_CurrentInjectorScope)

        self._injector = inj.create_injector(binder, *binders)

        self._scopes: ta.Mapping[els.PhasePair, _InjectorScope] = {
            s.phase_pair(): self._injector._scopes[s]
            for s in _InjectorScope._subclass_map.values()
        }

        self._elements: ta.Optional[els.ElementSet] = None

    def run(self, elements: ta.Iterable[els.Element]) -> els.ElementSet:
        def enter(s: _InjectorScope) -> None:
            s.enter()
            eags = self._injector[inj.Key(ta.Set[_Eager], s.phase_pair())]
            for eag in eags:
                self._injector[eag.key]  # noqa

        cur_phase: ta.Optional[els.Phase] = None

        def fac(elements: els.ElementSet, phase: els.Phase) -> ta.Iterable[els.ElementProcessor]:
            nonlocal cur_phase

            if cur_phase is not None:
                self._elements = elements
                enter(self._scopes[els.PhasePair(cur_phase, els.SubPhases.POST)])
                self._elements = None

                self._scopes[els.PhasePair(cur_phase, els.SubPhases.MAIN)].exit()
                self._scopes[els.PhasePair(cur_phase, els.SubPhases.PRE)].exit()

            cur_phase = phase

            enter(self._scopes[els.PhasePair(cur_phase, els.SubPhases.PRE)])
            enter(self._scopes[els.PhasePair(cur_phase, els.SubPhases.MAIN)])

            return self._injector[inj.Key(ta.Set[els.ElementProcessor], phase)]

        epd = els.ElementProcessingDriver(fac)
        elements = epd.process(elements)

        for s in reversed(list(self._scopes.values())):
            if s._state is not None:
                s.exit()

        return elements


def install(binder: inj.Binder) -> inj.Binder:
    binder.bind(sites.SiteProcessor, in_=Sites)
    binder.new_set_binder(els.ElementProcessor, annotated_with=els.Phases.SITES, in_=Sites).bind(to=sites.SiteProcessor)  # noqa

    binder.bind(UrlSecretsReplacer, in_=Connectors)
    binder.new_set_binder(els.ElementProcessor, annotated_with=els.Phases.CONNECTORS, in_=Connectors).bind(to=UrlSecretsReplacer)  # noqa

    binder.bind(rls.TableAsSelectProcessor, in_=Targets)
    binder.new_set_binder(rls.RuleProcessor, annotated_with=els.Phases.TARGETS, in_=Targets).bind(to=rls.TableAsSelectProcessor)  # noqa
    binder.new_set_binder(els.ElementProcessor, annotated_with=els.Phases.TARGETS, in_=Targets).bind(to_provider=rls.RuleElementProcessor[rls.TableAsSelect])  # noqa

    def provide_table_as_select_rule_element_processor(rp: rls.TableAsSelectProcessor) -> rls.RuleElementProcessor[rls.TableAsSelect]:  # noqa
        return rls.RuleElementProcessor(rp)
    binder.bind_callable(provide_table_as_select_rule_element_processor, in_=Targets)

    binder.bind(infr.InferTableProcessor, in_=Targets)
    binder.new_set_binder(els.ElementProcessor, annotated_with=els.Phases.TARGETS, in_=Targets).bind(to=infr.InferTableProcessor)  # noqa

    def provide_connector_set(es: els.ElementSet) -> ctrs.ConnectorSet:
        return ctrs.ConnectorSet.of(es.get_type_set(ctrs.Connector.Config))
    binder.bind_callable(provide_connector_set, in_=PostConnectors)

    return binder
