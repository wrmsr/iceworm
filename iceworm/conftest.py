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

_TEST_SWITCHES = [
    'docker',
    'online',
    'slow',
]


def pytest_addoption(parser):
    for sw in _TEST_SWITCHES:
        parser.addoption(f'--no-{sw}', action='store_true', default=False, help=f'disable {sw} tests')


def pytest_configure(config):
    for sw in _TEST_SWITCHES:
        config.addinivalue_line('markers', f'{sw}: mark test as {sw}')


def pytest_collection_modifyitems(config, items):
    for sw in _TEST_SWITCHES:
        if not config.getoption(f'--no-{sw}'):
            continue
        skip = pytest.mark.skip(reason=f'omit --no-{sw} to run')
        for item in items:
            if sw in item.keywords:
                item.add_marker(skip)


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

    # if call.excinfo is not None:
    #     from .tests.helpers import XfailException
    #     if call.excinfo.type == XfailException:
    #         from _pytest.reports import TestReport
    #         return TestReport.from_item_and_call(item, call)


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
