"""
TODO:
 - 'merge'? refresh?

Op families:
 - spark?
"""
import typing as ta

from omnibus import dataclasses as dc

from .. import metadata as md
from ..types import QualifiedName
from ..utils import build_dc_repr
from ..utils import NodalDataclass
from ..utils import ReprFn
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
    conn_name: str
    children: ta.Sequence[Op] = dc.field(coerce=seq)


class DropTable(SqlOp):
    table_name: QualifiedName = dc.field(check=lambda v: isinstance(v, QualifiedName))


class CreateTable(SqlOp):
    conn_name: str
    table: md.Table


class CreateTableAs(SqlOp):
    table_name: QualifiedName = dc.field(check=lambda v: isinstance(v, QualifiedName))
    query: str


class InsertInto(SqlOp):
    dst_table_name: QualifiedName = dc.field(check=ReprFn(lambda v: isinstance(v, QualifiedName)))
    src_table_name: QualifiedName = dc.field(check=ReprFn(lambda v: isinstance(v, QualifiedName)))
