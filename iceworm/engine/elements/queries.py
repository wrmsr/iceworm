import typing as ta
import weakref

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc

from ...trees import analysis as ana
from ...trees import nodes as no
from ...trees.types import AstQuery
from ...trees.types import Query
from ...trees.types import StrQuery
from .base import Element
from .base import Origin
from .collections import ElementSet
from .processing import ElementProcessor


_QUERY_FIELDS_CACHE = weakref.WeakKeyDictionary()


def _get_query_fields(cls: type) -> ta.AbstractSet[str]:
    try:
        return _QUERY_FIELDS_CACHE[cls]
    except KeyError:
        check.isinstance(cls, type)
        s = _QUERY_FIELDS_CACHE[cls] = frozenset(f.name for f in dc.fields(cls) if f.type is Query)
        return s


class QueryParsingElementProcessor(ElementProcessor):

    def __init__(self, parser: ta.Callable[[str], no.Node]) -> None:
        super().__init__()

        self._parser = check.callable(parser)

    def match(self, elements: ElementSet) -> ta.Iterable[Element]:
        return [
            e
            for e in elements
            for fs in [_get_query_fields(type(e))]
            if fs
            and any(not isinstance(getattr(e, f), AstQuery) for f in fs)
        ]

    def process(self, elements: ElementSet) -> ta.Iterable[Element]:
        ret = []
        for e in elements:
            fs = _get_query_fields(type(e))
            if fs and any(not isinstance(getattr(e, f), AstQuery) for f in fs):
                kw = {
                    f: AstQuery(self._parser(check.isinstance(q, StrQuery).src))
                    for f in fs
                    for q in [getattr(e, f)]
                    if not isinstance(q, AstQuery)
                }
                new = dc.replace(e, **kw, meta={Origin: Origin(e)})
                ret.append(new)
            else:
                ret.append(e)
        return ret


class QueryBasicAnalyses(dc.Pure):
    basics_by_query: ta.Mapping[no.Node, ana.BasicAnalysis]

    def __getitem__(self, obj: ta.Union[AstQuery, no.Node]):
        if isinstance(obj, AstQuery):
            root = obj.root
        elif isinstance(obj, no.Node):
            root = obj
        else:
            raise TypeError(obj)
        return self.basics_by_query[root]


class QueryBasicAnalysisElementProcessor(ElementProcessor):

    @classmethod
    def dependencies(cls) -> ta.Iterable[ta.Type['ElementProcessor']]:
        return {*super().dependencies(), QueryParsingElementProcessor}

    def match(self, elements: ElementSet) -> ta.Iterable[Element]:
        return [
            e
            for e in elements
            if _get_query_fields(type(e)) and QueryBasicAnalyses not in e.meta
        ]

    def process(self, elements: ElementSet) -> ta.Iterable[Element]:
        ret = []
        for e in elements:
            fs = _get_query_fields(type(e))
            if fs and QueryBasicAnalyses not in e.meta:
                ret.append(dc.replace(e, meta={
                    **e.meta,
                    Origin: Origin(e),
                    QueryBasicAnalyses: QueryBasicAnalyses(ocol.IdentityKeyDict(
                        (root, ana.basic(root))
                        for f in fs
                        for q in [getattr(e, f)]
                        for root in [check.isinstance(q, AstQuery).root]
                    ))
                }))
            else:
                ret.append(e)
        return ret


def get_basic(ele: Element, obj: ta.Any) -> ana.BasicAnalysis:
    check.isinstance(ele, Element)
    return ele.meta[QueryBasicAnalyses][obj]
