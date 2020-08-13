import collections
import typing as ta

from omnibus import collections as ocol
from omnibus import dataclasses as dc

from ..types import QualifiedName
from ..utils import build_dc_repr
from ..utils import seq


SelfOp = ta.TypeVar('SelfOp', bound='Op')
OpGen = ta.Generator['Op', None, None]
OpMapper = ta.Callable[['Op'], 'Op']


class Op(dc.Enum):

    __repr__ = build_dc_repr

    def yield_field_children(self, fld: dc.Field) -> OpGen:
        val = getattr(self, fld.name)
        if isinstance(val, Op):
            yield val
        elif isinstance(val, collections.abc.Sequence):
            yield from (item for item in val if isinstance(item, Op))

    @property
    def children(self) -> OpGen:
        for fld in dc.fields(self):
            yield from self.yield_field_children(fld)

    def build_field_map_kwargs(self, fn: OpMapper, fld: dc.Field) -> ta.Mapping[str, ta.Any]:
        val = getattr(self, fld.name)
        if isinstance(val, Op):
            return {fld.name: fn(val)}
        elif isinstance(val, collections.abc.Sequence) and not isinstance(val, str):
            return {fld.name: ocol.frozenlist([fn(item) if isinstance(item, Op) else item for item in val])}
        else:
            return {}

    def map(self: SelfOp, fn: OpMapper, **kwargs) -> SelfOp:
        rpl_kw = {**kwargs}
        for fld in dc.fields(self):
            if fld.name in kwargs:
                continue
            for k, v in self.build_field_map_kwargs(fn, fld).items():
                if k in rpl_kw:
                    raise KeyError(k)
                rpl_kw[k] = v
        return dc.replace(self, **rpl_kw)


class Transaction(Op):
    children: ta.Sequence[Op] = dc.field(coerce=seq)


class DropTable(Op):
    name: QualifiedName = dc.field(check=lambda v: isinstance(v, QualifiedName))


class CreateTableAs(Op):
    name: QualifiedName = dc.field(check=lambda v: isinstance(v, QualifiedName))
    query: str
