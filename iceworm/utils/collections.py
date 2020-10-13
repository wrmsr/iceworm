import typing as ta

from omnibus import check
from omnibus import lang


T = ta.TypeVar('T')
U = ta.TypeVar('U')


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
