from omnibus.lang.imports import ignore_unstable_warn

ignore_unstable_warn()


import os.path  # noqa

from omnibus.inject.dev import pytest as injp  # noqa
from omnibus.docker.dev import pytest as dckp  # noqa

injp.bind_instance(injp.Session, dckp.Prefix('iceworm-'))
injp.bind_instance(injp.Session, dckp.ComposePath(os.path.join(os.path.dirname(__file__), '../docker/docker-compose.yml')))  # noqa


from omnibus.dev.pytest import plugins as oplugins  # noqa

from .tests import plugins  # noqa

oplugins.ALL.extend(plugins.ALL)

oplugins.switches.SWITCHES.extend([

])


def pytest_addhooks(pluginmanager):
    for plugin in oplugins.ALL:
        pluginmanager.register(plugin())


def pytest_configure(config):
    config.addinivalue_line('filterwarnings', 'ignore:omnibus module is marked as unstable:::')
