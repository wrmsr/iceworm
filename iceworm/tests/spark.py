import importlib.util
import os.path
import time

from omnibus import check
from omnibus import lang
from omnibus import lifecycles as lc
from omnibus import os as oos
from omnibus import properties
from omnibus.spark import local as sl
import sqlalchemy as sa

from . import harness as har
from ..utils import ticking_timeout
from ..utils import timebomb
from .plugins import switches


@har.bind(har.Session)
class SparkManager(lc.ContextManageableLifecycle):

    def __init__(self, request: har.FixtureRequest) -> None:
        super().__init__()

        self._request = check.isinstance(request, har.FixtureRequest)

    TIMEOUT = 30

    @properties.stateful_cached
    @property
    def thrift_url(self) -> str:
        switches.skip_if_disabled(self._request, 'spark')

        from pyhive import hive  # noqa
        from thrift.transport.TTransport import TTransportException

        spark_home = os.path.abspath(os.path.dirname(importlib.util.find_spec('pyspark').origin))
        exe = os.path.join(spark_home, 'sbin/spark-daemon.sh')
        check.state(os.path.isfile(exe))

        cls = 'org.apache.spark.sql.hive.thriftserver.HiveThriftServer2'
        cwd = self._lifecycle_exit_stack.enter_context(oos.tmp_dir())
        env = {
            'JAVA_HOME': sl.LocalLauncher('exit(1)').java_home,
            'SPARK_HOME': spark_home,
        }

        start_cmd = f'cd {cwd} && {exe} submit {cls} 1 --name "Thrift JDBC/ODBC Server"'
        stop_cmd = f'{exe} stop {cls} 1'

        self._lifecycle_exit_stack.enter_context(lang.defer(lambda: os.system(stop_cmd)))
        self._lifecycle_exit_stack.enter_context(timebomb.start(stop_cmd, cwd=cwd, env=env, timeout=self.TIMEOUT))
        os.system(start_cmd)

        url = 'hive://localhost:10000/default'
        tick = ticking_timeout(self.TIMEOUT)
        while True:
            tick()
            try:
                with lang.disposing(sa.create_engine(url)) as engine:
                    with engine.connect() as conn:
                        rows = list(conn.execute(sa.select([1])))
                check.state(check.single(check.single(rows)) == 1)
                break
            except TTransportException as e:  # noqa
                pass
            time.sleep(1)

        return url
