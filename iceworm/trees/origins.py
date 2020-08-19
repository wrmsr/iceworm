import typing as ta

from omnibus import dataclasses as dc
from omnibus import dispatch

from . import nodes as no
from .symbols import Symbol


class Genesis(dc.Enum):

    @property
    def is_leaf(self) -> bool:
        return False


class Direct(Genesis):
    pass


class Constant(Genesis):

    @property
    def is_leaf(self) -> bool:
        return True


class Scan(Genesis):

    @property
    def is_leaf(self) -> bool:
        return True


class Origination(dc.Pure):
    sym: Symbol
    src: ta.Optional[Symbol]
    genesis: Genesis

    @staticmethod
    def merge(originations: ta.Iterable['Origination']) -> ta.Sequence['Origination']:
        raise NotImplementedError


class OriginationLink(dc.Pure, eq=False):
    sink: Origination
    next: ta.AbstractSet['OriginationLink']


class OriginChainAnalysis:

    def should_split(self, ori: Origination) -> bool:
        raise NotImplementedError

    @property
    def first_oris(self) -> ta.Set[Origination]:
        raise NotImplementedError

    @property
    def first_ori_sets_by_sink(self) -> ta.Mapping[Symbol, ta.Set[Origination]]:
        raise NotImplementedError

    @property
    def first_ori_sets_by_ori(self) -> ta.Mapping[Origination, ta.Set[Origination]]:
        raise NotImplementedError

    @property
    def ori_link_sets_by_sink(self) -> ta.Mapping[Symbol, ta.Set[OriginationLink]]:
        raise NotImplementedError

    @property
    def sink_sets_by_first_source(self) -> ta.Mapping[Symbol, ta.Set[Symbol]]:
        raise NotImplementedError

    def yield_paths(self, sink: Symbol, source: Symbol) -> ta.Generator[ta.Sequence[OriginationLink], None, None]:
        raise NotImplementedError


class OriginAnalysis:

    def __init__(
            self,
            originations: ta.List[Origination],
            toposort_indices_by_node: ta.Mapping[no.Node, int],
    ) -> None:
        super().__init__()

    @property
    def originations(self) -> ta.List[Origination]:
        raise NotImplementedError

    @property
    def origination_sets_by_sink(self) -> ta.Mapping[Symbol, ta.Set[Origination]]:
        raise NotImplementedError

    @property
    def origination_sets_by_source(self) -> ta.Mapping[Symbol, ta.Set[Origination]]:
        raise NotImplementedError

    @property
    def origination_sets_by_sink_node_by_sink_sym(self) -> ta.Mapping[no.Node, ta.Mapping[Symbol, ta.Set[Origination]]]:  # noqa
        raise NotImplementedError

    @property
    def origination_sets_by_source_node_by_source_sym(self) -> ta.Mapping[no.Node, ta.Mapping[Symbol, ta.Set[Origination]]]:  # noqa
        raise NotImplementedError

    def _build_chain_analysis(self, split_predicate: ta.Callable[[Origination], bool]) -> OriginChainAnalysis:
        raise NotImplementedError

    @property
    def leaf_chain_analysis(self) -> OriginChainAnalysis:
        raise NotImplementedError


class _Analyzer(dispatch.Class):

    def __init__(self) -> None:
        super().__init__()

    __call__ = dispatch.property()


def analyze(root: no.Node) -> OriginAnalysis:
    _Analyzer()(root)
    raise NotImplementedError
