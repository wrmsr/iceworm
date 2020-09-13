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


_TEST_FAILED_INCREMENTAL: ta.Dict[str, ta.Dict[ta.Tuple[int, ...], str]] = {}


def pytest_addoption(parser):
    parser.addoption('--no-slow', action='store_true', default=False, help='disable slow tests')
    parser.addoption('--no-online', action='store_true', default=False, help='disable online tests')


def pytest_configure(config):
    config.addinivalue_line('markers', 'slow: mark test as slow')
    config.addinivalue_line('markers', 'online: mark test as online only')


def pytest_collection_modifyitems(config, items):
    if config.getoption('--no-slow'):
        skip_slow = pytest.mark.skip(reason='omit --no-slow to run')
        for item in items:
            if 'slow' in item.keywords:
                item.add_marker(skip_slow)

    if config.getoption('--no-online'):
        skip_online = pytest.mark.skip(reason='omit --no-online to run')
        for item in items:
            if 'online' in item.keywords:
                item.add_marker(skip_online)


def pytest_runtest_setup(item):
    if 'incremental' in item.keywords:
        cls_name = str(item.cls)
        if cls_name in _TEST_FAILED_INCREMENTAL:
            parametrize_index = tuple(item.callspec.indices.values()) if hasattr(item, 'callspec') else ()
            test_name = _TEST_FAILED_INCREMENTAL[cls_name].get(parametrize_index, None)
            if test_name is not None:
                pytest.xfail('previous test failed ({})'.format(test_name))


def pytest_runtest_makereport(item, call):
    if 'incremental' in item.keywords:
        if call.excinfo is not None:
            cls_name = str(item.cls)
            parametrize_index = tuple(item.callspec.indices.values()) if hasattr(item, 'callspec') else ()
            test_name = item.originalname or item.name
            _TEST_FAILED_INCREMENTAL.setdefault(cls_name, {}).setdefault(parametrize_index, test_name)


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
