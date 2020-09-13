import types
import typing as ta

from omnibus import check

from .base import Op
from .base import OpExecutor


class OpExecutionDriver:

    def __init__(self, op_executors: ta.Mapping[ta.Type[Op], OpExecutor]) -> None:
        super().__init__()

        self._op_executors = {
            check.issubclass(k, Op): check.isinstance(v, OpExecutor)
            for k, v in op_executors.items()
        }

    def execute(self, plan: Op) -> None:
        check.isinstance(plan, Op)

        def execute(op: Op) -> None:
            executor = self._op_executors[type(op)]
            res = executor.execute(op)
            if isinstance(res, types.GeneratorType):
                for child in res:
                    execute(child)
            else:
                check.none(res)

        execute(plan)
