"""
TODO:
 - bootstrap:
  - git(-rev)-powered? - check for dirty + reject, check for rev pushed?
  - make vs setup.py.. reqs.txt..
   - just ship a reqs.txt w/ git+http://?
  - dist?

https://docs.snowflake.com/en/user-guide/spark-connector-overview.html ?

https://spark.apache.org/docs/latest/sql-ref-syntax.html

https://github.com/SherpaConsulting/PyHiveSpark/blob/master/pyhive/sqlalchemy_spark.py
https://github.com/dropbox/PyHive/pull/247/files

(cd temp && \
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_261.jdk/Contents/Home \
SPARK_HOME=../.venv/lib/python3.7/site-packages/pyspark \
../.venv/lib/python3.7/site-packages/pyspark/sbin/spark-daemon.sh \
submit org.apache.spark.sql.hive.thriftserver.HiveThriftServer2 1 --name "Thrift JDBC/ODBC Server" \
)

(cd temp && \
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_261.jdk/Contents/Home \
SPARK_HOME=../.venv/lib/python3.7/site-packages/pyspark \
../.venv/lib/python3.7/site-packages/pyspark/sbin/spark-daemon.sh \
stop org.apache.spark.sql.hive.thriftserver.HiveThriftServer2 1 \
)
"""
import importlib.util
import operator
import os.path
import tempfile
import textwrap
import time
import typing as ta

from omnibus import check
from omnibus import lang
from omnibus import lifecycles as lc
from omnibus import os as oos
from omnibus import properties
from omnibus.dev.testing.helpers import skip_if_cant_import
from omnibus.spark import local as sl
from pyhive import hive  # noqa
import pytest
import sqlalchemy as sa

if ta.TYPE_CHECKING:
    import pyspark as ps
else:
    ps = lang.proxy_import('pyspark')

from . import harness as har
from ..utils import ticking_timeout
from ..utils import timebomb
from .plugins import switches


@har.bind(har.Session)
class SparkManager(lc.ContextManageableLifecycle):

    def __init__(self, request: har.FixtureRequest) -> None:
        super().__init__()

        self._request = check.isinstance(request, har.FixtureRequest)

    TIMEOUT = 20

    @properties.stateful_cached
    @property
    def thrift_url(self) -> str:
        switches.skip_if_disabled(self._request, 'spark')

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


class Driver:

    DEFAULT_CONFIGS = {
        'spark.speculation': 'false',
    }

    @properties.cached
    def session(self) -> 'ps.sql.SparkSession':
        ssb = ps.sql.SparkSession.builder
        ssb.appName('spark_virtualenv')
        for k, v in self.DEFAULT_CONFIGS.items():
            ssb.config(k, v)
        ssb.config('spark.sql.warehouse.dir', tempfile.mkdtemp())
        ss = ssb.getOrCreate()

        sc = ss.sparkContext
        log4j = sc._jvm.org.apache.log4j
        log4j.LogManager.getRootLogger().setLevel(log4j.Level.ERROR)

        return ss

    @properties.cached
    def context(self) -> 'ps.context.SparkContext':
        return self.session.sparkContext

    def drive(self):
        try:
            data = self.context.parallelize(list("Hello World"))
            counts = data \
                .map(lambda x: (x, 1)) \
                .reduceByKey(operator.add) \
                .sortBy(lambda x: x[1], ascending=False) \
                .collect()
            for word, count in counts:
                print("{}: {}".format(word, count))

        finally:
            self.context.stop()


@pytest.mark.spark
@skip_if_cant_import('pyspark')
def test_local_launcher():
    launcher = sl.LocalLauncher(textwrap.dedent(f"""
    from {__name__} import Driver
    Driver().drive()
    """))
    launcher.launch()


@pytest.mark.spark
def test_sql(harness: har.Harness):
    # conn = hive.Connection(host='localhost', port=10000)
    # cur = conn.cursor()
    # print(list(cur.execute('select 1')))

    engine = sa.create_engine(harness[SparkManager].thrift_url)
    with engine.connect() as conn:
        print(list(conn.execute(sa.select([1]))))
