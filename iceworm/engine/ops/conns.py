"""
TODO:
 - sql conn specifics
  - parameterized sa.text
"""
import abc
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
import sqlalchemy as sa

from .. import connectors as ctrs
from ... import metadata as md
from ... import sql
from ...trees import eval as teval
from ...trees import parsing as tpar
from ...types import QualifiedName
from ...utils import abs_set
from ..connectors.impls.sql import SqlConnection
from .base import Op
from .base import OpExecutor
from .base import OpGen


OpT = ta.TypeVar('OpT', bound=Op)
ConnsOpT = ta.TypeVar('ConnsOpT', bound='ConnsOp')


class ConnsOp(Op, abstract=True):
    pass


class ConnOp(ConnsOp, abstract=True):

    @abc.abstractproperty
    def conn(self) -> str:
        raise NotImplementedError


class ConnsOpExecutor(OpExecutor[ConnsOpT], lang.Abstract):

    def __init__(self, conns: ctrs.ConnectionSet) -> None:
        super().__init__()

        self._conns = check.isinstance(conns, ctrs.ConnectionSet)


class Transaction(Op):
    conns: ta.AbstractSet[str] = dc.field(coerce=abs_set, check=lambda l: all(isinstance(o, str) for o in l))
    op: Op


class TransactionExecutor(ConnsOpExecutor[Transaction]):

    def execute(self, op: Transaction) -> OpGen:
        sa_conn = check.isinstance(self._conns[check.single(op.conns)], SqlConnection).sa_conn
        with sa_conn.begin() as txn:
            try:
                yield op.op
                txn.commit()
            except Exception:
                txn.rollback()
                raise


class DropTable(ConnOp):
    name: QualifiedName = dc.field(coerce=QualifiedName.of, check=lambda n: len(n) > 1)

    @property
    def conn(self) -> str:
        return self.name[0]


class DropTableExecutor(ConnsOpExecutor[DropTable]):

    def execute(self, op: DropTable) -> None:
        sa_conn = check.isinstance(self._conns[op.name[0]], SqlConnection).sa_conn
        sa_conn.execute(
            sql.DropTableIfExists(
                QualifiedName(op.name[1:])))


class CreateTable(ConnOp):
    table: md.Table = dc.field(check=lambda o: isinstance(o, md.Table) and len(o.name) > 1)

    @property
    def conn(self) -> str:
        return self.table.name[0]


class CreateTableExecutor(ConnsOpExecutor[CreateTable]):

    def execute(self, op: CreateTable) -> None:
        sa_conn = check.isinstance(self._conns[op.table.name[0]], SqlConnection).sa_conn
        table = md.alchemy.FromInternal(sa.MetaData())(dc.replace(op.table, name=op.table.name[1:]))
        table.create(sa_conn)


class CreateTableAs(ConnOp):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda s: isinstance(s, str) and s)

    @property
    def conn(self) -> str:
        return self.name[0]


class CreateTableAsExecutor(ConnsOpExecutor[CreateTableAs]):

    def execute(self, op: CreateTableAs) -> None:
        sa_conn = check.isinstance(self._conns[op.name[0]], SqlConnection).sa_conn
        sa_conn.execute(
            sql.CreateTableAs(
                sql.QualifiedNameElement(
                    QualifiedName(op.name[1:])),
                sa.text(op.query)))


class InsertIntoSelect(ConnsOp):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of)
    src: str = dc.field(check=lambda s: isinstance(s, str) and s)
    query: str = dc.field(check=lambda s: isinstance(s, str) and s)


class InsertIntoSelectExecutor(ConnsOpExecutor[InsertIntoSelect]):

    def execute(self, op: InsertIntoSelect) -> None:
        src_conn = self._conns[op.src]
        src = src_conn.create_row_source(op.query)
        dst_conn = self._conns[op.dst[0]]
        dst = dst_conn.create_row_sink(QualifiedName(op.dst[1:]))
        dst.consume_rows(src.produce_rows())


class InsertIntoEval(ConnsOp):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda s: isinstance(s, str) and s)


class InsertIntoEvalExecutor(ConnsOpExecutor[InsertIntoEval]):

    def execute(self, op: InsertIntoEval) -> None:
        root = tpar.parse_stmt(op.query)
        src = ctrs.ListRowSource(teval.StmtEvaluator().eval(root))
        dst_conn = self._conns[op.dst[0]]
        dst = dst_conn.create_row_sink(QualifiedName(op.dst[1:]))
        dst.consume_rows(src.produce_rows())


class Exec(ConnsOp):
    conn: str = dc.field(check=lambda s: isinstance(s, str) and s)
    query: str = dc.field(check=lambda s: isinstance(s, str) and s)


class ExecExecutor(ConnsOpExecutor[Exec]):

    def execute(self, op: Exec) -> None:
        sa_conn = check.isinstance(self._conns[op.conn], SqlConnection).sa_conn
        sa_conn.execute(op.query)


class CopyTable(Op):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of)
    src: QualifiedName = dc.field(coerce=QualifiedName.of)
