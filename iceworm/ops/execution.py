import abc
import typing as ta

from omnibus import check
from omnibus import lang
import sqlalchemy as sa

from .. import alchemy as alch
from .. import metadata as md
from .. import sql
from .ops import CreateTable
from .ops import CreateTableAs
from .ops import DropTable
from .ops import InsertInto
from .ops import Op
from .ops import SqlOp
from .ops import Transaction


OpT = ta.TypeVar('OpT', bound=Op)
SqlOpT = ta.TypeVar('SqlOpT', bound=SqlOp)


class Executor(lang.Abstract, ta.Generic[OpT]):

    @abc.abstractmethod
    def execute(self, op: OpT) -> ta.Union[None, ta.Generator[Op, None, None]]:
        raise NotImplementedError


class SqlExecutor(Executor[SqlOpT], lang.Abstract):

    def __init__(self, conn: sa.engine.Connection) -> None:
        super().__init__()

        self._conn = check.isinstance(conn, sa.engine.Connection)


class TransactionExecutor(SqlExecutor[Transaction]):

    def execute(self, op: Transaction) -> ta.Generator[Op, None, None]:
        with self._conn.begin() as txn:
            try:
                for child in op.children:
                    yield child
                txn.commit()
            except Exception:
                txn.rollback()
                raise


class DropTableExecutor(SqlExecutor[DropTable]):

    def execute(self, op: DropTable) -> None:
        self._conn.execute(sql.DropTableIfExists(sql.QualifiedNameElement(op.name)))


class CreateTableExecutor(SqlExecutor[CreateTable]):

    def execute(self, op: CreateTable) -> None:
        table = alch.FromInternal(sa.MetaData())(op.table)
        table.create(self._conn)


class CreateTableAsExecutor(SqlExecutor[CreateTableAs]):

    def execute(self, op: CreateTableAs) -> None:
        self._conn.execute(sql.CreateTableAs(sql.QualifiedNameElement(op.name), sa.text(op.query)))


class InsertIntoExecutor(SqlExecutor[InsertInto]):

    def __init__(self, conn: sa.engine.Connection, catalog: md.Catalog) -> None:
        super().__init__(conn)

        self._catalog = check.isinstance(catalog, md.Catalog)

    def execute(self, op: InsertInto) -> None:
        raise NotImplementedError
