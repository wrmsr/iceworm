from .tests import harness  # noqa
from .tests import plugins


def pytest_addhooks(pluginmanager):
    for plugin in plugins.ALL:
        pluginmanager.register(plugin())
