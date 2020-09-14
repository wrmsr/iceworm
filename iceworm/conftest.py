import typing as ta

from .tests.harness.fixtures import _scope_listener_class  # noqa
from .tests.harness.fixtures import _scope_listener_function  # noqa
from .tests.harness.fixtures import _scope_listener_module  # noqa
from .tests.harness.fixtures import _scope_listener_package  # noqa
from .tests.harness.fixtures import _scope_listener_session  # noqa
from .tests.harness.fixtures import harness  # noqa
from .tests.hooks import env
from .tests.hooks import incremental
from .tests.hooks import pycharm  # noqa
from .tests.hooks import switches


_TEST_FAILED_INCREMENTAL: ta.Dict[str, ta.Dict[ta.Tuple[int, ...], str]] = {}


def pytest_addoption(parser):
    switches.Hooks.addoption(parser)


def pytest_configure(config):
    env.Hooks.configure(config)
    switches.Hooks.configure(config)


def pytest_collection_modifyitems(config, items):
    switches.Hooks.collection_modifyitems(config, items)


def pytest_runtest_setup(item):
    incremental.Hooks.runtest_setup(item)


def pytest_runtest_makereport(item, call):
    incremental.Hooks.runtest_makereport(item, call)


def pytest_exception_interact(node, call, report):
    return pycharm.Hooks.exception_interact(node, call, report)
    # return report
