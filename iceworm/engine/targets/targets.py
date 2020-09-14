"""
TODO:
 - materialization conn: els.Ref[Connection.Config]
 - functions: js, py, sql, rpc
  - re py: isolation of gross pandas deps and shit..
  - ** revision tagging of py ** - no src to sha, pin to 'this' / site code ver
   - and later worker isolation? celery? :/ or just own fork server, spark style
    - also, pyspark/pyflink lol
  - re rpcs: if possible push into snowflake/spark/whatever (jvm support), if not do whole-table-at-a-time (rs accel?)
  - ** valid and useful to invalidate functions - should be detected at migration and triggerable for opaque rpcs **
   - optional rpc 'version' poller
"""
import typing as ta

from omnibus import dataclasses as dc

from .. import connectors as ctrs
from .. import elements as els
from ... import metadata as md_
from ...trees.types import Query
from ...types import QualifiedName


class Target(els.Element, abstract=True):
    pass


class Table(Target):
    id: els.Id = dc.field(None, check=els.id_check)
    md: ta.Optional[md_.Table] = dc.field(None, check=lambda o: o is None or isinstance(o, md_.Table))


class Rows(Target):
    table: els.Ref[Table] = dc.field(coerce=els.Ref.cls(Table).of)
    query: Query = dc.field(coerce=Query.of)


class Function(Target):
    id: els.Id = dc.field(None, check=els.id_check)


class Materialization(Target):
    table: els.Ref[Table] = dc.field(coerce=els.Ref.cls(Table).of)
    connector: els.Ref[ctrs.Connector.Config] = dc.field(coerce=els.Ref.cls(ctrs.Connector.Config).of)
    name: QualifiedName = dc.field(coerce=QualifiedName.of)

    readonly: bool = dc.field(False, kwonly=True)
