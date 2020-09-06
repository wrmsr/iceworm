"""
TODO:
 - ElementSet/ElementSetImpl/ElementSetView? for only showing EP's unprocessed els?
 - debug mode and make ESet props lazy / eager iff debug?
  - auto-rerun with dbg on fail?
"""
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

        ele_set = ocol.IdentitySet()
        by_id: ta.Dict[Id, ElementT] = {}
        for ele in self._elements:
            check.not_in(ele, ele_set)
            if ele.id is not None:
                check.not_in(ele.id, by_id)
                by_id[ele.id] = ele
            ele_set.add(ele)
        self._by_id: ta.Mapping[Id, ElementT] = by_id
        self._set = ele_set

        self._sets_by_type: ta.Dict[type, ta.AbstractSet[ElementT]] = {}

    @property
    def set(self) -> ta.AbstractSet[Element]:
        return self._set

    @classmethod
    def of(cls, it: ta.Iterable[ElementT]) -> 'ElementSet[ElementT]':
        if isinstance(it, cls):
            return it
        else:
            return cls(it)

    def get_type_set(self, ty: ta.Type[T]) -> ta.AbstractSet[T]:
        try:
            return self._sets_by_type[ty]
        except KeyError:
            ret = self._sets_by_type[ty] = ocol.IdentitySet(n for n in self._elements if isinstance(n, ty))
            return ret

    def __iter__(self) -> ta.Iterator[ElementT]:
        return iter(self._elements)

    def __contains__(self, key: ta.Union[Id, ElementT, type]) -> bool:
        if isinstance(key, Id):
            return key in self._by_id
        elif isinstance(key, Element):
            return key in self._set
        elif isinstance(key, type):
            return bool(self.get_type_set(key))
        else:
            raise TypeError(key)

    def __getitem__(self, key: ta.Union[Ref, Id]) -> ElementT:
        if isinstance(key, Ref):
            ele = self._by_id[key.id]
            if not isinstance(ele, key.ele_cls):
                raise TypeError(ele, key)
            return ele
        elif isinstance(key, Id):
            return self._by_id[key]
        else:
            raise TypeError(key)
