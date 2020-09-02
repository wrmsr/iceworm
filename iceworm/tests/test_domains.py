from .. import datatypes as dt
from .. import domains as dom


def test_domains():
    vs = dom.EquatableValueSet.all(dt.Integer())
    assert vs.is_all
    assert not vs.is_none

    vs = dom.EquatableValueSet.none(dt.Integer())
    assert not vs.is_all
    assert vs.is_none
