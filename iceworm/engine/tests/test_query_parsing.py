from omnibus import dataclasses as dc

from .. import elements as els
from ...trees import parsing as par
from ...trees.types import Query
from ...trees.types import StrQuery


class TestQueryElement(els.Element):
    query: Query = dc.field(coerce=Query.of)


def test_query_element():
    e = TestQueryElement('select 1')
    print(e)

    ep = els.queries.QueryParsingElementProcessor(par.parse_stmt)
    assert ep.match(els.ElementSet.of([e]))
    r = list(ep.process(els.ElementSet.of([e])))
    print(r)
    assert isinstance(e.query, StrQuery)
    assert not ep.match(els.ElementSet.of(r))
