import typing as ta

from omnibus import check
from omnibus import dispatch

from . import nodes as no
from .. import datatypes as dt
from .. import metadata as md
from ..utils import memoized_unary
from .origins import OriginAnalysis


class TypeAnalysis:

    def __init__(self, dts_by_node: ta.Mapping[no.Node, dt.Datatype]) -> None:
        super().__init__()

        self._dts_by_node = dts_by_node


class _Analyzer(dispatch.Class):

    def __init__(self, ori_ana: OriginAnalysis, catalog: md.Catalog) -> None:
        super().__init__()

        self._ori_ana = check.isinstance(ori_ana, OriginAnalysis)
        self._catalog = check.isinstance(catalog, md.Catalog)

    _process = dispatch.property()

    __call__ = memoized_unary(_process, identity=True)

    @property
    def dts_by_node(self) -> ta.Mapping[no.Node, dt.Datatype]:
        return self.__call__.dct

    def _process(self, node: no.Node) -> dt.Datatype:  # noqa
        raise TypeError(node)

    def _process(self, node: no.Select) -> dt.Datatype:  # noqa
        return dt.Integer()


def analyze(root: no.Node, ori_ana: OriginAnalysis, catalog: md.Catalog) -> TypeAnalysis:
    ana = _Analyzer(ori_ana, catalog)
    ana(root)
    return TypeAnalysis(check.not_empty(ana.dts_by_node))
