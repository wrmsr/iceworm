import abc
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
import sqlalchemy as sa

from .. import connectors as ctrs
from ... import alchemy as alch
from ... import metadata as md
from ... import sql
from ...trees import eval as teval
from ...trees import parsing as tpar
from ...types import QualifiedName
from ...utils import abs_set
from ..connectors.impls.sql import SqlConnection
from ..utils import parse_simple_select_table
from ..utils import parse_simple_select_tables
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
        table = alch.FromInternal(sa.MetaData())(dc.replace(op.table, name=op.table.name[1:]))
        table.create(sa_conn)


class CreateTableAs(ConnOp):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))

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
    query: str = dc.field(check=lambda o: isinstance(o, str))


class InsertIntoSelectExecutor(ConnsOpExecutor[InsertIntoSelect]):

    def execute(self, op: InsertIntoSelect) -> None:
        src = None

        if src is None:
            try:
                src_name = parse_simple_select_table(op.query, star=True)
            except ValueError:
                pass
            else:
                src_conn = self._conns[src_name[0]]
                src_query = f"select * from {'.'.join(src_name[1:])}"
                src = src_conn.create_row_source(src_query)

        if src is None:
            try:
                tbl_names = parse_simple_select_tables(op.query)
                if tbl_names:
                    raise ValueError
            except ValueError:
                pass
            else:
                root = tpar.parse_stmt(op.query)
                src = ctrs.ListRowSource(teval.StmtEvaluator().eval(root))

        if src is None:
            raise ValueError(op.query)

        dst_conn = self._conns[op.dst[0]]
        dst = dst_conn.create_row_sink(QualifiedName(op.dst[1:]))
        dst.consume_rows(src.produce_rows())


class CopyTable(Op):
    dst: QualifiedName = dc.field(coerce=QualifiedName.of)
    src: QualifiedName = dc.field(coerce=QualifiedName.of)
