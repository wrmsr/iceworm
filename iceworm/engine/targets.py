import typing as ta

from omnibus import dataclasses as dc


class Target(dc.Enum):

    @property
    def name(self) -> ta.Optional[str]:
        return None


class Table(Target):
    pass


class Rows(Target):
    pass


class Function(Target):
    pass
