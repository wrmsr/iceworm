import typing as ta

from omnibus import dataclasses as dc
from omnibus import dispatch
from omnibus import lang

from . import nodes as no
from .types import QualifiedName


NodeT = ta.TypeVar('NodeT', bound=no.Node)


class Transformer(dispatch.Class, lang.Abstract, ta.Generic[NodeT]):
    __call__ = dispatch.property()

    def __call__(self, node: no.Node) -> NodeT:  # noqa
        return node.map(self)


@dc.dataclass(frozen=True)
class ReplaceNamesTransformer(Transformer):
    dct: ta.Mapping[QualifiedName, QualifiedName]

    def __call__(self, node: no.QualifiedNameNode) -> no.QualifiedNameNode:  # noqa
        try:
            repl = self.dct[node.name]
        except KeyError:
            return node
        else:
            return no.QualifiedNameNode.of(repl)


def replace_names(node: no.Node, dct: ta.Mapping[QualifiedName, QualifiedName]) -> no.Node:
    return ReplaceNamesTransformer(dct)(node)
