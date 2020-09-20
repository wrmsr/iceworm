from .tests import harness
from .tests import plugins


def pytest_addhooks(pluginmanager):
    for plugin in plugins.ALL:
        pluginmanager.register(plugin())
    pluginmanager.register(harness.HarnessPlugin())
