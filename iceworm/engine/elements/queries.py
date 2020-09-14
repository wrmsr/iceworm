import typing as ta
import weakref

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties

from ...trees import analysis as ana
from ...trees import nodes as no
from ...trees.types import AstQuery
from ...trees.types import Query
from ...trees.types import StrQuery
from .base import Element
from .base import Origin
from .collections import Analysis
from .collections import ElementMap
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


class QueryBasics(dc.Pure):
    by_query: ta.Mapping[no.Node, ana.BasicAnalysis]

    def __getitem__(self, obj: ta.Union[Query, no.Node]):
        if isinstance(obj, AstQuery):
            root = obj.root
        elif isinstance(obj, no.Node):
            root = obj
        else:
            raise TypeError(obj)
        return self.by_query[root]


class QueryBasicAnalysis(Analysis):

    @classmethod
    def cls_dependencies(cls) -> ta.Iterable[ta.Type[ElementProcessor]]:
        return {*super().cls_dependencies(), QueryParsingElementProcessor}

    @properties.cached
    @property
    def by_element(self) -> ta.Mapping[Element, QueryBasics]:
        return ElementMap(
            (e, QueryBasics(ocol.IdentityKeyDict(
                (root, ana.basic(root))
                for f in qf
                for q in [getattr(e, f)]
                for root in [check.isinstance(q, AstQuery).root]
            )))
            for e in self.elements
            for qf in [_get_query_fields(type(e))]
            if qf
        )

    def __getitem__(self, ele: Element) -> QueryBasics:
        return self.by_element[ele]
