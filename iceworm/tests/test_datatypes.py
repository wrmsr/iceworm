from .. import datatypes as dt
from ..utils import serde


def test_serde():
    s = serde.serialize(dt.Integer())
    d = serde.deserialize(s, dt.Datatype)
    assert d == dt.Integer()
