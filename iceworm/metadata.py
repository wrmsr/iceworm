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
  - boostrap / publish / dl slug / refresh
   - git bot?
  - file? multi-git + merge? db?
  - versioning? hash? dumb autoinc?
 - exfiltration?
 - *record all statements as executed w/ pk/partition ranges -> use interval ops for persisted lineage*
 - no views - nullary table funcs usable without parens
  - call them 'view's?
"""
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import properties

from .datatypes import Datatype
from .types import QualifiedName
from .utils import mapping
from .utils import seq
from .utils import unique_dict


class Column(dc.Pure):
    name: str
    type: Datatype

    primary_key: bool = dc.field(False, kwonly=True)


class Object(lang.Abstract):
    pass


class Table(dc.Frozen, Object, final=True, allow_setattr=True, reorder=True):
    name: str = dc.field(check=lambda o: isinstance(o, str))
    schema_name: ta.Optional[str] = dc.field(None, kwonly=True, check=lambda o: isinstance(o, (str, type(None))))
    catalog_name: ta.Optional[str] = dc.field(None, kwonly=True, check=lambda o: isinstance(o, (str, type(None))))

    columns: ta.Sequence[Column] = dc.field(coerce=seq)

    def __post_init__(self) -> None:
        self._columns_by_name: ta.Mapping[str, Column] = unique_dict((c.name, c) for c in self.columns)

    @property
    def columns_by_name(self) -> ta.Mapping[str, Column]:
        return self._columns_by_name

    @properties.cached
    def qualified_name(self) -> QualifiedName:
        return QualifiedName(*filter(None, [self.catalog, self.schema_name, self.name_name]))


class Function(dc.Frozen, Object, final=True, allow_setattr=True, reorder=True):
    name: str
    type: Datatype
    params: ta.Mapping[str, Datatype] = dc.field(coerce=mapping)


class Catalog(dc.Frozen, final=True, allow_setattr=True):
    tables: ta.Sequence[Table] = dc.field((), coerce=seq)
    functions: ta.Sequence[Function] = dc.field((), coerce=seq)

    def __post_init__(self) -> None:
        self._tables_by_name: ta.Mapping[str, Table] = unique_dict((t.name, check.isinstance(t, Table)) for t in self.tables)  # noqa
        self._functions_by_name: ta.Mapping[str, Function] = unique_dict((f.name, check.isinstance(f, Function)) for f in self.functions)  # noqa

    @property
    def tables_by_name(self) -> ta.Mapping[str, Table]:
        return self._tables_by_name

    @property
    def functions_by_name(self) -> ta.Mapping[str, Function]:
        return self._functions_by_name
