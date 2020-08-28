import operator
import typing as ta

from omnibus import collections as ocol
from omnibus import dataclasses as dc

from ...utils import annotations as anns
from ...utils import build_dc_repr
from ...utils import serde
from ...utils.nodal import NodalDataclass


class Annotation(anns.Annotation, abstract=True):
    pass


class Annotations(anns.Annotations[Annotation]):

    @classmethod
    def _ann_cls(cls) -> ta.Type[Annotation]:
        return Annotation


class Op(dc.Enum, NodalDataclass['Op'], reorder=True, repr=False):

    anns: Annotations = dc.field(
        (),
        kwonly=True,
        repr=False,
        hash=False,
        compare=False,
        coerce=Annotations,
        metadata={serde.Ignore: operator.not_},
    )

    meta: ta.Mapping[ta.Any, ta.Any] = dc.field(
        ocol.frozendict(),
        kwonly=True,
        repr=False,
        hash=False,
        compare=False,
        coerce=ocol.frozendict,
        metadata={serde.Ignore: True},
    )

    __repr__ = build_dc_repr

    @classmethod
    def _nodal_cls(cls) -> ta.Type['Op']:
        return Op
