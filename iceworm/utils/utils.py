import abc
import collections
import inspect
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import defs
from omnibus import lang


T = ta.TypeVar('T')
U = ta.TypeVar('U')
K = ta.TypeVar('K')
V = ta.TypeVar('V')
Self = ta.TypeVar('Self')
NodalT = ta.TypeVar('NodalT', bound='Nodal')


def build_dc_repr(obj: ta.Any) -> str:
    return defs.build_repr(obj, *[f.name for f in dc.fields(obj) if f.repr])


def build_enum_value_map(cls: ta.Type[T]) -> ta.Mapping[U, T]:
    dct = {}
    for v in cls.__members__.values():
        if v.value in dct:
            raise NameError(v.name)
        dct[v.value] = v
    return dct


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
        return ocol.frozenlist(it)


def mapping(obj: ta.Union[ta.Mapping[K, V], ta.Iterable[ta.Tuple[K, V]], None]) -> ta.Optional[ta.Mapping[K, V]]:
    if obj is None:
        return None
    elif isinstance(obj, str):
        raise TypeError(obj)
    else:
        return ocol.frozendict(obj)


class NodalDataclass(ta.Generic[NodalT], lang.Abstract):
    """
    TODO:
     - explicit subclass registration for serde
    """

    @classmethod
    @abc.abstractmethod
    def _nodal_cls(cls) -> ta.Type[NodalT]:
        raise NotImplementedError

    def yield_field_children(self, fld: dc.Field) -> ta.Generator[NodalT, None, None]:
        val = getattr(self, fld.name)
        if isinstance(val, self._nodal_cls()):
            yield val
        elif isinstance(val, collections.abc.Sequence):
            yield from (item for item in val if isinstance(item, self._nodal_cls()))

    @property
    def children(self) -> ta.Generator[NodalT, None, None]:
        for fld in dc.fields(self):
            yield from self.yield_field_children(fld)

    def build_field_map_kwargs(self, fn: ta.Callable[[NodalT], NodalT], fld: dc.Field) -> ta.Mapping[str, ta.Any]:
        val = getattr(self, fld.name)
        if isinstance(val, self._nodal_cls()):
            return {fld.name: fn(val)}
        elif isinstance(val, collections.abc.Sequence) and not isinstance(val, str):
            return {fld.name: ocol.frozenlist([fn(item) if isinstance(item, self._nodal_cls()) else item for item in val])}  # noqa
        else:
            return {}

    def map(self: Self, fn: ta.Callable[[NodalT], NodalT], **kwargs) -> Self:
        rpl_kw = {**kwargs}
        for fld in dc.fields(self):
            if fld.name in kwargs:
                continue
            for k, v in self.build_field_map_kwargs(fn, fld).items():
                if k in rpl_kw:
                    raise KeyError(k)
                rpl_kw[k] = v
        return dc.replace(self, **rpl_kw)


class ReprFn:

    def __init__(self, fn: ta.Callable) -> None:
        super().__init__()

        self._fn = fn

    def __repr__(self) -> str:
        fn = self._fn
        file = inspect.getsourcefile(fn)
        obj = fn
        if inspect.ismethod(fn):
            obj = fn.__func__
        if inspect.isfunction(obj):
            obj = fn.__code__
        lnum = obj.co_firstlineno
        return f'ReprFn(<{file}:{lnum}>)'

    def __get__(self, instance, owner=None):
        return ReprFn(self._fn.__get__(instance, owner))

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


class MemoizedUnary(ta.Generic[T, U]):

    def __init__(
            self,
            fn: ta.Callable[[T], U],
            *,
            identity: bool = False,
            on_compute: ta.Optional[ta.Callable[[T], U]] = None,
            name: ta.Optional[str] = None,
    ) -> None:
        super().__init__()

        self._fn = check.not_none(fn)
        self._identity = identity
        self._on_compute = on_compute
        self._name = name

        self._dct: ta.MutableMapping[T, U] = ocol.IdentityKeyDict() if identity else {}

    def __set_name__(self, owner, name):
        if self._name is not None:
            check.state(name == self._name)
        else:
            self._name = check.not_empty(name)

    @property
    def dct(self) -> ta.Mapping[T, U]:
        return self._dct

    def __get__(self, instance, owner=None):
        obj = type(self)(
            self._fn.__get__(instance, owner),
            identity=self._identity,
            on_compute=self._on_compute,
            name=self._name,
        )
        if instance is not None:
            check.not_empty(self._name)
            check.not_in(self._name, instance.__dict__)
            instance.__dict__[self._name] = obj
        return obj

    def __call__(self, arg: T) -> U:
        try:
            return self._dct[arg]
        except KeyError:
            v = self._dct[arg] = self._fn(arg)
            if self._on_compute is not None:
                self._on_compute(arg, v)
            return v


memoized_unary = MemoizedUnary
