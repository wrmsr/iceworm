import os.path
import typing as ta

from omnibus import lang

from .tests.harness import _scope_listener_class  # noqa
from .tests.harness import _scope_listener_function  # noqa
from .tests.harness import _scope_listener_module  # noqa
from .tests.harness import _scope_listener_package  # noqa
from .tests.harness import _scope_listener_session  # noqa
from .tests.harness import harness  # noqa


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
