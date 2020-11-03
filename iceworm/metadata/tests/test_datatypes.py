from omnibus.serde import mapping as sm

from .. import datatypes as dt


def test_serde():
    s = sm.serialize(dt.Integer(), dt.Datatype)
    assert s == {'number': {}}
    d = sm.deserialize(s, dt.Datatype)
    assert d == dt.Integer()

    assert isinstance(sm.deserialize('number', dt.Datatype), dt.Number)
    # assert isinstance(sm.deserialize('integer', dt.Number), dt.Number)  # FIXME: ? just dep a dt.Datatype and check if varchar and such?  # noqa
