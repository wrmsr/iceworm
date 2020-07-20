"""
TODO:
 - strip/readd date/ds clamps
  - https://docs.snowflake.com/en/user-guide/tables-clustering-keys.html
  - https://docs.snowflake.com/en/sql-reference/sql/create-table.html#syntax
 - *name disambiguator* (powered by sym res)
 - expression inversion / undo queries
 - selectallexpansion
 - symbol resolution / namification
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

from . import metadata as md
from . import nodes as no
from .types import QualifiedName


class Origin(lang.Marker):
    pass


class Transformer(dispatch.Class, lang.Abstract):
    __call__ = dispatch.property()

    def __call__(self, node: no.Node) -> no.Node:  # noqa
        res = node.map(self)
        return dc.replace(res, meta={**res.meta, Origin: node})


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


class ExpandSelectsTransformer(Transformer):

    def __init__(self, catalog: md.Catalog) -> None:
        super().__init__()

        self._catalog = catalog

    def __call__(self, node: no.Select) -> no.Node:
        return node
