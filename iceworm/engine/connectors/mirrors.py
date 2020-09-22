"""
TODO:
 - caching / offline
"""
import abc
import typing as ta

from omnibus import lang

from ...types import QualifiedName
from ... import metadata as md


class Mirror(lang.Abstract):

    @abc.abstractmethod
    def reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        raise NotImplementedError
