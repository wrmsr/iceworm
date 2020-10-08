"""
TODO:
 - ** diffing **
 - explicit subclass registration for serde
"""
import collections
import operator
import types
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import reflect as rfl

from . import annotations as ans
from . import serde


Self = ta.TypeVar('Self')
NodalT = ta.TypeVar('NodalT', bound='Nodal')
AnnotationT = ta.TypeVar('AnnotationT', bound=ans.Annotation)


class _FieldInfo(dc.Pure):
    cls: ta.Type['Noda']
    opt: bool = False
    seq: bool = False


class _FieldsInfo(dc.Pure):
    flds: ta.Mapping[str, _FieldInfo]


class _NodalMeta(dc.metaclass.Meta):  # noqa

    def __new__(mcls, name, bases, namespace, **kwargs):
        if name == 'Nodal' and namespace['__module__'] == __name__:
            return super().__new__(mcls, name, bases, namespace, **kwargs)

        for k in [
            '_ann_cls',
            '_anns_cls',
            'anns',
            'meta',
        ]:
            check.not_in(k, kwargs)
            check.not_in(k, namespace.get('__annotations__', {}))

        nbs = {nb for b in bases for nb in b.__mro__ if Nodal in nb.__bases__}
        if not nbs:
            check.in_(Nodal, bases)
            nos = check.single([
                obs
                for ob in namespace['__orig_bases__']
                for obs in [rfl.spec(ob)]
                if isinstance(obs, rfl.ExplicitParameterizedGenericTypeSpec) and obs.erased_cls is Nodal
            ])

            ann_cls = check.issubclass(nos.cls_args[1], ans.Annotation)
            namespace['_ann_cls'] = ann_cls

            class Annotations(ans.Annotations[ann_cls]):
                @classmethod
                def _ann_cls(cls) -> ta.Type[ann_cls]:
                    return ann_cls

            namespace['_anns_cls'] = Annotations

            namespace['anns'] = dc.field(
                (),
                kwonly=True,
                repr=False,
                hash=False,
                compare=False,
                coerce=Annotations,
                metadata={serde.Ignore: operator.not_},
            )

            namespace.setdefault('__annotations__', {})['anns'] = Annotations

            namespace['meta'] = dc.field(
                ocol.frozendict(),
                kwonly=True,
                repr=False,
                hash=False,
                compare=False,
                coerce=lambda d: ocol.frozendict(
                    (k, v) for k, v in check.isinstance(d, ta.Mapping).items() if v is not None),
                check=lambda d: not any(isinstance(k, ann_cls) or v is None for k, v in d.items()),
                metadata={serde.Ignore: True},
            )

            namespace.setdefault('__annotations__', {})['meta'] = ta.Mapping[ta.Any, ta.Any]

        else:
            nb = check.single(nbs)  # noqa

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        if not nbs:
            cls._nodal_cls = cls

        return cls


_COMMON_META_KWARGS = {
    'frozen': True,
    'reorder': True,
}


def _confer_final(att, sub, sup, bases):
    return sub['abstract'] is dc.MISSING or not sub['abstract']


class Nodal(
    dc.Data,
    ta.Generic[NodalT, AnnotationT],
    metaclass=_NodalMeta,
    abstract=True,
    eq=False,
    **_COMMON_META_KWARGS,
    confer={
        'abstract': True,
        **_COMMON_META_KWARGS,
        'confer': {
            **_COMMON_META_KWARGS,
            'final': dc.Conferrer(_confer_final),
            'repr': dc.SUPER,
            'eq': dc.SUPER,
            'allow_setattr': dc.SUPER,
            'aspects': dc.SUPER,
            'confer': dc.SUPER,
        },
    },
):

    anns: ans.Annotations = dc.field((), kwonly=True)
    meta: ta.Mapping[ta.Any, ta.Any] = dc.field(ocol.frozendict(), kwonly=True)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        # Note: Cannot build fields info here as this is happening during class construction.
        check.state(dc.is_dataclass(cls))

    _nodal_cls: ta.ClassVar[ta.Type[NodalT]]

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
            if isinstance(fcls, type) and issubclass(fcls, Nodal):
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

    def yield_field_children(self, fld: dc.Field) -> ta.Iterator[NodalT]:
        val = getattr(self, fld.name)
        if isinstance(val, self._nodal_cls):
            yield val
        elif isinstance(val, collections.abc.Sequence):
            yield from (item for item in val if isinstance(item, self._nodal_cls))

    @property
    def children(self) -> ta.Generator[NodalT, None, None]:
        for fld in dc.fields(self):
            yield from self.yield_field_children(fld)

    def build_field_map_kwargs(self, fn: ta.Callable[[NodalT], NodalT], fld: dc.Field) -> ta.Mapping[str, ta.Any]:
        val = getattr(self, fld.name)
        if isinstance(val, self._nodal_cls):
            return {fld.name: fn(val)}
        elif isinstance(val, collections.abc.Sequence) and not isinstance(val, str):
            return {fld.name: tuple([fn(item) if isinstance(item, self._nodal_cls) else item for item in val])}
        else:
            return {}

    def map(self: Self, fn: ta.Callable[[NodalT], ta.Mapping[str, ta.Any]], **kwargs) -> Self:
        rpl_kw = {**kwargs}
        for fld in dc.fields(self):
            if fld.name in kwargs:
                continue
            for k, v in self.build_field_map_kwargs(fn, fld).items():
                if k in rpl_kw:
                    raise KeyError(k)
                rpl_kw[k] = v
        return dc.replace(self, **rpl_kw)

    def fmap(self: Self, fn: ta.Callable[[NodalT], ta.Mapping[str, ta.Any]]) -> Self:
        return self.map(fn, **fn(self))


def meta_chain(
        obj: Nodal,
        key: ta.Any,
        *,
        cls: ta.Type[Nodal] = Nodal,
        next: ta.Callable[[ta.Any], Nodal] = lambda o: o,
) -> ta.List[Nodal]:
    lst = []
    while True:
        lst.append(check.isinstance(obj, cls))
        try:
            val = obj.meta[key]
        except KeyError:
            break
        obj = next(val)
    return lst
