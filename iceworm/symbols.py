"""
TODO:
 - all node? just clone tok
 - origins/sym resolution (shallow)
 - types
  - including inferred jinja
   - 'ANY' type?
"""
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import dispatch

from . import nodes as no
from .types import QualifiedName


class Symbol(dc.Pure, eq=False):
    name: ta.Optional[str]
    node: no.Node
    origin: ta.Optional['Symbol']
    scope: 'SymbolScope'


class SymbolRef(dc.Pure, eq=False):
    qualified_name: QualifiedName
    node: no.Node
    binding: ta.Optional['Symbol']
    scope: 'SymbolScope'


class SymbolScope(dc.Data, eq=False, final=True):
    node: no.Node
    parent: ta.Optional['SymbolScope'] = None
    name: ta.Optional[str] = dc.field(default=None, kwonly=True)

    def __post_init__(self) -> None:
        self._enclosed_nodes: ta.MutableSet[no.Node] = ocol.IdentitySet()
        self._children: ta.MutableSet['SymbolScope'] = set()
        self._symbols: ta.MutableSet['Symbol'] = set()
        self._refs: ta.MutableSet['SymbolRef'] = set()

        self._enclosed_nodes.add(self.node)

    @property
    def children(self) -> ta.AbstractSet['SymbolScope']:
        return self._children

    @property
    def symbols(self) -> ta.AbstractSet['Symbol']:
        return self._symbols

    @property
    def refs(self) -> ta.AbstractSet['SymbolRef']:
        return self._refs


class SymbolResolutions(dc.Pure, eq=False):
    symbols: ta.Mapping[SymbolRef, Symbol]
    refs: ta.Mapping[Symbol, ta.AbstractSet[SymbolRef]]


class SymbolAnalysis:

    def __init__(self, root: SymbolScope) -> None:
        super().__init__()

        self._root = check.isinstance(root, SymbolScope)

        self._scopes: ta.MutableSet[SymbolScope] = set()
        self._scopes_by_node: ta.MutableMapping[no.Node, SymbolScope] = {}
        self._symbol_sets_by_node: ta.MutableMapping[no.Node, ta.MutableSet[Symbol]] = {}
        self._refs_by_node: ta.MutableMapping[no.Node, SymbolRef] = {}

    def root(self) -> SymbolScope:
        return self._root

    def scopes(self) -> ta.AbstractSet[SymbolScope]:
        return self._scopes

    def scopes_by_node(self) -> ta.Mapping[no.Node, SymbolScope]:
        return self._scopes_by_node

    def symbol_sets_by_node(self) -> ta.Mapping[no.Node, ta.AbstractSet[Symbol]]:
        return self._symbol_sets_by_node

    def refs_by_node(self) -> ta.Mapping[no.Node, SymbolRef]:
        return self._refs_by_node


class _Analyzer(dispatch.Class):
    __call__ = dispatch.property()

    def __call__(self, node: no.Node, scope: SymbolScope) -> ta.Optional[SymbolScope]:  # noqa
        if scope is not None:
            scope._enclosed_nodes.add(node)
        return None
