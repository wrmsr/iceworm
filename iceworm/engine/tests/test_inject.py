import contextlib
import os.path
import typing as ta  # noqa

from omnibus import inject as inj
from omnibus import os as oos  # noqa
import pytest

from . import inject  # noqa
from .. import connectors as ctrs
from ...sql.tests.helpers import DbManager
from ...tests import harness as har
from ...types import QualifiedName  # noqa
from ...utils import secrets as sec  # noqa


@pytest.mark.xfail()
def test_inject(harness: har.Harness):
    with contextlib.ExitStack() as es:
        es.enter_context(oos.tmp_chdir(os.path.dirname(__file__)))

        secrets = sec.Secrets({'pg_url': harness[DbManager].pg_url})

        binder = inj.create_binder()
        binder.bind(sec.Secrets, to_instance=secrets)

        inject._Driver(binder, inject.install(inj.create_binder())).run([
            ctrs.system.SystemConnector.Config(),
        ])
