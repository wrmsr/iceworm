import pytest

from .. import datatypes as dt
from .. import metadata as md
from ...utils import serde


def test_metadata():
    t = md.Table(['t'], [md.Column('a', dt.Integer()), md.Column('b', dt.String())])
    print(t.columns_by_name)

    with pytest.raises(KeyError):
        md.Table(['t'], [md.Column('a', dt.Integer()), md.Column('a', dt.Integer())])


def test_serde():
    t = md.Table(['t'], [md.Column('a', dt.Integer()), md.Column('b', dt.String())])
    s = serde.serialize(t, md.Object)
    d = serde.deserialize(s, md.Object)
    assert t == d
