import typing as ta

from omnibus import dataclasses as dc


class QualifiedName(dc.Pure):
    parts: ta.Sequence[str]

    def __iter__(self) -> ta.Iterator[str]:
        return iter(self.parts)

    @classmethod
    def of_dotted(cls, dotted: str) -> 'QualifiedName':
        return cls(dotted.split('.'))
