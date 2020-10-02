import abc
import functools
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import lang


K = ta.TypeVar('K')
T = ta.TypeVar('T')
U = ta.TypeVar('U')
V = ta.TypeVar('V')

BoxT = ta.TypeVar('BoxT', bound='Box')
ORDERING_TYPES = (ta.Sequence, ocol.OrderedSet, ocol.OrderedFrozenSet)
OrderingT = ta.Union[ta.Sequence[T], ocol.OrderedSet[T], ocol.OrderedFrozenSet[T]]


def list_dict(
        items: ta.Iterable[T],
        key: ta.Callable[[V], K],
        map: ta.Callable[[T], V] = lang.identity,
        *,
        identity_dict: bool = False,
) -> ta.Dict[K, ta.List[V]]:
    dct = ocol.IdentityKeyDict() if identity_dict else {}
    for e in items:
        k = key(e)
        v = map(e)
        dct.setdefault(k, []).append(v)
    return dct


def set_dict(
        items: ta.Iterable[T],
        key: ta.Callable[[T], K],
        map: ta.Callable[[T], V] = lang.identity,
        *,
        identity_dict: bool = False,
        identity_set: bool = False,
) -> ta.Dict[K, ta.Set[V]]:
    dct = ocol.IdentityKeyDict() if identity_dict else {}
    for e in items:
        k = key(e)
        v = map(e)
        dct.setdefault(k, ocol.IdentitySet() if identity_set else set()).add(v)
    return dct


def partition(items: ta.Iterable[T], pred: ta.Callable[[T], bool]) -> ta.Tuple[ta.List[T], ta.List[T]]:
    t, f = [], []
    for e in items:
        if pred(e):
            t.append(e)
        else:
            f.append(e)
    return t, f


def unique_dict(items: ta.Iterable[ta.Tuple[K, V]], *, identity: bool = False) -> ta.Dict[K, V]:
    dct = ocol.IdentityKeyDict() if identity else {}
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


class ClassKeyedCollection(lang.Abstract, ta.Collection[T]):

    _item_cls: ta.ClassVar[ta.Type[T]]

    def __init__(self, *srcs: ta.Union[ta.Mapping[ta.Type[T], T], ta.Iterable[T]], strict: bool = False) -> None:
        super().__init__()

        dct: ta.Dict[ta.Type[T], T] = {}
        for src in srcs:
            if isinstance(src, (ta.Mapping, ClassKeyedCollection)):
                if isinstance(src, ClassKeyedCollection):
                    check.issubclass(src._item_cls, self._item_cls)
                for at, a in src.items():
                    check.issubclass(at, self._item_cls)
                    if a is None:
                        if at in dct:
                            del dct[at]
                    else:
                        check.isinstance(a, at)
                        dct[at] = a

            else:
                seen = set()
                for a in src:
                    check.isinstance(a, self._item_cls)
                    at = type(a)
                    if strict:
                        check.not_in(at, seen)
                    dct[at] = a
                    seen.add(at)

        self._dct: ta.Mapping[ta.Type[T], T] = dct
        self._seq: ta.Sequence[T] = tuple(self._dct.values())

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        if any(issubclass(b, ClassKeyedCollection) and b is not ClassKeyedCollection for b in cls.__bases__):
            raise lang.FinalException(cls)

        [cls._item_cls] = [
            a
            for b in cls.__orig_bases__  # noqa
            if isinstance(b, ta._GenericAlias)  # noqa
            and getattr(b, '__origin__', None) is ClassKeyedCollection
            for a in b.__args__
        ]

    def __hash__(self) -> int:
        raise TypeError

    @property
    def seq(self) -> ta.Sequence[T]:
        return self._seq

    def __eq__(self, other: ta.Any) -> bool:
        if type(other) is not type(self):
            raise TypeError(other)
        return self._dct == other._dct

    def __repr__(self) -> str:
        return f'{{{", ".join(map(repr, self._dct.values()))}}}'

    def keys(self) -> ta.Collection[ta.Type[T]]:
        return self._dct.keys()  # noqa  # type: ignore

    def values(self) -> ta.Collection[T]:
        return self._dct.values()  # noqa  # type: ignore

    def items(self) -> ta.Iterable[ta.Tuple[ta.Type[T], T]]:
        return self._dct.items()

    def __getitem__(self, k: ta.Type[U]) -> U:
        check.issubclass(k, self._item_cls)
        return ta.cast(k, self._dct[k])

    def get(self, k: ta.Type[T], default: ta.Any = None) -> ta.Any:
        try:
            return self[k]
        except KeyError:
            return default

    def __len__(self) -> int:
        return len(self._dct)

    def __iter__(self) -> ta.Iterator[T]:
        return iter(self._dct.values())

    def __contains__(self, key: ta.Union[T, ta.Type[T]]) -> bool:  # noqa
        if isinstance(key, type):
            return check.issubclass(key, self._item_cls) in self._dct
        elif isinstance(key, self._item_cls):
            return any(a is key for a in self._dct.values())
        else:
            raise TypeError(key)


class _BoxMeta(abc.ABCMeta):

    def __new__(mcls, name, bases, namespace, **kwargs):
        if 'Box' not in globals():
            return super().__new__(mcls, name, bases, namespace, **kwargs)  # noqa

        # if Final not in bases and Abstract not in bases:
        #     bases = (*bases, Final)

        if '_value_cls' not in namespace:
            [base_arg] = {
                b._value_cls
                for b in bases
                if Box in b.__mro__
                and hasattr(b, '_value_cls')
            } or [None]
            [box_arg] = [
                a
                for b in namespace.get('__orig_bases__', [])
                if isinstance(b, ta._GenericAlias)  # noqa
                and getattr(b, '__origin__', None) is Box
                for a in b.__args__
            ] or [None]
            args = list(filter(None, [base_arg, box_arg]))
            if not args or not all(a is args[0] for a in args[1:]):
                raise TypeError(args)
            namespace['_value_cls'] = args[0]
        if not isinstance(namespace['_value_cls'], type):
            raise TypeError(namespace['_value_cls'])

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)  # noqa
        if cls.value is not Box.value:
            raise lang.FinalException(cls)
        return cls


@functools.total_ordering
class Box(lang.Abstract, ta.Generic[T], metaclass=_BoxMeta):
    _value_cls: ta.ClassVar[ta.Type[T]]

    def __init__(self, value: T) -> None:
        super().__init__()
        if not isinstance(value, self._value_cls):
            raise TypeError(value)
        self._value = value

    def repr(self) -> str:
        return f'{self.__class__.__name__}({self._value!r})'

    def __hash__(self) -> int:
        return hash(self._value)

    def __eq__(self, other: ta.Any) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(other)
        return self._value == other._value

    def __lt__(self, other: ta.Any) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(other)
        return self._value < other._value  # type: ignore

    @property
    def value(self) -> T:
        return self._value

    @classmethod
    def of(cls: BoxT, obj: ta.Union['BoxT', T]) -> BoxT:  # type: ignore
        if isinstance(obj, cls):  # noqa  # type: ignore
            return obj  # type: ignore
        elif isinstance(obj, cls._value_cls):
            return cls(obj)   # noqa  # type: ignore
        else:
            raise TypeError(obj)

    @classmethod
    def of_optional(cls: BoxT, obj: ta.Union[None, 'BoxT', T]) -> ta.Optional[BoxT]:  # type: ignore
        if obj is None:
            return None
        else:
            return cls.of(obj)
