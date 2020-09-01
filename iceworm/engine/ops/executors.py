"""
TODO:
 - def handles? strategies? InsertIntoFrom?
  - aot ops rewriting is more powerful than feuding greedy executors
"""
import abc
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
import sqlalchemy as sa

from .. import connectors as ctrs
from .. import ops
from ... import alchemy as alch
from ... import sql
from ...trees import eval as teval
from ...trees import parsing as tpar
from ...types import QualifiedName
from ..connectors.sql import SqlConnection
from ..utils import parse_simple_select_table
from ..utils import parse_simple_select_tables


OpT = ta.TypeVar('OpT', bound=ops.Op)
OpGen = ta.Generator[ops.Op, None, None]


class Executor(lang.Abstract, ta.Generic[OpT]):

    @abc.abstractmethod
    def execute(self, op: OpT) -> ta.Optional[OpGen]:
        raise NotImplementedError


class ListExecutor(Executor[ops.List]):

    def execute(self, op: ops.List) -> OpGen:
        yield from op.ops


class ConnsExecutor(Executor[OpT], lang.Abstract):

    def __init__(self, conns: ctrs.ConnectionSet) -> None:
        super().__init__()

        self._conns = check.isinstance(conns, ctrs.ConnectionSet)


class TransactionExecutor(ConnsExecutor[ops.Transaction]):

    def execute(self, op: ops.Transaction) -> OpGen:
        sa_conn = check.isinstance(self._conns[check.single(op.conns)], SqlConnection).sa_conn
        with sa_conn.begin() as txn:
            try:
                yield op.op
                txn.commit()
            except Exception:
                txn.rollback()
                raise


class DropTableExecutor(ConnsExecutor[ops.DropTable]):

    def execute(self, op: ops.DropTable) -> None:
        sa_conn = check.isinstance(self._conns[op.name[0]], SqlConnection).sa_conn
        sa_conn.execute(
            sql.DropTableIfExists(
                sql.QualifiedNameElement(
                    QualifiedName(op.name[1:]))))


class CreateTableExecutor(ConnsExecutor[ops.CreateTable]):

    def execute(self, op: ops.CreateTable) -> None:
        sa_conn = check.isinstance(self._conns[op.table.name[0]], SqlConnection).sa_conn
        table = alch.FromInternal(sa.MetaData())(dc.replace(op.table, name=op.table.name[1:]))
        table.create(sa_conn)


class AtomicCreateTableAsExecutor(ConnsExecutor[ops.AtomicCreateTableAs]):

    def execute(self, op: ops.AtomicCreateTableAs) -> None:
        sa_conn = check.isinstance(self._conns[op.name[0]], SqlConnection).sa_conn
        sa_conn.execute(
            sql.CreateTableAs(
                sql.QualifiedNameElement(
                    QualifiedName(op.name[1:])),
                sa.text(op.query)))


class InsertIntoSelectExecutor(ConnsExecutor[ops.InsertIntoSelect]):

    def execute(self, op: ops.InsertIntoSelect) -> None:
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
                root = tpar.parse_statement(op.query)
                src = ctrs.ListRowSource(teval.StmtEvaluator().eval(root))

        if src is None:
            raise ValueError(op.query)

        dst_conn = self._conns[op.dst[0]]
        dst = dst_conn.create_row_sink(QualifiedName(op.dst[1:]))
        dst.consume_rows(src.produce_rows())
