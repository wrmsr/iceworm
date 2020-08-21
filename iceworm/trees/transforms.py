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
import collections  # noqa
import typing as ta

from omnibus import check
from omnibus import code as ocode
from omnibus import dataclasses as dc
from omnibus import dispatch
from omnibus import lang

from . import analysis as ana  # noqa
from . import nodes as no
from .. import metadata as md
from ..types import QualifiedName


class Origin(lang.Marker):
    pass


class Transformer(dispatch.Class, lang.Abstract):
    __call__ = dispatch.property()

    def __call__(self, node: no.Node, **kwargs) -> no.Node:  # noqa
        res = node.map(self, **kwargs)
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


class AliasRelationsTransformer(Transformer):

    def __init__(self, root: no.Node) -> None:
        super().__init__()

        self._root = check.isinstance(root, no.Node)

        self._basic = ana.basic(root)

        rel_names = set()
        for ar in self._basic.get_node_type_set(no.AliasedRelation):
            rel_names.add(ar.alias.name)
        for tbl in self._basic.get_node_type_set(no.Table):
            rel_names.add(tbl.name.parts[-1].name)
        self._name_gen = ocode.name_generator(unavailable_names=rel_names)

    def __call__(self, node: no.AliasedRelation) -> no.Node:  # noqa
        return super().__call__(node)

    def __call__(self, node: no.Relation) -> no.Node:  # noqa
        parent = self._basic.parents_by_node[node]
        node = super().__call__(node)
        if not isinstance(parent, no.AliasedRelation):
            if isinstance(node, no.Table):
                name = node.name.parts[-1].name  # FIXME: lame
            else:
                name = self._name_gen()
            node = no.AliasedRelation(
                node,
                no.Identifier(name))
        return node


class LabelSelectItemsTransformer(Transformer):

    def __init__(self, root: no.Node) -> None:
        super().__init__()

        self._root = check.isinstance(root, no.Node)

        self._basic = ana.basic(root)

        labels = set()
        for item in self._basic.get_node_type_set(no.ExprSelectItem):
            if item.label is not None:
                labels.add(item.label.name)
        self._name_gen = ocode.name_generator(unavailable_names=labels)

    def __call__(self, node: no.ExprSelectItem) -> no.Node:  # noqa
        return super().__call__(
            node,
            label=self(node.label) if node.label is not None else no.Identifier(self._name_gen()),
        )


class ExpandSelectsTransformer(Transformer):

    def __init__(self, root: no.Node, catalog: md.Catalog) -> None:
        super().__init__()

        self._root = check.isinstance(root, no.Node)
        self._catalog = check.isinstance(catalog, md.Catalog)

        self._basic = ana.basic(root)

        labels = set()
        for item in self._basic.get_node_type_set(no.ExprSelectItem):
            labels.add(check.not_none(item.label).name)
        self._name_gen = ocode.name_generator(unavailable_names=labels)

    def __call__(self, node: no.Select) -> no.Node:  # noqa
        sup = super().__call__  # FIXME: wut
        rels = [check.isinstance(sup(r), no.Relation) for r in node.relations]

        items = []
        for item in node.items:
            if isinstance(item, no.AllSelectItem):
                def rec(rel: no.Relation, alias: ta.Optional[str] = None) -> None:
                    if isinstance(rel, no.Table):
                        tbl = self._catalog.tables_by_name[rel.name.name]
                        for col in tbl.columns:
                            items.append(
                                no.ExprSelectItem(
                                    no.QualifiedNameNode.of([alias or tbl.name, col.name]),
                                    no.Identifier(self._name_gen())))

                    elif isinstance(rel, no.AliasedRelation):
                        check.none(alias)
                        rec(rel.relation, rel.alias.name)

                    else:
                        raise TypeError(rel)

                for rel in rels:
                    rec(rel)

            elif isinstance(item, no.IdentifierAllSelectItem):
                raise NotImplementedError

            elif isinstance(item, no.ExprSelectItem):
                items.append(self(item))

            else:
                raise TypeError(item)

        return super().__call__(node, items=items, relations=rels)
