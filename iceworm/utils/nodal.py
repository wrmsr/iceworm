"""
TODO:
 - explicit subclass registration for serde
 - typecheck child fields
"""
import abc
import collections
import typing as ta

from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import lang


Self = ta.TypeVar('Self')
NodalT = ta.TypeVar('NodalT', bound='Nodal')


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
