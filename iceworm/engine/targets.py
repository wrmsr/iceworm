"""
TODO:
 - materialization conn: els.Ref[Connection.Config]
"""
import typing as ta

from omnibus import dataclasses as dc

from . import elements as els
from .. import metadata as md_
from ..types import QualifiedName


class Target(els.Element, abstract=True):
    pass


class Table(Target):
    name: str = dc.field(None, check=els.name_check)
    md: ta.Optional[md_.Table] = dc.field(None, check=lambda o: o is None or isinstance(o, md_.Table))


class Rows(Target):
    table: els.Ref[Table] = dc.field(coerce=els.Ref.cls(Table).of)
    query: str = dc.field(check=lambda o: isinstance(o, str))


class Function(Target):
    name: str = dc.field(None, check=els.name_check)


class Materialization(Target):
    table: els.Ref[Table] = dc.field(coerce=els.Ref.cls(Table).of)
    dst: QualifiedName = dc.field(coerce=QualifiedName.of)
