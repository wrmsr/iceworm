"""
TODO:
 - add id's
 - add deps
 - find / warn / reject elements with no processors
 - enforce only modified ids that matched (or added new)
 - ** timing, + detect infinite loops **
  - max iterations?
"""
import abc
import typing as ta

from omnibus import lang

from .base import Id
from .collections import ElementSet


class ElementProcessor(lang.Abstract):

    @abc.abstractmethod
    def processes(self, elements: ElementSet) -> ta.AbstractSet[Id]:
        raise NotImplementedError

    @abc.abstractmethod
    def process(self, elements: ElementSet) -> ElementSet:
        raise NotImplementedError
