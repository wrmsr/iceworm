import os.path
import typing as ta

from omnibus import lang
import pytest

from .tests.harness.fixtures import _scope_listener_class  # noqa
from .tests.harness.fixtures import _scope_listener_function  # noqa
from .tests.harness.fixtures import _scope_listener_module  # noqa
from .tests.harness.fixtures import _scope_listener_package  # noqa
from .tests.harness.fixtures import _scope_listener_session  # noqa
from .tests.harness.fixtures import harness  # noqa


def pytest_addoption(parser):
    parser.addoption('--offline', action='store_true', default=False, help='disable online tests')


def pytest_configure(config):
    config.addinivalue_line('markers', 'online: mark test as online only')


def pytest_collection_modifyitems(config, items):
    if not config.getoption('--offline'):
        return
    skip_online = pytest.mark.skip(reason='omit --offline to run')
    for item in items:
        if 'online' in item.keywords:
            item.add_marker(skip_online)


# FIXME: gross
@lang.cached_nullary
def _load_dot_env() -> ta.Optional[ta.Mapping[str, str]]:
    fp = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if not os.path.isfile(fp):
        return None
    with open(fp, 'r') as f:
        buf = f.read()
    ret = {}
    for line in buf.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        k, _, v = line.partition('=')
        k = k.strip()
        v = v.strip()
        ret[k] = v
        os.environ[k] = v
    return ret


_load_dot_env()
