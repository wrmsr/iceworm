"""
TODO:
 - parents, dom's, origins/sym resolution (shallow), types
"""
import typing as ta

from omnibus import dispatch

from . import nodes as no
from .types import QualifiedName


T = ta.TypeVar('T')


class Analyzer(dispatch.Class, ta.Generic[T]):
    analyze = dispatch.property()

    def analyze(self, node: no.Node) -> T:  # noqa
        raise TypeError(node)


def collect_name_references(node: no.Node) -> ta.Mapping[QualifiedName, ta.AbstractSet[no.Node]]:
    raise NotImplementedError
