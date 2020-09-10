import abc
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


def run(*binders: inj.Binder) -> None:
    ib = inj.create_binder()
    for p in _InjectorScope._subclass_map.values():
        ib._elements.append(inj.types.ScopeBinding(p))
        ib.new_set_binder(els.ElementProcessor, annotated_with=p.phase(), in_=p)
        ib.new_set_binder(rls.RuleProcessor, annotated_with=p.phase(), in_=p)

    injector = inj.create_injector(ib, *binders)

    print(injector)

    scopes: ta.Mapping[els.processing.Phase, _InjectorScope] = {
        s.phase(): injector._scopes[s]
        for s in _InjectorScope._subclass_map.values()
    }

    for s in scopes.values():
        s.enter()
        try:
            eps = injector[inj.Key(ta.Set[els.ElementProcessor], s.phase())]
            for ep in eps:
                print(ep)
        finally:
            s.exit()


def install(binder: inj.Binder) -> inj.Binder:
    binder.bind(sites.SiteProcessor, in_=Sites)
    binder.new_set_binder(els.ElementProcessor, annotated_with=els.processing.Phases.SITES, in_=Sites).bind(to=sites.SiteProcessor)  # noqa

    binder.bind(UrlSecretsReplacer, in_=Connectors)
    binder.new_set_binder(els.ElementProcessor, annotated_with=els.processing.Phases.CONNECTORS, in_=Connectors).bind(to=UrlSecretsReplacer)  # noqa

    binder.bind(rls.TableAsSelectProcessor, in_=Targets)
    binder.new_set_binder(rls.RuleProcessor, annotated_with=els.processing.Phases.TARGETS, in_=Targets).bind(to=rls.TableAsSelectProcessor)  # noqa
    def provide_table_as_select_rule_element_processor(rp: rls.TableAsSelectProcessor) -> rls.RuleElementProcessor[rls.TableAsSelect]:  # noqa
        return rls.RuleElementProcessor(rp)
    binder.new_set_binder(els.ElementProcessor, annotated_with=els.processing.Phases.TARGETS, in_=Targets).bind(to_provider=rls.RuleElementProcessor[rls.TableAsSelect])  # noqa
    binder.bind_callable(provide_table_as_select_rule_element_processor, in_=Targets)

    binder.bind(infr.InferTableProcessor, in_=Targets)
    binder.new_set_binder(els.ElementProcessor, annotated_with=els.processing.Phases.TARGETS, in_=Targets).bind(to=infr.InferTableProcessor)  # noqa

    binder.bind_callable(lambda: lang.raise_(Exception), key=inj.Key(ctrs.ConnectorSet))

    return binder
