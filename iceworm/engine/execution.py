import contextlib
import inspect
import typing as ta

from omnibus import check

from . import connectors as ctrs
from . import ops
from .ops import executors as exes
from .ops import Op
from .ops import transforms as tfm


class PlanExecutor:

    def __init__(self, plan: ops.Op, ctors: ta.Iterable[ctrs.Connector]) -> None:
        super().__init__()

        self._plan = check.isinstance(plan, ops.Op)
        self._ctors = ctrs.ConnectorSet.of(ctors)

    def execute(self) -> None:
        with contextlib.ExitStack() as es:
            conns = es.enter_context(contextlib.closing(ctrs.ConnectionSet(self._ctors)))

            executors_by_op_cls = {
                ops.AtomicCreateTableAs: exes.AtomicCreateTableAsExecutor(conns),
                ops.CreateTable: exes.CreateTableExecutor(conns),
                ops.DropTable: exes.DropTableExecutor(conns),
                ops.InsertIntoSelect: exes.InsertIntoSelectExecutor(conns),
                ops.List: exes.ListExecutor(),
                ops.Transaction: exes.TransactionExecutor(conns),
            }

            def execute(op: Op) -> None:
                executor = executors_by_op_cls[type(op)]
                if inspect.isgeneratorfunction(executor.execute):
                    for child in executor.execute(op):
                        execute(child)
                else:
                    check.none(executor.execute(op))

            root = ops.Transaction({'pg'}, self._plan)

            root = tfm.CreateTableAsAtomizer()(root)

            execute(root)
