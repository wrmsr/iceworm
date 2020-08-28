"""
TODO:
 - ** blurs line between task and target **
 - 'merge'? refresh?
 - from alerts:
  - conditional? takes query?
   - contextual? context?
    - state as tables? garbage collection? static lifetime analysis? kinda btree blackboard style
  - again w/ the 'insert into slack' thing: slack/pd/email

Op families:
 - spark?
"""
import abc
import typing as ta

from omnibus import dataclasses as dc

from ... import metadata as md
from ...types import QualifiedName
from ...utils import abs_set
from ...utils import seq
from .base import Op


SelfOp = ta.TypeVar('SelfOp', bound='Op')
OpGen = ta.Generator['Op', None, None]
OpMapper = ta.Callable[['Op'], 'Op']


class List(Op):
    ops: ta.Sequence[Op] = dc.field(coerce=seq)


class Set(Op):
    ops: ta.Sequence[Op] = dc.field(coerce=seq)


class Transaction(Op):
    conns: ta.AbstractSet[str] = dc.field(coerce=abs_set, check=lambda l: all(isinstance(o, str) for o in l))
    op: Op


class Atomic(Op, abstract=True):

    @abc.abstractproperty
    def conn(self) -> str:
        raise NotImplementedError


class DropTable(Atomic):
    name: QualifiedName = dc.field(coerce=QualifiedName.of, check=lambda n: len(n) > 1)

    @property
    def conn(self) -> str:
        return self.name[0]


class CreateTable(Atomic):
    table: md.Table = dc.field(check=lambda o: isinstance(o, md.Table) and len(o.name) > 1)

    @property
    def conn(self) -> str:
        return self.table.name[0]


class CreateTableAs(Op):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))


class AtomicCreateTableAs(Atomic):
    name: QualifiedName = dc.field(coerce=QualifiedName.of, check=lambda n: len(n) > 1)
    query: str = dc.field(check=lambda o: isinstance(o, str))

    @property
    def conn(self) -> str:
        return self.name[0]


class InsertIntoSelect(Op):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))


class AtomicInsertIntoSelect(Atomic):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of, check=lambda n: len(n) > 1)
    query: str = dc.field(check=lambda o: isinstance(o, str))

    @property
    def conn(self) -> str:
        return self.dst[0]


class CopyTable(Op):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of)
    src: QualifiedName = dc.field(coerce=QualifiedName.of)


class AtomicCopyTable(Atomic):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of, check=lambda n: len(n) > 1)
    src: QualifiedName = dc.field(coerce=QualifiedName.of, check=lambda n: len(n) > 1)

    dc.check(lambda dst, src: dst[0] == src[0])

    @property
    def conn(self) -> str:
        return self.dst[0]
