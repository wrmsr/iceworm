import typing as ta

from omnibus import dataclasses as dc

from ...utils import annotations as anns
from ...utils import build_dc_repr
from ...utils import nodal


class Annotation(anns.Annotation, abstract=True):
    pass


class Annotations(anns.Annotations[Annotation]):

    @classmethod
    def _ann_cls(cls) -> ta.Type[Annotation]:
        return Annotation


class Op(dc.Enum, nodal.Nodal['Op'], reorder=True, repr=False):

    anns: Annotations = nodal.new_anns_field(Annotations)
    meta: ta.Mapping[ta.Any, ta.Any] = nodal.new_meta_field(Annotation)

    __repr__ = build_dc_repr

    @classmethod
    def _nodal_cls(cls) -> ta.Type['Op']:
        return Op
