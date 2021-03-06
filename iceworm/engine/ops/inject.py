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

    binder.bind_scope(ExecutionScope)
    binder.bind_callable(lambda: lang.raise_(RuntimeError), key=inj.Key(ctrs.ConnectorSet), in_=ExecutionScope)
    binder.bind_callable(lambda: lang.raise_(RuntimeError), key=inj.Key(ctrs.ConnectionSet), in_=ExecutionScope)

    binder.new_dict_binder(ta.Type[Op], OpExecutor)

    bind_op_executor(binder, base.List, base.ListExecutor)

    bind_op_executor(binder, conns.CreateTable, conns.CreateTableExecutor)
    bind_op_executor(binder, conns.CreateTableAs, conns.CreateTableAsExecutor)
    bind_op_executor(binder, conns.DropTable, conns.DropTableExecutor)
    bind_op_executor(binder, conns.Exec, conns.ExecExecutor)
    bind_op_executor(binder, conns.InsertIntoEval, conns.InsertIntoEvalExecutor)
    bind_op_executor(binder, conns.InsertIntoSelect, conns.InsertIntoSelectExecutor)
    bind_op_executor(binder, conns.Transaction, conns.TransactionExecutor)

    binder.bind(driving.OpExecutionDriver)

    return binder


def bind_execution_module(binder: inj.Binder, module: ta.Callable[[inj.Binder], ta.Any]) -> None:
    check.isinstance(binder, inj.Binder)
    check.callable(module)

    binder.new_set_binder(ta.Callable[[inj.Binder], None], annotated_with='execution').bind(to_instance=module)


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    def check_binds(injector: inj.Injector) -> None:
        check.empty(injector[ta.Mapping[ta.Type[Op], OpExecutor]])

    binder.new_dict_binder(ta.Type[Op], OpExecutor)
    binder.bind_callable(check_binds, key=inj.Key(object, check_binds), as_eager_singleton=True)

    bind_execution_module(binder, _install_execution)

    @inj.annotate('execution', mods='execution')
    def provide_execution_injector(injector: inj.Injector, mods: ta.AbstractSet[ta.Callable[[inj.Binder], None]]) -> inj.Injector:  # noqa
        bnd = inj.create_binder()
        for mod in mods:
            mod(bnd)
        return injector.create_child(bnd)

    binder.bind_callable(provide_execution_injector, as_eager_singleton=True)

    return binder
