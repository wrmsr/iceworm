import functools
import typing as ta
import weakref

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import lang

from ...utils import serde
from .base import Element
from .base import Id
from .base import id_check


ElementT = ta.TypeVar('ElementT', bound='Element')
Self = ta.TypeVar('Self"')
V = ta.TypeVar('V')
Refable = ta.Union['Ref', Id, Element]


_REF_CLS_CACHE: ta.MutableMapping[type, ta.Type['Ref']] = weakref.WeakKeyDictionary()


@functools.total_ordering
class Ref(dc.Frozen, lang.Abstract, ta.Generic[ElementT], repr=False, eq=False, order=False):
    id: Id = dc.field(check=id_check)

    ele_cls: ta.ClassVar[type]

    def __hash__(self) -> int:
        return hash(id)

    def __bool__(self) -> bool:
        raise TypeError('Forbidden')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.id!r})'

    __str__ = __repr__

    def __eq__(self, other: ta.Any) -> bool:
        if isinstance(other, self.ele_cls):
            return self.id == other.id
        elif type(other) is type(self):
            return self.id == other.id
        else:
            raise TypeError(other)

    def __lt__(self, other: ta.Any) -> bool:
        if type(other) is type(self):
            return self.id < other.id
        else:
            raise TypeError(other)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()

        check.isinstance(cls.ele_cls, type)
        if cls.ele_cls is not Element:
            check.issubclass(cls.ele_cls, Element)
        check.state(lang.Final in cls.__bases__)
        rc = cls.ele_cls
        check.not_in(rc, _REF_CLS_CACHE)
        _REF_CLS_CACHE[rc] = cls

        class _RefSerde(serde.AutoSerde[cls]):  # noqa
            _bind = cls

            @property
            def handles_dataclass_polymorphism(self) -> bool:
                return True

            def serialize(self, obj: Ref) -> ta.Any:
                return check.isinstance(obj, cls).id

            def deserialize(self, ser: ta.Any) -> Ref:
                return cls(check.isinstance(ser, Id))

    def __class_getitem__(cls, arg: type) -> type:
        check.isinstance(arg, type)
        try:
            ret = _REF_CLS_CACHE[arg]
        except KeyError:
            bc = super().__class_getitem__(arg)
            ns = {
                'ele_cls': arg,
                '__class_getitem__': ta.Generic.__class_getitem__,
                '__hash__': Ref.__hash__,
                '__bool__': Ref.__bool__,
            }
            ret = lang.new_type(
                f'{cls.__name__}[{arg.__name__}]',
                (bc, lang.Final),
                ns,
                repr=False,
                eq=False,
                order=False,
            )
        check.state(_REF_CLS_CACHE[arg] is ret)
        return ret

    @classmethod
    def cls(cls: ta.Type[Self], arg: type) -> ta.Type[Self]:
        return cls[arg]

    @classmethod
    def of(cls: ta.Type[Self], obj: Refable) -> Self:
        if cls is Ref:
            if isinstance(obj, Element):
                return cls[type(obj)](obj.id)
            if isinstance(obj, Ref):
                return obj
            if isinstance(obj, Id):
                return cls[Element](obj)
        else:
            if isinstance(obj, cls.ele_cls):
                return cls(obj.id)
            if type(obj) is cls:
                return obj
            if isinstance(obj, Id):
                return cls(obj)
        raise TypeError(obj)


class RefSet(ta.AbstractSet[Ref]):

    def __init__(self, src: ta.Iterable[Refable] = ()) -> None:
        super().__init__()
        self._set = {Ref.of(e) for e in src}

    def __len__(self) -> int:
        return len(self._set)

    def __contains__(self, obj: Refable) -> bool:
        return Ref.of(obj) in self._set

    def __iter__(self) -> ta.Iterator[Ref]:
        return iter(self._set)


class RefMap(ta.Mapping[Ref, V]):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        if len(args) > 1:
            raise TypeError(args)
        self._dct: ta.Dict[Ref, V] = {}
        for e, v in ocol.yield_dict_init(*args, **kwargs):
            r = Ref.of(e)
            check.not_in(r, self._dct)
            self._dct[r] = v

    def __len__(self) -> int:
        return len(self._dct)

    def __iter__(self) -> ta.Iterator[Ref]:
        return iter(self._dct)

    def __contains__(self, key: Refable) -> bool:
        return Ref.of(key) in self._dct

    def __getitem__(self, key: Refable) -> Element:
        return self._dct[Ref.of(key)]
