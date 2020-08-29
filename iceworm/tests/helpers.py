"""
TODO:
 - db setup/teardown
 - all docker compose services
"""
from omnibus import check
from omnibus import code as oco
from omnibus import docker
from omnibus import lang
import pytest


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


@pytest_callable_fixture()
@lang.cached_nullary
def pg_url():
    if docker.is_in_docker():
        (host, port) = 'iceworm-postgres', 5432

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_iceworm-postgres_1', 5432)])

        [(host, port)] = eps.values()

    return f'postgresql+psycopg2://iceworm:iceworm@{host}:{port}'
