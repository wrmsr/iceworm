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
"""
import abc
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import lang

from .base import Element
from .base import Id
from .collections import ElementSet


class Phase(lang.AutoEnum):
    BOOTSTRAP = ...
    SITES = ...
    RULES = ...
    CONNECTORS = ...
    TARGETS = ...
    FINALIZE = ...


class SubPhase(lang.AutoEnum):
    PRE = ...
    MAIN = ...
    POST = ...


class ElementProcessor(lang.Abstract):

    @abc.abstractmethod
    def processes(self, elements: ElementSet) -> ta.AbstractSet[Id]:
        raise NotImplementedError

    @abc.abstractmethod
    def process(self, elements: ElementSet) -> ElementSet:
        raise NotImplementedError


class ElementProcessingDriver:

    def __init__(self, processors: ta.Iterable[ElementProcessor]) -> None:
        super().__init__()

        lst = []
        seen = ocol.IdentitySet()
        for ep in processors:
            check.isinstance(ep, ElementProcessor)
            check.not_in(ep, seen)
            lst.append(ep)
            seen.add(ep)
        self._processors: ta.Sequence[ElementProcessor] = lst

    @property
    def processors(self) -> ta.Sequence[ElementProcessor]:
        return self._processors

    def process(self, elements: ta.Iterable[Element]) -> ElementSet:
        elements = ElementSet.of(elements)
        while True:
            dct: ta.MutableMapping[ElementProcessor, ta.AbstractSet[Id]] = ocol.IdentityKeyDict()
            for ep in self._processors:
                epids = ep.processes(elements)
                if epids:
                    dct[ep] = epids
            if not dct:
                break
            cur = next(iter(dct.keys()))
            elements = ElementSet.of(cur.process(elements))
        return elements
