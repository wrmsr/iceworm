import typing as ta

from omnibus import check
from omnibus import inject as inj

from . import base
from . import conns
from . import driving
from .base import Op
from .base import OpExecutor


def bind_op_executor(binder: inj.Binder, op_cls: ta.Type[Op], oe_cls: ta.Type[OpExecutor]) -> None:
    check.isinstance(binder, inj.Binder)

    binder.bind(oe_cls)
    binder.new_dict_binder(ta.Type[Op], OpExecutor).bind(op_cls, to=oe_cls)


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    binder.new_dict_binder(ta.Type[Op], OpExecutor)

    bind_op_executor(binder, base.List, base.ListExecutor)

    bind_op_executor(binder, conns.CreateTable, conns.CreateTableExecutor)
    bind_op_executor(binder, conns.CreateTableAs, conns.CreateTableAsExecutor)
    bind_op_executor(binder, conns.DropTable, conns.DropTableExecutor)
    bind_op_executor(binder, conns.InsertIntoSelect, conns.InsertIntoSelectExecutor)
    bind_op_executor(binder, conns.Transaction, conns.TransactionExecutor)

    binder.bind(driving.OpExecutionDriver)

    return binder
