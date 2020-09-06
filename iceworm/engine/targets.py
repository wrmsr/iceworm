import typing as ta

from omnibus import dataclasses as dc

from .. import metadata as md_
from ..types import QualifiedName
from .elements import Element


class Target(Element, abstract=True):
    pass


class Table(Target):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
    md: ta.Optional[md_.Table] = dc.field(None, check=lambda o: o is None or isinstance(o, md_.Table))

    dc.check(lambda name, md: md is None or name == md.name)


class Rows(Target):
    table: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))

    name: ta.Optional[QualifiedName] = dc.field(None, coerce=QualifiedName.of_optional, kwonly=True)


class Function(Target):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
