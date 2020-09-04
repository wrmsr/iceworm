"""
TODO:
 - ** decree: QUARANTINE DEP - lazy_import, not required for core **
"""
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc


_PROTO_OBJS: ta.Mapping[str, type] = {}


def proto(**kwargs):
    def inner(obj):
        check.isinstance(obj, type)
        check.not_in(obj.__name__, _PROTO_OBJS)
        _PROTO_OBJS[obj.__name__] = obj
        return obj
    check.empty(kwargs)
    return inner


@proto()
class _Stub(dc.Pure):
    data: str
