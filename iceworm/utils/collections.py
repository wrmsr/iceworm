import typing as ta

from omnibus import check
from omnibus import collections as ocol


T = ta.TypeVar('T')
K = ta.TypeVar('K')
V = ta.TypeVar('V')
OrderingT = ta.Union[ta.Sequence[T], ocol.OrderedSet[T], ocol.OrderedFrozenSet[T]]
ORDERING_TYPES = (ta.Sequence, ocol.OrderedSet, ocol.OrderedFrozenSet)


def unique_dict(items: ta.Iterable[ta.Tuple[K, V]]) -> ta.Dict[K, V]:
    dct = {}
    for k, v in items:
        if k in dct:
            raise KeyError(k)
        dct[k] = v
    return dct


def seq(it: ta.Optional[ta.Iterable[T]]) -> ta.Optional[ta.Sequence[T]]:
    if it is None:
        return None
    elif isinstance(it, str):
        raise TypeError(it)
    else:
        return tuple(it)


def seq_or_none(it: ta.Optional[ta.Iterable[T]]) -> ta.Optional[ta.Sequence[T]]:
    if it is None:
        return None
    elif isinstance(it, str):
        raise TypeError(it)
    if isinstance(it, tuple):
        ret = it
    else:
        ret = tuple(it)
    if not ret:
        return None
    else:
        return ret


def mapping(obj: ta.Union[ta.Mapping[K, V], ta.Iterable[ta.Tuple[K, V]], None]) -> ta.Optional[ta.Mapping[K, V]]:
    if obj is None:
        return None
    elif isinstance(obj, str):
        raise TypeError(obj)
    else:
        return ocol.frozendict(obj)


def abs_set(it: ta.Optional[ta.Iterable[T]]) -> ta.Optional[ta.AbstractSet[T]]:
    if it is None:
        return None
    elif isinstance(it, str):
        raise TypeError(it)
    elif isinstance(it, frozenset):
        return it
    else:
        return frozenset(it)


def abs_set_or_none(it: ta.Optional[ta.Iterable[T]]) -> ta.Optional[ta.AbstractSet[T]]:
    if it is None:
        return None
    elif isinstance(it, str):
        raise TypeError(it)
    if isinstance(it, frozenset):
        ret = it
    else:
        ret = frozenset(it)
    if not ret:
        return None
    else:
        return ret


def order_values(values: ta.Container[T], ordering: OrderingT) -> ta.List[T]:
    check.isinstance(ordering, ORDERING_TYPES)
    lst = []
    seen = set()
    for v in ordering:
        if v in values and v not in seen:
            lst.append(v)
            seen.add(v)
    return lst


def order_set(values: ta.Container[T], ordering: OrderingT) -> ocol.OrderedSet[T]:
    return ocol.OrderedSet(order_values(values, ordering))


def order_frozen_set(values: ta.Container[T], ordering: OrderingT) -> ocol.OrderedFrozenSet[T]:
    return ocol.OrderedFrozenSet(order_values(values, ordering))


class IndexedSeq(ta.Sequence[T]):

    def __init__(self, it: ta.Iterable[T], *, identity: bool = False) -> None:
        super().__init__()

        self._lst = list(it)
        self._idxs = (ocol.IdentityKeyDict if identity else dict)(map(reversed, enumerate(self._lst)))
        check.state(len(self._idxs) == len(self._lst))

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._lst)

    def __getitem__(self, idx: int) -> T:
        return self._lst[idx]

    def __len__(self) -> int:
        return len(self._lst)

    def __contains__(self, obj: T) -> bool:
        return obj in self._idxs

    @property
    def idxs(self) -> ta.Mapping[T, int]:
        return self._idxs

    def idx(self, obj: T) -> int:
        return self._idxs[obj]


class IndexedSetSeq(ta.Sequence[ta.AbstractSet[T]]):

    def __init__(self, it: ta.Iterable[ta.Iterable[T]], *, identity: bool = False) -> None:
        super().__init__()

        self._lst = [(ocol.IdentitySet if identity else set)(e) for e in it]
        self._idxs = (ocol.IdentityKeyDict if identity else dict)((e, i) for i, es in enumerate(self._lst) for e in es)
        check.state(len(self._idxs) == sum(map(len, self._lst)))

    def __iter__(self) -> ta.Iterator[ta.AbstractSet[T]]:
        return iter(self._lst)

    def __getitem__(self, idx: int) -> ta.AbstractSet[T]:
        return self._lst[idx]

    def __len__(self) -> int:
        return len(self._lst)

    def __contains__(self, obj: T) -> bool:
        return obj in self._idxs

    @property
    def idxs(self) -> ta.Mapping[T, int]:
        return self._idxs

    def idx(self, obj: T) -> int:
        return self._idxs[obj]
