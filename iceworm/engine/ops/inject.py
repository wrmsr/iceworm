import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dynamic as dyn
from omnibus import inject as inj
from omnibus import lang

from . import base
from . import conns
from . import driving
from .. import connectors as ctrs
from .base import Op
from .base import OpExecutor


T = ta.TypeVar('T')


class ExecutionScope(inj.Scope):

    def provide(self, binding: inj.Binding[T]) -> T:
        vals = self._CURRENT()
        try:
            return vals[binding]
        except KeyError:
            try:
                val = vals[binding.key.type]
            except KeyError:
                val = binding.provide()
            vals[binding] = val
            return val

    _CURRENT: dyn.Var[ta.MutableMapping[ta.Union[type, inj.Binding], ta.Any]] = dyn.Var()  # noqa


@dyn.contextmanager
def new_execution_scope(injector: inj.Injector, conns: ctrs.ConnectionSet) -> ta.Generator[None, None, None]:
    check.isinstance(injector, inj.Injector)
    check.isinstance(conns, ctrs.ConnectionSet)
    vals = ocol.IdentityKeyDict()
    with ExecutionScope._CURRENT(vals):
        with injector._CURRENT(injector):
            vals[ctrs.ConnectionSet] = conns
            vals[ctrs.ConnectorSet] = conns.connectors
        yield


def bind_op_executor(binder: inj.Binder, op_cls: ta.Type[Op], oe_cls: ta.Type[OpExecutor]) -> None:
    check.isinstance(binder, inj.Binder)

    binder.bind(oe_cls)
    binder.new_dict_binder(ta.Type[Op], OpExecutor).bind(op_cls, to=oe_cls)


def _install_execution(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    binder._elements.append(inj.types.ScopeBinding(ExecutionScope))
    binder.bind_callable(lambda: lang.raise_(RuntimeError), key=inj.Key(ctrs.ConnectorSet), in_=ExecutionScope)
    binder.bind_callable(lambda: lang.raise_(RuntimeError), key=inj.Key(ctrs.ConnectionSet), in_=ExecutionScope)

    binder.new_dict_binder(ta.Type[Op], OpExecutor)

    bind_op_executor(binder, base.List, base.ListExecutor)

    bind_op_executor(binder, conns.CreateTable, conns.CreateTableExecutor)
    bind_op_executor(binder, conns.CreateTableAs, conns.CreateTableAsExecutor)
    bind_op_executor(binder, conns.DropTable, conns.DropTableExecutor)
    bind_op_executor(binder, conns.InsertIntoEval, conns.InsertIntoEvalExecutor)
    bind_op_executor(binder, conns.InsertIntoSelect, conns.InsertIntoSelectExecutor)
    bind_op_executor(binder, conns.Transaction, conns.TransactionExecutor)

    binder.bind(driving.OpExecutionDriver)

    return binder


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    binder.new_set_binder(ta.Callable[[inj.Binder], None], annotated_with='execution').bind(to_instance=_install_execution)  # noqa

    return binder
