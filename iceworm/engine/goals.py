import typing as ta

from omnibus import dataclasses as dc


class Goal(dc.Enum):

    @property
    def name(self) -> ta.Optional[str]:
        return None


class Invalidation(Goal):
    pass
