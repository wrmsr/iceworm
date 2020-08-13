import abc
import typing as ta

from omnibus import check
from omnibus import lang
from omnibus import sql as osql
import sqlalchemy as sa

from .. import sql
from .tasks import CreateTableAs
from .tasks import DropTable
from .tasks import Task
from .tasks import Transaction


TaskT = ta.TypeVar('TaskT', bound=Task)


class Executor(lang.Abstract, ta.Generic[TaskT]):

    @abc.abstractmethod
    def execute(self, task: TaskT) -> ta.Union[None, ta.Generator[Task, None, None]]:
        raise NotImplementedError


class DbExecutor(Executor[TaskT], lang.Abstract):

    def __init__(self, conn: sa.engine.Connection) -> None:
        super().__init__()

        self._conn = check.isinstance(conn, sa.engine.Connection)


class TransactionExecutor(DbExecutor[Transaction]):

    def execute(self, task: Transaction) -> ta.Generator[Task, None, None]:
        with self._conn.begin():
            for child in task.children:
                yield child


class DropTableExecutor(DbExecutor[DropTable]):

    def execute(self, task: DropTable) -> None:
        self._conn.execute(sql.DropTableIfExists(task.table_name))


class CreateTableAsExecutor(DbExecutor[CreateTableAs]):

    def execute(self, task: CreateTableAs) -> None:
        self._conn.execute(sql.CreateTableAs(task.table_name, sa.text(task.query)))
