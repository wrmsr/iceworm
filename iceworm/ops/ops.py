"""
TODO:
 - 'merge'? refresh?

Op families:
 - spark?
"""
import typing as ta

from omnibus import dataclasses as dc

from ..types import QualifiedName
from ..utils import NodalDataclass
from ..utils import build_dc_repr
from ..utils import seq


SelfOp = ta.TypeVar('SelfOp', bound='Op')
OpGen = ta.Generator['Op', None, None]
OpMapper = ta.Callable[['Op'], 'Op']


class Op(dc.Enum, NodalDataclass['Op']):

    __repr__ = build_dc_repr

    @classmethod
    def _nodal_cls(cls) -> ta.Type['Op']:
        return Op


class SqlOp(Op, abstract=True):
    pass


class Transaction(SqlOp):
    children: ta.Sequence[Op] = dc.field(coerce=seq)


class DropTable(SqlOp):
    name: QualifiedName = dc.field(check=lambda v: isinstance(v, QualifiedName))


class CreateTableAs(SqlOp):
    name: QualifiedName = dc.field(check=lambda v: isinstance(v, QualifiedName))
    query: str
