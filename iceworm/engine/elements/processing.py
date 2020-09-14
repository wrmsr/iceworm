"""
TODO:
 - add id's
 - add deps
 - find / warn / reject elements with no processors
  - processed_cls_set? optional, enforced if present, warn
 - enforce only modified ids that matched (or added new)
 - ** timing, + detect infinite loops **
  - max iterations?
  - 'aspect_id' tagging equiv - 'ProcessedBy' attribute?
 - ProcessedBy allowed to be updated but only for self, added if not
 - RULES phase - keep? serde already bound lol, can't load any dynamic rule types yet.. *yet*.. nuke serde ctx?
 - subphases - use to combine transforms and validations? like disable mutation in POST?
 - class Phase(dc.Pure): name: str, mutable_element_types: ta.AbstractSet[type], ...
 - decompose? need to setup ctors before instantiating next phases lol..
 - secrets processor - url: str, url_secret: Secret = dc.field(metadata={els.SecretField: 'url')
 - phase inj scope?
 - overlap w/ tree xforms? passes? no cuz flat?
 - support / enforce els.Frozen
  - added by phase * in addition to rejecting addition of phase-frozen types *
 - ** enforce origin propagation somehow - require for ids? auto-add for ids? **
 - if mem is an issue strip origins unless explicitly kept
"""
import abc
import itertools
import typing as ta
import weakref

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import properties

from .base import Element
from .base import Frozen
from .collections import ElementSet
from .phases import PHASES
from .phases import Phase


InstanceElementProcessorT = ta.TypeVar('InstanceElementProcessorT', bound='InstanceElementProcessor')


class ProcessedBy(dc.Pure):
    processors: ta.AbstractSet['ElementProcessor'] = dc.field(
        coerce=lambda o: ocol.IdentitySet(check.not_isinstance(o, str)) if not isinstance(o, ocol.IdentitySet) else o,
        check=lambda o: isinstance(o, ocol.IdentitySet) and all(isinstance(e, ElementProcessor) for e in o))


class PhaseFrozen(dc.Pure):
    phase: Phase = dc.field(check=lambda o: isinstance(o, Phase))


_PHASE_FROZEN_CACHE = weakref.WeakKeyDictionary()


def _phase_frozen(cls: type) -> ta.Optional[Phase]:
    try:
        return _PHASE_FROZEN_CACHE[cls]
    except KeyError:
        check.issubclass(cls, Element)
        pfi = dc.metadatas_dict(cls).get(PhaseFrozen)
        if pfi is not None:
            pf = check.isinstance(pfi, PhaseFrozen).phase
        else:
            pf = None
        _PHASE_FROZEN_CACHE[cls] = pf
        return pf


def has_processed(ep: 'ElementProcessor', e: Element) -> bool:
    check.isinstance(ep, ElementProcessor)
    check.isinstance(e, Element)
    try:
        pb = e.meta[ProcessedBy]
    except KeyError:
        return False
    else:
        return ep in check.isinstance(pb, ProcessedBy).processors


class ElementProcessor(lang.Abstract):

    @classmethod
    def phases(cls) -> ta.Iterable[Phase]:
        return PHASES

    @classmethod
    def dependencies(cls) -> ta.Iterable[ta.Type['ElementProcessor']]:
        return []

    @abc.abstractmethod
    def match(self, elements: ElementSet) -> ta.Iterable[Element]:
        raise NotImplementedError

    @abc.abstractmethod
    def process(self, elements: ElementSet) -> ta.Iterable[Element]:
        raise NotImplementedError


class InstanceElementProcessor(ElementProcessor, lang.Abstract):

    class Instance(ta.Generic[InstanceElementProcessorT], lang.Abstract):

        def __init__(self, owner: InstanceElementProcessorT, input: ElementSet) -> None:
            super().__init__()

            self.__owner = check.isinstance(owner, self._owner_cls)
            self.__input = check.isinstance(input, ElementSet)

        _owner_cls: ta.ClassVar[ta.Type[InstanceElementProcessorT]]

        @property
        def owner(self) -> InstanceElementProcessorT:
            return self.__owner

        @property
        def input(self) -> ElementSet:
            return self.__input

        @abc.abstractproperty
        def matches(self) -> ta.AbstractSet[Element]:
            raise NotImplementedError

        @abc.abstractproperty
        def output(self) -> ElementSet:
            raise NotImplementedError

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        lang.check_finals(cls, InstanceElementProcessor)
        inst_cls = check.issubclass(cls.__dict__['Instance'], InstanceElementProcessor.Instance)
        inst_cls._owner_cls = cls

    _instance_cache: ta.MutableMapping[ElementSet, Instance] = properties.cached(lambda self: weakref.WeakKeyDictionary())  # noqa

    def _get_instance(self, elements: ElementSet) -> Instance:
        try:
            return self._instance_cache[elements]
        except KeyError:
            inst = self._instance_cache[elements] = self.Instance(self, elements)
            return inst

    @lang.final
    def match(self, elements: ElementSet) -> ta.Iterable[Element]:
        inst = self._get_instance(elements)
        check.state(inst.input is elements)
        return inst.matches

    @lang.final
    def process(self, elements: ElementSet) -> ta.Iterable[Element]:
        inst = self._get_instance(elements)
        check.state(inst.input is elements)
        return inst.output


ElementProcessorFactory = ta.Callable[[ElementSet, Phase], ta.Iterable[ElementProcessor]]


class ElementProcessingDriver:

    def __init__(self, processor_factory: ElementProcessorFactory) -> None:
        super().__init__()

        self._processor_factory = check.callable(processor_factory)

    @classmethod
    def build_factory(cls, processors: ta.Iterable[ElementProcessor]) -> ElementProcessorFactory:
        lst = []
        seen = ocol.IdentitySet()
        by_phase = {}
        for ep in processors:
            check.isinstance(ep, ElementProcessor)
            check.not_in(ep, seen)
            lst.append(ep)
            for p in set(type(ep).phases()):
                check.isinstance(p, Phase)
                by_phase.setdefault(p, []).append(ep)
            seen.add(ep)
        processor_seqs_by_phase: ta.Mapping[Phase, ta.Sequence[ElementProcessor]] = by_phase
        return lambda es, phase: processor_seqs_by_phase.get(phase, [])

    def process(self, elements: ta.Iterable[Element]) -> ElementSet:
        elements = ElementSet.of(elements)

        for phase in PHASES:
            eps = [check.isinstance(ep, ElementProcessor) for ep in self._processor_factory(elements, phase)]
            ep_dep_tys = {}
            ep_sets_by_mro_cls = {}
            for ep in eps:
                check.not_in(ep, ep_dep_tys)
                check.in_(phase, type(ep).phases())
                ep_dep_tys[ep] = {check.issubclass(d, ElementProcessor) for d in type(ep).dependencies()}
                for mro_cls in type(ep).__mro__:
                    if issubclass(mro_cls, ElementProcessor) and mro_cls != ElementProcessor:
                        ep_sets_by_mro_cls.setdefault(mro_cls, set()).add(ep)

            if ep_dep_tys:
                ep_deps = {
                    ep: {dep for dt in dts for dep in check.not_empty(ep_sets_by_mro_cls[dt])}
                    for ep, dts in ep_dep_tys.items()
                }
                steps = list(ocol.toposort(ep_deps))
            else:
                steps = [eps]

            count = 0
            history = []
            while True:
                count += 1

                dct: ta.MutableMapping[ElementProcessor, ta.AbstractSet[Element]] = ocol.IdentityKeyDict()
                for step in steps:
                    for ep in step:
                        epes = ocol.IdentitySet(check.isinstance(e, Element) for e in ep.match(elements))
                        if epes:
                            check.empty([e for e in epes if Frozen in e.meta])
                            dct[ep] = epes
                    if dct:
                        break
                if not dct:
                    break

                cur, cures = next(iter(dct.items()))
                history.append(cur)
                expected = [e for e in elements if e not in cures]
                res = ElementSet.of(cur.process(elements))

                missing = [e for e in expected if e not in res]
                if missing:
                    raise ValueError(missing)

                leftover = [e for e in cures if e in res]
                if leftover:
                    # Need to consume all matched or it'll inf loop..
                    raise ValueError(leftover)

                swaps: ta.MutableMapping[Element, Element] = ocol.IdentityKeyDict()

                added = [e for e in res if e not in elements]
                removed = [e for e in elements if e not in res]  # noqa

                for e in itertools.chain(added, removed):
                    pf = _phase_frozen(type(e))
                    if pf is not None and pf < phase:
                        raise ValueError(e, pf)

                for e in added:
                    pbs = e.meta.get(ProcessedBy)
                    if pbs is not None:
                        npbs = check.isinstance(pbs, ProcessedBy).processors
                        if cur in npbs:
                            continue
                    else:
                        npbs = []
                    swaps[e] = dc.replace(
                        e,
                        meta={
                            **e.meta,
                            ProcessedBy: ProcessedBy([*npbs, cur]),
                        },
                    )

                if swaps:
                    res = ElementSet.of(swaps.get(e, e) for e in res)

                elements = res

            elements = ElementSet.of([
                dc.replace(e, meta={**e.meta, Frozen: Frozen})
                if pf is not None and phase == pf and Frozen not in e.meta else e
                for e in elements
                for pf in [_phase_frozen(type(e))]
            ])

        return elements
