import typing as ta

from . import nodes as no
from .types import QualifiedName


def replace_names(node: no.Node, dct: ta.Mapping[QualifiedName, QualifiedName]) -> no.Node:
    raise NotImplementedError
