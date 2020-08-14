import abc
import collections
import typing as ta

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
