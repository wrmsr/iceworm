from .. import nodes as no
from ...utils import serde
from ..types import AstQuery
from ..types import Query
from ..types import StrQuery


def test_query():
    s = 'abc'
    d = serde.deserialize(s, Query)
    assert d == StrQuery('abc')
    s = serde.serialize(d, Query)
    assert s == {'str_query': {'src': 'abc'}}
    d = serde.deserialize(s, Query)
    assert d == StrQuery('abc')

    r = no.Select([
        no.ExprSelectItem(
            no.Integer(1))])
    d = AstQuery(r)
    s = serde.serialize(d, Query)
    assert s == {'ast_query': {'root': {'select': {'items': [{'expr_select_item': {'value': {'integer': {'value': 1}}}}]}}}}  # noqa
    d = serde.deserialize(s, Query)
    assert d == AstQuery(r)
