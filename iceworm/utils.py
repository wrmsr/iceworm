import typing as ta

from omnibus import dataclasses as dc
from omnibus import defs


def build_dc_repr(obj: ta.Any) -> str:
    return defs.build_repr(obj, *[f.name for f in dc.fields(obj) if f.repr])
