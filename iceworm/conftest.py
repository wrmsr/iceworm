from omnibus.dev.pytest import plugins as oplugins
from omnibus.inject.dev import pytest as _  # noqa

from .tests import plugins


oplugins.switches.SWITCHES.extend([

])


def pytest_addhooks(pluginmanager):
    for plugin in oplugins.ALL:
        pluginmanager.register(plugin())
    for plugin in plugins.ALL:
        pluginmanager.register(plugin())


def pytest_configure(config):
    config.addinivalue_line('filterwarnings', 'ignore:omnibus module is marked as unstable:::')
