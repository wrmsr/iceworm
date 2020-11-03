import abc
import typing as ta

from omnibus import dataclasses as dc
from omnibus import collections as col
from omnibus import lang
from omnibus import nodal

from ...utils import build_dc_repr


OpT = ta.TypeVar('OpT', bound='Op')
OpGen = ta.Generator['Op', None, None]


class Annotation(nodal.Annotation):
    pass


class Op(nodal.Nodal['Op', Annotation], repr=False):
    __repr__ = build_dc_repr


class OpExecutor(lang.Abstract, ta.Generic[OpT]):

    @abc.abstractmethod
    def execute(self, op: OpT) -> ta.Optional[OpGen]:
        raise NotImplementedError


class Set(Op):
    ops: ta.Sequence[Op] = dc.field(coerce=col.seq)


class List(Op):
    ops: ta.Sequence[Op] = dc.field(coerce=col.seq)


class ListExecutor(OpExecutor[List]):

    def execute(self, op: List) -> OpGen:
        yield from op.ops
