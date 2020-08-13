import collections
import typing as ta

from omnibus import collections as ocol
from omnibus import dataclasses as dc

from ..utils import build_dc_repr
from ..utils import mapping
from ..utils import seq


SelfTask = ta.TypeVar('SelfTask', bound='Task')
TaskGen = ta.Generator['Task', None, None]
TaskMapper = ta.Callable[['Task'], 'Task']


class Task(dc.Enum):

    __repr__ = build_dc_repr

    def yield_field_children(self, fld: dc.Field) -> TaskGen:
        val = getattr(self, fld.name)
        if isinstance(val, Task):
            yield val
        elif isinstance(val, collections.abc.Sequence):
            yield from (item for item in val if isinstance(item, Task))

    @property
    def children(self) -> TaskGen:
        for fld in dc.fields(self):
            yield from self.yield_field_children(fld)

    def build_field_map_kwargs(self, fn: TaskMapper, fld: dc.Field) -> ta.Mapping[str, ta.Any]:
        val = getattr(self, fld.name)
        if isinstance(val, Task):
            return {fld.name: fn(val)}
        elif isinstance(val, collections.abc.Sequence) and not isinstance(val, str):
            return {fld.name: ocol.frozenlist([fn(item) if isinstance(item, Task) else item for item in val])}
        else:
            return {}

    def map(self: SelfTask, fn: TaskMapper, **kwargs) -> SelfTask:
        rpl_kw = {**kwargs}
        for fld in dc.fields(self):
            if fld.name in kwargs:
                continue
            for k, v in self.build_field_map_kwargs(fn, fld).items():
                if k in rpl_kw:
                    raise KeyError(k)
                rpl_kw[k] = v
        return dc.replace(self, **rpl_kw)


class Transaction(Task):
    children: ta.Sequence[Task] = dc.field(coerce=seq)


class DropTable(Task):
    table_name: str


class CreateTableAs(Task):
    table_name: str
    query: str
