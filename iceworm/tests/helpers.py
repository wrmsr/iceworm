"""
TODO:
 - db setup/teardown
 - all docker compose services
"""
import threading
import typing as ta


T = ta.TypeVar('T')


DEFAULT_TIMEOUT_S = 30


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
