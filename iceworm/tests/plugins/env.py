import os
import typing as ta

from omnibus import lang

from ._registry import register


@lang.cached_nullary
def _load_dot_env() -> ta.Optional[ta.Mapping[str, str]]:
    fp = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../../.env')
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


@register
class EnvPlugin:

    def pytest_addoption(self, parser):
        parser.addoption('--no-dotenv', action='store_true', help='Disables dotenv')

    def pytest_configure(self, config):
        if not config.option.no_dotenv:
            _load_dot_env()
