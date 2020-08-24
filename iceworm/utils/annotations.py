import abc
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from .utils import seq


AnnotationT = ta.TypeVar('AnnotationT', bound='Annotation')


class Annotation(dc.Enum):
    pass


class Annotations(
    dc.Frozen,
    ta.Generic[AnnotationT],
    ta.Collection[Annotation],
    abstract=True,
    allow_setattr=True,
):
    anns: ta.Sequence[Annotation] = dc.field(coerce=seq)

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

        dct: ta.Mapping[ta.Type[Annotation], Annotation] = {}
        for ann in self.anns:
            check.not_in(type(ann), dct)
            dct[type(ann)] = ann
        self._anns_by_cls: ta.Mapping[ta.Type[Annotation], Annotation] = dct

    def __getitem__(self, cls: ta.Type[AnnotationT]) -> AnnotationT:
        check.issubclass(cls, Annotation)
        return self._anns_by_cls[cls]

    def __contains__(self, cls: ta.Type[AnnotationT]) -> bool:
        check.issubclass(cls, Annotation)
        return cls in self._anns_by_cls

    def __len__(self) -> int:
        return len(self._anns_by_cls)

    def __iter__(self) -> ta.Iterator[Annotation]:
        return iter(self._anns_by_cls.values())
