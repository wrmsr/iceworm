from omnibus import dataclasses as dc
from omnibus import dispatch
from omnibus import lang

from .base import Op


class Origin(lang.Marker):
    pass


class Transformer(dispatch.Class, lang.Abstract):
    __call__ = dispatch.property()

    def __call__(self, op: Op, **kwargs) -> Op:  # noqa
        res = op.map(self, **kwargs)
        return dc.replace(res, meta={**res.meta, Origin: op})
