"""
TODO:
 - def handles? strategies? InsertIntoFrom?
  - aot ops rewriting is more powerful than feuding greedy executors
"""
import abc
import typing as ta

from omnibus import check
from omnibus import lang
import sqlalchemy as sa

from .. import alchemy as alch
from .. import sql
from ..types import QualifiedName
from .connectors import ConnectionSet
from .connectors import TableRowSpec
from .ops import CreateTable
from .ops import CreateTableAs
from .ops import DropTable
from .ops import InsertInto
from .ops import Op
from .ops import SqlOp
from .ops import Transaction
from .sql import SqlConnection


OpT = ta.TypeVar('OpT', bound=Op)
SqlOpT = ta.TypeVar('SqlOpT', bound=SqlOp)


class Executor(lang.Abstract, ta.Generic[OpT]):

    @abc.abstractmethod
    def execute(self, op: OpT) -> ta.Union[None, ta.Generator[Op, None, None]]:
        raise NotImplementedError


class SqlExecutor(Executor[SqlOpT], lang.Abstract):

    def __init__(self, conns: ConnectionSet) -> None:
        super().__init__()

        self._conns = check.isinstance(conns, ConnectionSet)


class TransactionExecutor(SqlExecutor[Transaction]):

    def execute(self, op: Transaction) -> ta.Generator[Op, None, None]:
        sa_conn = check.isinstance(self._conns[op.conn_name], SqlConnection).sa_conn
        with sa_conn.begin() as txn:
            try:
                for child in op.children:
                    yield child
                txn.commit()
            except Exception:
                txn.rollback()
                raise


class DropTableExecutor(SqlExecutor[DropTable]):

    def execute(self, op: DropTable) -> None:
        sa_conn = check.isinstance(self._conns[op.table_name.parts[0]], SqlConnection).sa_conn
        sa_conn.execute(
            sql.DropTableIfExists(
                sql.QualifiedNameElement(
                    QualifiedName(op.table_name.parts[1:]))))


class CreateTableExecutor(SqlExecutor[CreateTable]):

    def execute(self, op: CreateTable) -> None:
        sa_conn = check.isinstance(self._conns[op.conn_name], SqlConnection).sa_conn
        table = alch.FromInternal(sa.MetaData())(op.table)
        table.create(sa_conn)


class CreateTableAsExecutor(SqlExecutor[CreateTableAs]):

    def execute(self, op: CreateTableAs) -> None:
        sa_conn = check.isinstance(self._conns[op.table_name.parts[0]], SqlConnection).sa_conn
        sa_conn.execute(
            sql.CreateTableAs(
                sql.QualifiedNameElement(
                    QualifiedName(op.table_name.parts[1:])),
                sa.text(op.query)))


class InsertIntoExecutor(SqlExecutor[InsertInto]):

    def execute(self, op: InsertInto) -> None:
        dst_conn = self._conns[op.dst_table_name.parts[0]]
        src_conn = self._conns[op.src_table_name.parts[0]]
        dst = dst_conn.create_row_sink(QualifiedName(op.dst_table_name.parts[1:]))
        src = src_conn.create_row_source(TableRowSpec(op.src_table_name.parts[1:]))
        dst.consume_rows(src.produce_rows())
