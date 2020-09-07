"""
TODO:
 - db setup/teardown
 - all docker compose services
"""
import threading
import typing as ta

from omnibus import check
from omnibus import code as oco
import pytest


T = ta.TypeVar('T')


DEFAULT_TIMEOUT_S = 30


def pytest_callable_fixture(*fxargs, **fxkwargs):
    """Fuck off pytest."""

    def inner(fn):
        fixture = pytest.fixture(*fxargs, **fxkwargs)(fn)

        def override(*args, **kwargs):
            nonlocal fn
            return 1(*args, **kwargs)  # noqa

        code = override.__code__
        check.state(code.co_consts == (None, 1))
        newcodeargs = [getattr(code, f'co_{a}') for a in oco.CODE_ARGS]
        newcodeargs[oco.CODE_ARGS.index('consts')] = (None, fn)
        fixture.__code__ = type(code)(*newcodeargs)

        return fixture

    return inner


def call_many_with_timeout(
        fns: ta.Iterable[ta.Callable[[], T]],
        timeout_s: int = None,
        timeout_exception: Exception = RuntimeError('Thread timeout'),
) -> ta.List[T]:
    if timeout_s is None:
        timeout_s = DEFAULT_TIMEOUT_S

    fns = list(fns)
    missing = object()
    rets: T = [missing] * len(fns)
    thread_exception: ta.Optional[Exception] = None

    def inner(fn, idx):
        try:
            nonlocal rets
            rets[idx] = fn()
        except Exception as e:
            nonlocal thread_exception
            thread_exception = e
            raise

    threads = [threading.Thread(target=inner, args=(fn, idx)) for idx, fn in enumerate(fns)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout_s)
    for thread in threads:
        if thread.is_alive():
            raise timeout_exception

    if thread_exception is not None:
        raise thread_exception
    for ret in rets:
        if ret is missing:
            raise ValueError

    return rets


def run_with_timeout(
        *fns: ta.Callable[[], None],
        timeout_s: int = None,
        timeout_exception: Exception = RuntimeError('Thread timeout'),
) -> None:
    call_many_with_timeout(fns, timeout_s, timeout_exception)
