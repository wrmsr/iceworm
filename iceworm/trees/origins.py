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
    node: no.Node = dc.field(check=lambda o: isinstance(o, no.Node))


class Link(Origin, abstract=True):
    src: Origin = dc.field(check=lambda o: isinstance(o, Origin))


class Leaf(Origin, abstract=True):
    pass


class Direct(Link):
    pass


class Derive(Link):
    pass


class Export(Link):
    sym: Symbol = dc.field(check=lambda o: isinstance(o, Symbol))


class Ref(Link):
    ref: SymbolRef = dc.field(check=lambda o: isinstance(o, SymbolRef))


class Constant(Leaf):
    pass


class Scan(Leaf):
    sym: Symbol = dc.field(check=lambda o: isinstance(o, Symbol))


class OriginAnalysis:

    def __init__(self, origins: ta.Iterable[Origin]) -> None:
        super().__init__()

        self._oris = list(origins)

        self._ori_sets_by_node: ta.Mapping[no.Node, ta.AbstractSet[Origin]] = ocol.IdentityKeyDict()
        self._exports_by_sym: ta.MutableMapping[Symbol, Export] = {}
        self._exports_by_node_by_name: ta.MutableMapping[no.Node, ta.MutableMapping[str, Export]] = ocol.IdentityKeyDict()  # noqa

        for ori in self._oris:
            self._ori_sets_by_node.setdefault(ori.node, set()).add(ori)

            if isinstance(ori, Export):
                check.not_in(ori.sym, self._exports_by_sym)
                self._exports_by_sym[ori.sym] = ori

                if ori.sym.name is not None:
                    dct = self._exports_by_node_by_name.setdefault(ori.node, {})
                    check.not_in(ori.sym.name, dct)
                    dct[ori.sym.name] = ori

    @property
    def origins(self) -> ta.List[Origin]:
        return self._oris

    @property
    def ori_sets_by_node(self) -> ta.Mapping[no.Node, ta.AbstractSet[Origin]]:
        return self._ori_sets_by_node

    @property
    def exports_by_sym(self) -> ta.MutableMapping[Symbol, Export]:
        return self._exports_by_sym

    @property
    def exports_by_node_by_name(self) -> ta.MutableMapping[no.Node, ta.MutableMapping[str, Export]]:
        return self._exports_by_node_by_name


class _Analyzer(dispatch.Class):

    def __init__(self, sym_ana: SymbolAnalysis) -> None:
        super().__init__()

        self._sym_ana = check.isinstance(sym_ana, SymbolAnalysis)

        self._oris: ta.List[Origin] = []
        self._ori_sets_by_node: ta.MutableMapping[no.Node, ta.MutableSet[Origin]] = ocol.IdentityKeyDict()
        self._exports_by_sym: ta.MutableMapping[Symbol, Export] = {}

    def _add(self, ori: Origin) -> Origin:
        check.isinstance(ori, Origin)
        self._oris.append(ori)
        self._ori_sets_by_node.setdefault(ori.node, set()).add(ori)

        if isinstance(ori, Export):
            check.not_in(ori.sym, self._exports_by_sym)
            self._exports_by_sym[ori.sym] = ori

        return ori

    class Context(dc.Enum):
        pass

    class Value(Context):
        ori: Origin

    class Scope(Context):
        oris_by_sym: ta.Mapping[Symbol, Origin]

    __call__ = dispatch.property()

    def __call__(self, node: no.Node) -> Context:  # noqa
        raise TypeError(node)

    def __call__(self, node: no.AliasedRelation) -> Context:  # noqa
        src_scope = check.isinstance(self(node.relation), self.Scope)
        scope = {}
        for sym, src in src_scope.oris_by_sym.items():
            scope[sym] = self._add(Export(node, src, sym))
        return self.Scope(scope)

    def __call__(self, node: no.AllSelectItem) -> Context:  # noqa
        raise TypeError(node)

    def __call__(self, node: no.BinaryExpr) -> Context:  # noqa
        raise TypeError(node)

    def __call__(self, node: no.ExprSelectItem) -> Context:  # noqa
        src = check.isinstance(self(node.value), self.Value).ori
        return self.Value(self._add(Direct(node, src)))

    def __call__(self, node: no.QualifiedNameNode) -> Context:  # noqa
        ref = self._sym_ana.refs_by_node[node]
        sym = self._sym_ana.resolutions.syms[ref]
        src = self._exports_by_sym[sym]
        return self.Value(self._add(Ref(node, src, ref)))

    def __call__(self, node: no.Select) -> Context:  # noqa
        for rel in node.relations:
            self(rel)
        scope = {}
        for item in node.items:
            sym = check.single(self._sym_ana.sym_sets_by_node[item])
            src = check.isinstance(self(item), self.Value).ori
            scope[sym] = self._add(Export(node, src, sym))
        return self.Scope(scope)

    def __call__(self, node: no.Table) -> Context:  # noqa
        return self.Scope({
            sym: self._add(Scan(node, sym))
            for sym in self._sym_ana.sym_sets_by_node.get(node, [])
            if check.state(sym.node is node) or True
        })


def analyze(root: no.Node, sym_ana: SymbolAnalysis) -> OriginAnalysis:
    ana = _Analyzer(sym_ana)
    ana(root)
    return OriginAnalysis(ana._oris)
