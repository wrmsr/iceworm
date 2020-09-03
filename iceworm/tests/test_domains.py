from .. import datatypes as dt
from .. import domains as dom


def test_domains():
    vs = dom.EquatableValueSet.all(dt.Integer())
    assert vs.is_all
    assert not vs.is_none

    vs = dom.EquatableValueSet.none(dt.Integer())
    assert not vs.is_all
    assert vs.is_none

    vs = dom.SortedRangeSet.none(dt.Integer())
    print(vs)

    rngs = [
        dom.Range(dom.Marker(dt.Integer(), 10, dom.Bound.EXACTLY), dom.Marker(dt.Integer(), 20, dom.Bound.BELOW)),
        dom.Range(dom.Marker(dt.Integer(), 30, dom.Bound.EXACTLY), dom.Marker(dt.Integer(), 40, dom.Bound.BELOW)),
    ]
    vs = dom.SortedRangeSet(dt.Integer(), rngs)
    print(vs)
