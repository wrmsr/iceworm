from omnibus import dataclasses as dc
from omnibus import dispatch
from omnibus import lang

from . import ops
from .base import Op
from .utils import parse_simple_select_tables


class Origin(lang.Marker):
    pass


class Transformer(dispatch.Class, lang.Abstract):
    __call__ = dispatch.property()

    def __call__(self, op: Op, **kwargs) -> Op:  # noqa
        res = op.map(self, **kwargs)
        return dc.replace(res, meta={**res.meta, Origin: op})


class CreateTableAsAtomizer(Transformer):

    def __call__(self, op: ops.CreateTableAs) -> Op:  # noqa
        try:
            tbls = parse_simple_select_tables(op.query)
        except ValueError:
            return op
        if not all(tbl.parts[0] != op.name[0] for tbl in tbls):
            return op
        return ops.AtomicCreateTableAs(op.name, op.query, meta={**op.meta, Origin: op})
