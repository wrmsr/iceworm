import sys

if sys.version_info < (3, 7):
    raise EnvironmentError('python >= 3.7 required')

import warnings as _warnings

from omnibus import lang as _lang

_warnings.filterwarnings('ignore', category=_lang.UnstableWarning)
