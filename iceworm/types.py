"""
TODO:
  - quoting
"""
import typing as ta

from omnibus import collections as ocol
from omnibus import dataclasses as dc


class QualifiedName(dc.Pure):
    parts: ta.Sequence[str] = dc.field(coerce=ocol.frozenlist)

    @property
    def dotted(self) -> str:
        return '.'.join(self.parts)

    def __iter__(self) -> ta.Iterator[str]:
        return iter(self.parts)

    @classmethod
    def of_dotted(cls, dotted: str) -> 'QualifiedName':
        return cls(tuple(dotted.split('.')))
