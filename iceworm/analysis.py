import typing as ta

from . import nodes as no
from .types import QualifiedName


def collect_name_references(node: no.Node) -> ta.Mapping[QualifiedName, ta.AbstractSet[no.Node]]:
    raise NotImplementedError
