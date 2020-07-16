"""
TODO:
 - dc.PrivateVar or per-field frozen
 - all node? just clone tok
 - origins/sym resolution (shallow)
 - types
  - including inferred jinja
   - 'ANY' type?
"""
import collections
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

        if self.parent is not None:
            self.parent._children.add(self)
        self._enclosed_nodes.add(self.node)

    @property
    def enclosed_nodes(self) -> ta.AbstractSet[no.Node]:
        return self._enclosed_nodes

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
        self._scopes_by_node: ta.MutableMapping[no.Node, SymbolScope] = ocol.IdentityKeyDict()
        self._symbol_sets_by_node: ta.MutableMapping[no.Node, ta.MutableSet[Symbol]] = ocol.IdentityKeyDict()
        self._refs_by_node: ta.MutableMapping[no.Node, SymbolRef] = ocol.IdentityKeyDict()

        seen: ta.MutableSet[SymbolScope] = set()
        queue: ta.Deque[SymbolScope] = collections.deque()
        queue.append(root)
        seen.add(root)

        while queue:
            cur = queue.pop()
            for n in cur.enclosed_nodes:
                check.not_in(n, self._scopes_by_node)
                self._scopes_by_node[n] = cur
            for s in cur.symbols:
                self._symbol_sets_by_node.setdefault(s.node, set()).add(s)
            for r in cur.refs:
                check.not_in(r.node, self._refs_by_node)
                self._refs_by_node[r.node] = r
            for c in cur.children:
                check.not_in(c, seen)
                queue.append(c)
                seen.add(c)

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

    def __call__(self, node: no.Node, scope: ta.Optional[SymbolScope]) -> ta.Optional[SymbolScope]:  # noqa
        if scope is not None:
            scope._enclosed_nodes.add(node)
        for child in node.children:
            self(child, scope)
        return None

    def __call__(self, node: no.Select, scope: ta.Optional[SymbolScope]) -> ta.Optional[SymbolScope]:  # noqa
        scope = SymbolScope(node, scope)
        for child in node.children:
            self(child, scope)
        return scope


def analyze(root: no.Node) -> SymbolAnalysis:
    scope = _Analyzer()(root, None)
    return SymbolAnalysis(scope)
