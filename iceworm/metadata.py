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
import abc
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from . import datatypes as dt
from .types import QualifiedName
from .utils import abs_set
from .utils import mapping
from .utils import seq
from .utils import unique_dict


ObjectT = ta.TypeVar('ObjectT', bound='Object')


class Object(dc.Enum, allow_setattr=True, reorder=True):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
    aliases: ta.AbstractSet[QualifiedName] = dc.field(
        (), kwonly=True, coerce=abs_set, check=lambda l: all(isinstance(o, QualifiedName) for o in l))

    dc.check(lambda name, aliases: name not in aliases)

    @abc.abstractproperty
    def type(self) -> dt.Datatype:
        raise NotImplementedError


class Column(dc.Pure):
    name: str = dc.field(check=lambda o: isinstance(o, str) and o)
    type: dt.Datatype = dc.field(check=lambda o: isinstance(o, dt.Datatype))

    primary_key: bool = dc.field(False, kwonly=True, check=lambda o: isinstance(o, bool))


class Table(Object):
    columns: ta.Sequence[Column] = dc.field(coerce=seq, check=lambda l: all(isinstance(o, Column) for o in l))

    def __post_init__(self) -> None:
        self._columns_by_name: ta.Mapping[str, Column] = unique_dict((c.name, c) for c in self.columns)
        self._type = dt.Table([(c.name, c.type) for c in self.columns])

    @property
    def columns_by_name(self) -> ta.Mapping[str, Column]:
        return self._columns_by_name

    @property
    def type(self) -> dt.Table:
        return self._type


class Function(Object):
    type: dt.Datatype = dc.field(check=lambda o: isinstance(o, dt.Datatype))
    params: ta.Mapping[str, dt.Datatype] = dc.field(
        coerce=mapping, check=lambda d: all(isinstance(k, str) and isinstance(v, dt.Datatype) for k, v in d.items()))


def _build_obj_map(objs: ta.Iterable[ObjectT], cls: ta.Type[ObjectT]) -> ta.Mapping[QualifiedName, ObjectT]:
    return unique_dict(
        (n, o)
        for o in objs
        for _ in [check.isinstance(o, cls)]
        for n in [o.name, *(o.aliases or [])]
    )


class Catalog(dc.Frozen, final=True, allow_setattr=True):
    tables: ta.Sequence[Table] = dc.field((), coerce=seq, check=lambda l: all(isinstance(o, Table) for o in l))
    functions: ta.Sequence[Function] = dc.field((), coerce=seq, check=lambda l: all(isinstance(o, Function) for o in l))

    def __post_init__(self) -> None:
        self._tables_by_name: ta.Mapping[QualifiedName, Table] = _build_obj_map(self.tables, Table)
        self._functions_by_name: ta.Mapping[QualifiedName, Function] = _build_obj_map(self.functions, Function)

    @property
    def tables_by_name(self) -> ta.Mapping[QualifiedName, Table]:
        return self._tables_by_name

    @property
    def functions_by_name(self) -> ta.Mapping[QualifiedName, Function]:
        return self._functions_by_name
