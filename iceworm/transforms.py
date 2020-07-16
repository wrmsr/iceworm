"""
TODO:
 - strip/readd date/ds clamps
  - https://docs.snowflake.com/en/user-guide/tables-clustering-keys.html
  - https://docs.snowflake.com/en/sql-reference/sql/create-table.html#syntax
 - *name disambiguator* (powered by sym res)
 - expression inversion / undo queries
 - inlining
  - upstreams
  - (mat)views
  - table funcs (laterals?)
 - jinja eval
 - parameter eval
 - lint / bugsquash
 - opto opportunities
 - window granularity
  - can you compute x days of a daily query with a single query with correct results (enforce agg bounds)
 - optimizations
  - pushdown
  - drop unused rels, cols
 - name mangling
 - limits (limit 0) pushdown
 - integrity check gen?
 - pk / ds? / 'generic?' propagation?
 - omni.matching?
"""
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
