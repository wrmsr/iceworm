"""
TODO:
 - explicit subclass registration for serde
"""
import abc
import collections
import types
import typing as ta

from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import reflect as rfl


Self = ta.TypeVar('Self')
NodalT = ta.TypeVar('NodalT', bound='Nodal')


class _FieldInfo(dc.Pure):
    cls: ta.Type['Noda']
    opt: bool = False
    seq: bool = False


class _FieldsInfo(dc.Pure):
    flds: ta.Mapping[str, _FieldInfo]


class NodalDataclass(ta.Generic[NodalT], lang.Abstract):

    @classmethod
    @abc.abstractmethod
    def _nodal_cls(cls) -> ta.Type[NodalT]:
        raise NotImplementedError

    @classmethod
    def _build_fields_info(cls) -> _FieldsInfo:
        th = ta.get_type_hints(cls)
        flds = {}
        for f in dc.fields(cls):
            fcls = th[f.name]
            opt = False
            seq = False
            if rfl.is_generic(fcls) and fcls.__origin__ is ta.Union:
                args = fcls.__args__
                if len(args) != 2 or type(None) not in args:
                    raise TypeError(fcls)
                [fcls] = [a for a in args if a not in (None, type(None))]
                opt = True
            if rfl.is_generic(fcls) and fcls.__origin__ is collections.abc.Sequence:
                [fcls] = fcls.__args__
                seq = True
            if isinstance(fcls, type) and issubclass(fcls, NodalDataclass):
                flds[f.name] = _FieldInfo(fcls, opt, seq)
        return _FieldsInfo(flds)

    def __post_init__(self) -> None:
        cls = type(self)
        try:
            fi = cls.__dict__['_fields_info']
        except KeyError:
            fi = cls._build_fields_info()
            setattr(cls, '_fields_info', fi)

        for a, f in fi.flds.items():
            v = getattr(self, a)
            if f.opt and v is None:
                continue
            elif v is None:
                raise TypeError(v, f, a)
            if f.seq:
                if isinstance(v, types.GeneratorType):
                    raise TypeError(v, f, a)
                for e in v:
                    if not isinstance(e, f.cls):
                        raise TypeError(e, f, a)
            else:
                if not isinstance(v, f.cls):
                    raise TypeError(v, f, a)

        try:
            sup = super().__post_init__
        except AttributeError:
            pass
        else:
            sup()

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
