import abc
import typing as ta
import weakref

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import defs
from omnibus import lang
from omnibus import properties

from .analyses import IdGen
from .base import Dependable
from .base import Element
from .base import Origin
from .collections import ElementSet
from .phases import PHASES
from .phases import Phase


InstanceElementProcessorT = ta.TypeVar('InstanceElementProcessorT', bound='InstanceElementProcessor')


class ElementProcessor(Dependable, lang.Abstract):

    defs.repr('key')

    @property
    def key(self) -> ta.Mapping[str, ta.Any]:
        return {}

    @classmethod
    def phases(cls) -> ta.Iterable[Phase]:
        return PHASES

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
        def matches(self) -> ta.Iterable[Element]:
            raise NotImplementedError

        @abc.abstractproperty
        def output(self) -> ta.Iterable[Element]:
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


class IdGeneratorProcessor(InstanceElementProcessor):

    class Instance(InstanceElementProcessor.Instance['IdGeneratorProcessor']):

        @properties.cached
        def matches(self) -> ta.Iterable[Element]:
            return [e for e in self.input if e.id is None]

        @properties.cached
        def output(self) -> ta.Iterable[Element]:
            ng = self.input.analyze(IdGen).name_gen
            return [
                dc.replace(
                    e,
                    id=ng(f'_{type(e).__name__}_'),
                    meta={Origin: Origin(e)},
                )
                if e.id is None else e
                for e in self.input
            ]
