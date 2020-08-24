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

from .. import alchemy as alch
from .. import sql
from ..types import QualifiedName
from .connectors import ConnectionSet
from .ops import CreateTable
from .ops import CreateTableAs
from .ops import DropTable
from .ops import InsertIntoSelect
from .ops import Op
from .ops import Transaction
from .sql import SqlConnection
from .utils import parse_simple_select_star_table


OpT = ta.TypeVar('OpT', bound=Op)


class Executor(lang.Abstract, ta.Generic[OpT]):

    def __init__(self, conns: ConnectionSet) -> None:
        super().__init__()

        self._conns = check.isinstance(conns, ConnectionSet)

    @abc.abstractmethod
    def execute(self, op: OpT) -> ta.Union[None, ta.Generator[Op, None, None]]:
        raise NotImplementedError


class TransactionExecutor(Executor[Transaction]):

    def execute(self, op: Transaction) -> ta.Generator[Op, None, None]:
        sa_conn = check.isinstance(self._conns[check.single(op.conns)], SqlConnection).sa_conn
        with sa_conn.begin() as txn:
            try:
                for child in op.children:
                    yield child
                txn.commit()
            except Exception:
                txn.rollback()
                raise


class DropTableExecutor(Executor[DropTable]):

    def execute(self, op: DropTable) -> None:
        sa_conn = check.isinstance(self._conns[op.name[0]], SqlConnection).sa_conn
        sa_conn.execute(
            sql.DropTableIfExists(
                sql.QualifiedNameElement(
                    QualifiedName(op.name[1:]))))


class CreateTableExecutor(Executor[CreateTable]):

    def execute(self, op: CreateTable) -> None:
        sa_conn = check.isinstance(self._conns[op.table.name[0]], SqlConnection).sa_conn
        table = alch.FromInternal(sa.MetaData())(dc.replace(op.table, name=op.table.name[1:]))
        table.create(sa_conn)


class CreateTableAsExecutor(Executor[CreateTableAs]):

    def execute(self, op: CreateTableAs) -> None:
        sa_conn = check.isinstance(self._conns[op.name[0]], SqlConnection).sa_conn
        sa_conn.execute(
            sql.CreateTableAs(
                sql.QualifiedNameElement(
                    QualifiedName(op.name[1:])),
                sa.text(op.query)))


class InsertIntoSelectExecutor(Executor[InsertIntoSelect]):

    def execute(self, op: InsertIntoSelect) -> None:
        dst_conn = self._conns[op.dst[0]]

        src_name = parse_simple_select_star_table(op.query)
        src_conn = self._conns[src_name[0]]
        src_query = f"select * from {'.'.join(src_name[1:])}"

        dst = dst_conn.create_row_sink(QualifiedName(op.dst[1:]))
        src = src_conn.create_row_source(src_query)

        dst.consume_rows(src.produce_rows())
