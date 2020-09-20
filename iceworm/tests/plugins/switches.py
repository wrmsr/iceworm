from omnibus import check
from omnibus import lang
import pytest

from ._registry import register


SWITCHES = [
    'docker',
    'online',
    'slow',
    'spark',
]


def is_disabled(request, name: str) -> bool:
    check.isinstance(name, str)
    check.in_(name, SWITCHES)
    return request is not None and request.config.getoption(f'--no-{name}')


def skip_if_disabled(request, name: str) -> None:
    if is_disabled(request, name):
        pytest.skip(f'{name} disabled')


@register
class SwitchesPlugin(lang.Namespace):

    @staticmethod
    def pytest_addoption(parser):
        for sw in SWITCHES:
            parser.addoption(f'--no-{sw}', action='store_true', default=False, help=f'disable {sw} tests')

    @staticmethod
    def pytest_configure(config):
        for sw in SWITCHES:
            config.addinivalue_line('markers', f'{sw}: mark test as {sw}')

    @staticmethod
    def pytest_collection_modifyitems(config, items):
        for sw in SWITCHES:
            if not config.getoption(f'--no-{sw}'):
                continue
            skip = pytest.mark.skip(reason=f'omit --no-{sw} to run')
            for item in items:
                if sw in item.keywords:
                    item.add_marker(skip)
