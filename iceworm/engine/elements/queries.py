import typing as ta
import weakref

from omnibus import check
from omnibus import dataclasses as dc

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

    def processes(self, elements: ElementSet) -> ta.Iterable[Element]:
        return {
            e
            for e in elements
            for fs in [_get_query_fields(type(e))]
            if fs
            and any(not isinstance(getattr(e, f), AstQuery) for f in fs)
        }

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
                new = dc.replace(e, **kw, anns={**e.anns, Origin: Origin(e)})
                ret.append(new)
            else:
                ret.append(e)
        return ret
