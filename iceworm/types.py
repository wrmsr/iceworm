import typing as ta

from omnibus import dataclasses as dc


class QualifiedName(dc.Pure):
    parts: ta.Sequence[str]
