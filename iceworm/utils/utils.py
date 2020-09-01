import inspect
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import defs


T = ta.TypeVar('T')
U = ta.TypeVar('U')


def build_dc_repr(obj: ta.Any) -> str:
    return defs.build_repr(obj, *[f.name for f in dc.fields(obj) if f.repr])


def build_enum_value_map(cls: ta.Type[T]) -> ta.Mapping[U, T]:
    dct = {}
    for v in cls.__members__.values():
        if v.value in dct:
            raise NameError(v.name)
        dct[v.value] = v
    return dct


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
            max_recursion: ta.Optional[int] = None,
    ) -> None:
        super().__init__()

        self._fn = check.not_none(fn)
        self._identity = identity
        self._on_compute = on_compute
        self._name = name
        self._max_recursion = max_recursion

        self._dct: ta.MutableMapping[T, U] = ocol.IdentityKeyDict() if identity else {}
        self._recursion = 0

    def __set_name__(self, owner, name):
        if self._name is not None:
            check.state(name == self._name)
        else:
            self._name = check.not_empty(name)

    @property
    def dct(self) -> ta.Mapping[T, U]:
        return self._dct

    def __get__(self, instance, owner=None):
        if self._name:
            try:
                return instance.__dict__[self._name]  # FIXME: why
            except KeyError:
                pass
        obj = type(self)(
            self._fn.__get__(instance, owner),
            identity=self._identity,
            on_compute=self._on_compute,
            name=self._name,
            max_recursion=self._max_recursion,
        )
        if instance is not None:
            check.not_empty(self._name)
            instance.__dict__[self._name] = obj
        return obj

    def __call__(self, arg: T) -> U:
        try:
            return self._dct[arg]
        except KeyError:
            try:
                self._recursion += 1
                if self._max_recursion is not None:
                    check.state(self._recursion < self._max_recursion)
                v = self._dct[arg] = self._fn(arg)
            finally:
                self._recursion -= 1
            if self._on_compute is not None:
                self._on_compute(arg, v)
            return v


memoized_unary = MemoizedUnary
