import typing as ta

from omnibus import check
from omnibus import collections as ocol

from .base import Element
from .base import Id
from .refs import Ref


T = ta.TypeVar('T"')
ElementT = ta.TypeVar('ElementT', bound='Element')


class ElementSet(ta.Generic[ElementT]):

    def __init__(self, elements: ta.Iterable[ElementT]) -> None:
        super().__init__()

        self._elements = [check.isinstance(e, Element) for e in elements]

        self._element_set = ocol.IdentitySet(self._elements)
        by_id: ta.Dict[Id, ElementT] = {}
        for element in self._elements:
            if element.id is not None:
                check.not_in(element.id, by_id)
                by_id[element.id] = element
        self._elements_by_id: ta.Mapping[Id, ElementT] = by_id
        self._element_sets_by_type: ta.Dict[type, ta.AbstractSet[ElementT]] = {}

    @classmethod
    def of(cls, it: ta.Iterable[ElementT]) -> 'ElementSet[ElementT]':
        if isinstance(it, cls):
            return it
        else:
            return cls(it)

    def get_element_type_set(self, ty: ta.Type[T]) -> ta.AbstractSet[T]:
        try:
            return self._element_sets_by_type[ty]
        except KeyError:
            ret = self._element_sets_by_type[ty] = ocol.IdentitySet(n for n in self._elements if isinstance(n, ty))
            return ret

    def __iter__(self) -> ta.Iterator[ElementT]:
        return iter(self._elements)

    def __contains__(self, key: ta.Union[Id, ElementT, type]) -> bool:
        if isinstance(key, Id):
            return key in self._elements_by_id
        elif isinstance(key, Element):
            return key in self._element_set
        elif isinstance(key, type):
            return bool(self.get_element_type_set(key))
        else:
            raise TypeError(key)

    def __getitem__(self, key: ta.Union[Ref, Id]) -> ElementT:
        if isinstance(key, Ref):
            ele = self._elements_by_id[key.id]
            if not isinstance(ele, key.ele_cls):
                raise TypeError(ele, key)
            return ele
        elif isinstance(key, Id):
            return self._elements_by_id[key]
        else:
            raise TypeError(key)
