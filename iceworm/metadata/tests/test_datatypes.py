from .. import datatypes as dt
from ...utils import serde


def test_serde():
    s = serde.serialize(dt.Integer(), dt.Datatype)
    assert s == {'number': {}}
    d = serde.deserialize(s, dt.Datatype)
    assert d == dt.Integer()

    assert isinstance(serde.deserialize('number', dt.Datatype), dt.Number)
    # assert isinstance(serde.deserialize('integer', dt.Number), dt.Number)  # FIXME: ? just dep a dt.Datatype and check if varchar and such?  # noqa
