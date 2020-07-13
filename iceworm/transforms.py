import typing as ta

from omnibus import dispatch
from omnibus import lang

from . import nodes as no
from .types import QualifiedName


NodeT = ta.TypeVar('NodeT', bound=no.Node)


class Transformer(dispatch.Class, lang.Abstract, ta.Generic[NodeT]):
    __call__ = dispatch.property()

    def __call__(self, node: no.Node) -> NodeT:  # noqa
        return node.map(self)


class ReplaceNamesTransform(Transformer):

    def __init__(self, dct: ta.Mapping[QualifiedName, QualifiedName]) -> None:
        super().__init__()
        self._dct = dct

    def __call__(self, node: no.QualifiedNameNode) -> no.QualifiedNameNode:  # noqa
        raise NotImplementedError


def replace_names(node: no.Node, dct: ta.Mapping[QualifiedName, QualifiedName]) -> no.Node:
    return ReplaceNamesTransform(dct)(node)
