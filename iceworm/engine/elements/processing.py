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

        self._processors = [check.isinstance(p, ElementProcessor) for p in processors]

    def process(self, elements: ta.Iterable[Element]) -> ElementSet:
        elements = ElementSet.of(elements)
        while True:
            mtps = [tp for tp in self._processors if tp.processes(elements)]
            if not mtps:
                break
            elements = ElementSet.of(mtps[0].process(elements))
        return elements
