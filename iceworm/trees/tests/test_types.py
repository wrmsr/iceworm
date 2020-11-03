from omnibus.serde import mapping as sm

from .. import nodes as no
from ..types import AstQuery
from ..types import Query
from ..types import StrQuery


def test_query():
    s = 'abc'
    d = sm.deserialize(s, Query)
    assert d == StrQuery('abc')
    s = sm.serialize(d, Query)
    assert s == {'str_query': {'src': 'abc'}}
    d = sm.deserialize(s, Query)
    assert d == StrQuery('abc')

    r = no.Select([
        no.ExprSelectItem(
            no.Integer(1))])
    d = AstQuery(r)
    s = sm.serialize(d, Query)
    assert s == {'ast_query': {'root': {'select': {'items': [{'expr_select_item': {'value': {'integer': {'value': 1}}}}]}}}}  # noqa
    d = sm.deserialize(s, Query)
    assert d == AstQuery(r)
