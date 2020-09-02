"""
TODO:
 - bootstrap:
  - git(-rev)-powered? - check for dirty + reject, check for rev pushed?
  - make vs setup.py.. reqs.txt..
   - just ship a reqs.txt w/ git+http://?
  - dist?

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
import operator
import tempfile
import textwrap
import typing as ta

from omnibus import lang
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


@skip_if_cant_import('pyspark')
def test_local_launcher():
    launcher = sl.LocalLauncher(textwrap.dedent(f"""
    from {__name__} import Driver
    Driver().drive()
    """))
    launcher.launch()


@pytest.mark.xfail()
def test_sql():
    # conn = hive.Connection(host='localhost', port=10000)
    # cur = conn.cursor()
    # print(list(cur.execute('select 1')))

    engine = sa.create_engine('hive://localhost:10000/default')
    with engine.connect() as conn:
        print(list(conn.execute(sa.select([1]))))
