"""
TODO:
  - quoting
"""
import collections.abc
import typing as ta

from omnibus import dataclasses as dc

from .utils import seq


class QualifiedName(dc.Pure):
    parts: ta.Sequence[str] = dc.field(coerce=seq)

    dc.check(lambda parts: (
            parts and
            len(parts) < 4 and
            all(parts) and
            all(isinstance(p, str) for p in parts)
    ))

    @property
    def object_name(self) -> str:
        return self.parts[-1]

    @property
    def schema_name(self) -> ta.Optional[str]:
        return self.parts[-2] if len(self.parts) > 1 else None

    @property
    def catalog_name(self) -> ta.Optional[str]:
        return self.parts[-3] if len(self.parts) > 2 else None

    @property
    def dotted(self) -> str:
        return '.'.join(self.parts)

    def __iter__(self) -> ta.Iterator[str]:
        return iter(self.parts)

    @classmethod
    def of_dotted(cls, dotted: str) -> 'QualifiedName':
        return cls(dotted.split('.'))

    @classmethod
    def of(cls, obj: ta.Union['QualifiedName', ta.Iterable[str]]) -> 'QualifiedName':
        if isinstance(obj, QualifiedName):
            return obj
        elif isinstance(obj, str):
            raise TypeError(obj)
        elif isinstance(obj, collections.abc.Iterable):
            return cls(list(obj))
        else:
            raise TypeError(obj)
