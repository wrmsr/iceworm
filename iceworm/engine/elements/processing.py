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

from .base import Element
from .base import Frozen
from .collections import ElementSet
from .phases import Phase
from .phases import Phases


class ProcessedBy(dc.Pure):
    processors: ta.AbstractSet['ElementProcessor'] = dc.field(check=lambda o: isinstance(o, ocol.IdentitySet))


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


class ElementProcessor(lang.Abstract):

    @classmethod
    def phases(cls) -> ta.Iterable[Phase]:
        return Phases.all()

    @abc.abstractmethod
    def processes(self, elements: ElementSet) -> ta.Iterable[Element]:
        raise NotImplementedError

    @abc.abstractmethod
    def process(self, elements: ElementSet) -> ta.Iterable[Element]:
        raise NotImplementedError


ElementProcessorFactory = ta.Callable[[ElementSet, Phase], ta.Iterable[ElementProcessor]]


class ElementProcessingDriver:

    def __init__(self, processor_factory: ta.Iterable[ElementProcessor]) -> None:
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

        for phase in Phases.all():
            eps = [check.isinstance(ep, ElementProcessor) for ep in self._processor_factory(elements, phase)]
            seen = ocol.IdentitySet()
            for ep in eps:
                check.not_in(ep, seen)
                check.in_(phase, type(ep).phases())
                seen.add(ep)

            while True:
                dct: ta.MutableMapping[ElementProcessor, ta.AbstractSet[Element]] = ocol.IdentityKeyDict()
                for ep in eps:
                    epes = ocol.IdentitySet(check.isinstance(e, Element) for e in ep.processes(elements))
                    if epes:
                        check.empty([e for e in epes if Frozen in e.meta])
                        dct[ep] = epes
                if not dct:
                    break

                cur, cures = next(iter(dct.items()))
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
                        check.state(check.single(pbs) is cur)
                        continue
                    swaps[e] = dc.replace(e, meta={**e.meta, ProcessedBy: ocol.IdentitySet([cur])})

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
