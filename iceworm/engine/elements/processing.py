import abc

from omnibus import lang

from .collections import ElementSet


class ElementProcessor(lang.Abstract):

    @abc.abstractmethod
    def matches(self, elements: ElementSet) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def process(self, elements: ElementSet) -> ElementSet:
        raise NotImplementedError
