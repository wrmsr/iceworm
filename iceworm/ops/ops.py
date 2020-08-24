"""
TODO:
 - 'merge'? refresh?
 - opaque / marking purely-internal ops
  - annotation?

Op families:
 - spark?
"""
import typing as ta

from omnibus import dataclasses as dc

from .. import metadata as md
from ..types import QualifiedName
from ..utils import abs_set
from ..utils import build_dc_repr
from ..utils import seq
from ..utils.nodal import NodalDataclass


SelfOp = ta.TypeVar('SelfOp', bound='Op')
OpGen = ta.Generator['Op', None, None]
OpMapper = ta.Callable[['Op'], 'Op']


class Op(dc.Enum, NodalDataclass['Op']):

    __repr__ = build_dc_repr

    @classmethod
    def _nodal_cls(cls) -> ta.Type['Op']:
        return Op


class Transaction(Op):
    conns: ta.AbstractSet[str] = dc.field(coerce=abs_set, check=lambda l: all(isinstance(o, str) for o in l))
    children: ta.Sequence[Op] = dc.field(coerce=seq, check=lambda l: all(isinstance(o, Op) for o in l))


class DropTable(Op):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)


class CreateTable(Op):
    table: md.Table = dc.field(check=lambda o: isinstance(o, md.Table))


class CreateTableAs(Op):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))


class InsertIntoSelect(Op):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))


class CopyTable(Op):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of)
    src: QualifiedName = dc.field(coerce=QualifiedName.of)
