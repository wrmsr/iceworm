"""
** *NOT* nested **
"""
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc

from .. import metadata as md_
from ..types import QualifiedName


T = ta.TypeVar('T"')


class Target(dc.Enum):

    @property
    def name(self) -> ta.Optional[QualifiedName]:
        return None


class Table(Target):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
    md: ta.Optional[md_.Table] = dc.field(None, check=lambda o: o is None or isinstance(o, md_.Table))


class Rows(Target):
    table: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))

    name: ta.Optional[QualifiedName] = dc.field(None, coerce=QualifiedName.of_optional, kwonly=True)


class Function(Target):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)


class TargetSet:

    def __init__(self, targets: ta.Iterable[Target]) -> None:
        super().__init__()

        self._targets = [check.isinstance(e, Target) for e in targets]

        self._target_set = ocol.IdentitySet(self._targets)
        by_name = ocol.IdentityKeyDict()
        for target in self._targets:
            if target.name is not None:
                check.not_in(target.name, by_name)
                by_name[target.name] = target
        self._targets_by_name: ta.Mapping[QualifiedName, Target] = by_name
        self._node_sets_by_type: ta.Dict[type, ta.AbstractSet[Target]] = {}

    @classmethod
    def of(cls, it: ta.Iterable[Target]) -> 'TargetSet':
        if isinstance(it, cls):
            return it
        else:
            return cls(it)

    def get_target_type_set(self, ty: ta.Type[T]) -> ta.AbstractSet[T]:
        try:
            return self._node_sets_by_type[ty]
        except KeyError:
            ret = self._node_sets_by_type[ty] = ocol.IdentitySet(n for n in self._targets if isinstance(n, ty))
            return ret

    def __iter__(self) -> ta.Iterator[Target]:
        return iter(self._targets)

    def __contains__(self, key: ta.Union[QualifiedName, Target, type]) -> bool:
        if isinstance(key, QualifiedName):
            return key in self._targets_by_name
        elif isinstance(key, Target):
            return key in self._target_set
        elif isinstance(key, type):
            return bool(self.get_target_type_set(key))
        else:
            raise TypeError(key)

    def __getitem__(self, name: QualifiedName) -> Target:
        return self._targets_by_name[check.isinstance(name, QualifiedName)]
