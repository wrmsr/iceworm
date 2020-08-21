import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import dispatch

from . import nodes as no
from .symbols import Symbol
from .symbols import SymbolAnalysis
from .symbols import SymbolRef


class Origin(dc.Enum, eq=False):
    node: no.Node


class Link(Origin, abstract=True):
    src: Origin


class Leaf(Origin, abstract=True):
    pass


class Direct(Link):
    pass


class Derive(Link):
    pass


class Ref(Link):
    ref: SymbolRef


class Constant(Leaf):
    pass


class Scan(Leaf):
    sym: Symbol


class OriginAnalysis:

    def __init__(self, origins: ta.Iterable[Origin]) -> None:
        super().__init__()

        self._oris = list(origins)

    @property
    def origins(self) -> ta.List[Origin]:
        return self._oris


class _Analyzer(dispatch.Class):

    def __init__(self, sym_ana: SymbolAnalysis) -> None:
        super().__init__()

        self._sym_ana = check.isinstance(sym_ana, SymbolAnalysis)

        self._oris: ta.List[Origin] = []
        self._ori_sets_by_node: ta.MutableMapping[no.Node, ta.MutableSet[Origin]] = ocol.IdentityKeyDict()

    def _add(self, ori: Origin) -> Origin:
        check.isinstance(ori, Origin)
        self._oris.append(ori)
        self._ori_sets_by_node.setdefault(ori.node, set()).add(ori)
        return ori

    class Context(dc.Enum):
        pass

    class Value(Context):
        value: Origin

    class Scope(Context):
        oris_by_sym: ta.Mapping[Symbol, Origin]

    __call__ = dispatch.property()

    def __call__(self, node: no.Node) -> Context:  # noqa
        raise TypeError(node)

    def __call__(self, node: no.AliasedRelation) -> Context:  # noqa
        scope = self._sym_ana.scopes_by_node[node]
        check.state(scope.node is node)
        src = check.isinstance(self(node.relation), self.Scope)
        return self.Scope({0: 0 for src_sym, src_ori in src.oris_by_sym.items()})

    def __call__(self, node: no.AllSelectItem) -> Context:  # noqa
        raise TypeError(node)

    def __call__(self, node: no.BinaryExpr) -> Context:  # noqa
        raise TypeError(node)

    def __call__(self, node: no.ExprSelectItem) -> Context:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.QualifiedNameNode) -> Context:  # noqa
        raise NotImplementedError

    def __call__(self, node: no.Select) -> Context:  # noqa
        for rel in node.relations:
            self(rel)
        for item in node.items:
            self(item)

    def __call__(self, node: no.Table) -> Context:  # noqa
        scope = self._sym_ana.scopes_by_node[node]
        check.state(scope.node is node)
        return self.Scope({sym: self._add(Scan(node, sym)) for sym in scope.syms})


def analyze(root: no.Node, sym_ana: SymbolAnalysis) -> OriginAnalysis:
    ana = _Analyzer(sym_ana)
    ana(root)
    return SymbolAnalysis(ana._oris)  # noqa
