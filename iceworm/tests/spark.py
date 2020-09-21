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
from ..utils import find_free_port
from ..utils import ticking_timeout
from ..utils import timebomb
from .plugins import switches


@har.bind(har.Session)
class SparkManager(lc.ContextManageableLifecycle):

    def __init__(self, request: har.FixtureRequest) -> None:
        super().__init__()

        self._request = check.isinstance(request, har.FixtureRequest)

    TIMEOUT = 60

    @properties.stateful_cached
    @property
    def thrift_url(self) -> str:
        switches.skip_if_disabled(self._request, 'spark')

        port = find_free_port()
        url = f'hive://localhost:{port}/default'

        from pyhive import hive  # noqa
        from thrift.transport.TTransport import TTransportException

        def ping() -> bool:
            try:
                with lang.disposing(sa.create_engine(url)) as engine:
                    with engine.connect() as conn:
                        rows = list(conn.execute(sa.select([1])))
                check.state(check.single(check.single(rows)) == 1)
                return True
            except TTransportException as e:  # noqa
                return False

        if ping():
            return url

        spark_home = os.path.abspath(os.path.dirname(importlib.util.find_spec('pyspark').origin))
        exe = os.path.join(spark_home, 'sbin/spark-daemon.sh')
        check.state(os.path.isfile(exe))

        cls = 'org.apache.spark.sql.hive.thriftserver.HiveThriftServer2'
        args = [
            f'--hiveconf hive.server2.thrift.port={port}',
            '--name "Thrift JDBC/ODBC Server"',
        ]
        cwd = self._lifecycle_exit_stack.enter_context(oos.tmp_dir())
        env = {
            'HIVE_SERVER2_THRIFT_PORT': str(port),
            'JAVA_HOME': os.path.abspath(sl.LocalLauncher('exit(1)').java_home),
            'SPARK_HOME': spark_home,
        }

        setenv = ' '.join(f'{k}={v}' for k, v in env.items())
        start_cmd = f'cd {cwd} && {setenv} {exe} submit {cls} 1 {" ".join(args)}'
        stop_cmd = f'{setenv} {exe} stop {cls} 1'

        self._lifecycle_exit_stack.enter_context(lang.defer(lambda: os.system(stop_cmd)))
        self._lifecycle_exit_stack.enter_context(timebomb.start(stop_cmd, cwd=cwd, env={**os.environ, **env}, timeout=self.TIMEOUT))  # noqa
        os.system(start_cmd)

        tick = ticking_timeout(self.TIMEOUT)
        while not ping():
            tick()
            time.sleep(1)

        return url
