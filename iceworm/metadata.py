"""
TODO:
 - *load and treat derived tables as table funcs*
  - transform jinja exprs to params
   - inJinjaPredicate -> array arg + contains pred
 - pk awareness
 - partition / clustering
 - slow vs fast changing
  - refresh interval awareness
 - alchemy reflection bidir adapter
 - serde
 - external tables from files
 - permanence
  - file? multi-git + merge? db?
  - versioning? hash? dumb autoinc?
 - exfiltration?
"""
import typing as ta

from omnibus import dataclasses as dc

from .datatypes import Datatype
from .types import QualifiedName


class Column(dc.Pure):
    name: str
    type: Datatype


class Table(dc.Pure):
    name: str
    columns: ta.Sequence[Column]

    schema: ta.Optional[str] = None
    catalog: ta.Optional[str] = None

    @property
    def qualified_name(self) -> QualifiedName:
        return QualifiedName(*filter(None, [self.catalog, self.schema, self.name]))
