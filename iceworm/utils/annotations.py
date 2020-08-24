import abc
import collections.abc
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from . import serde


AnnotationT = ta.TypeVar('AnnotationT', bound='Annotation')


class Annotation(dc.Enum):
    pass


def _coerce_anns(
        obj: ta.Union[ta.Mapping[ta.Type[Annotation], Annotation], ta.Iterable[Annotation]],
) -> ta.Sequence[Annotation]:
    if isinstance(obj, collections.abc.Mapping):
        ret = []
        seen = set()
        for c, a in obj.items():
            if type(a) is not c:
                raise TypeError((c, a))
            if c in seen:
                raise KeyError(c)
            ret.append(a)
        return ret
    else:
        return [check.isinstance(a, Annotation) for a in obj]


class Annotations(
    dc.Frozen,
    ta.Generic[AnnotationT],
    collections.abc.Sized,
    ta.Iterable[AnnotationT],
    ta.Container[ta.Type[AnnotationT]],
    abstract=True,
    allow_setattr=True,
):
    anns: ta.Sequence[AnnotationT] = dc.field(
        (), coerce=_coerce_anns, metadata={serde.GetType: lambda cls: ta.Sequence[cls._ann_cls()]})

    @abc.abstractclassmethod
    def _ann_cls(cls) -> ta.Type[Annotation]:
        raise NotImplementedError

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        check.issubclass(cls._ann_cls(), Annotation)

    def __post_init__(self) -> None:
        ann_cls = self._ann_cls()
        for ann in self.anns:
            check.isinstance(ann, ann_cls)

        dct = {}
        for ann in self.anns:
            check.not_in(type(ann), dct)
            dct[type(ann)] = ann
        self._anns_by_cls: ta.Mapping[ta.Type[AnnotationT], AnnotationT] = dct

    def __getitem__(self, cls: ta.Type[AnnotationT]) -> AnnotationT:
        check.issubclass(cls, self._ann_cls())
        return self._anns_by_cls[cls]

    def __contains__(self, cls: ta.Type[AnnotationT]) -> bool:  # noqa
        check.issubclass(cls, self._ann_cls())
        return cls in self._anns_by_cls

    def __len__(self) -> int:
        return len(self._anns_by_cls)

    def __iter__(self) -> ta.Iterator[Annotation]:
        return iter(self._anns_by_cls.values())
