import pytest

from omnibus.serde import mapping as sm

from .. import datatypes as dt
from .. import metadata as md


def test_metadata():
    t = md.Table(['t'], [md.Column('a', dt.Integer()), md.Column('b', dt.String())])
    print(t.columns_by_name)

    with pytest.raises(KeyError):
        md.Table(['t'], [md.Column('a', dt.Integer()), md.Column('a', dt.Integer())])


def test_serde():
    t = md.Table(['t'], [md.Column('a', dt.Integer()), md.Column('b', dt.String())])
    s = sm.serialize(t, md.Object)
    d = sm.deserialize(s, md.Object)
    assert t == d
