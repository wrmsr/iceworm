import contextlib
import os.path
import typing as ta  # noqa

from omnibus import inject as inj
from omnibus import os as oos  # noqa
import pytest

from . import inject  # noqa
from .. import connectors as ctrs
from .. import execution as exe
from .. import planning as pln
from .. import sites  # noqa
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

        drv = inject._Driver(binder, inject.install(inj.create_binder()))
        elements = drv.run([
            sites.Site('site0.yml'),
        ])

        print(elements)

        connectors = drv._injector[ctrs.ConnectorSet]

        plan = pln.ElementPlanner(elements, connectors).plan({
            'pg/a',
            'pg/b',
            'pg/c',
            'pg/nums',
            'system/notifications',
        })

        exe.PlanExecutor(plan, connectors).execute()

        with harness[DbManager].pg_engine.connect() as pg_conn:
            print(list(pg_conn.execute('select * from a')))
            print(list(pg_conn.execute('select * from b')))
            print(list(pg_conn.execute('select * from c')))
            print(list(pg_conn.execute('select * from nums')))
