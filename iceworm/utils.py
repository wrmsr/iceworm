import typing as ta

from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import defs


T = ta.TypeVar('T')
U = ta.TypeVar('U')
K = ta.TypeVar('K')
V = ta.TypeVar('V')


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
