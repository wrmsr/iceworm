import pytest

from .. import datatypes as dt
from .. import metadata as md


def test_metadata():
    t = md.Table(['t'], [md.Column('a', dt.Integer()), md.Column('b', dt.String())])
    print(t.columns_by_name)

    with pytest.raises(KeyError):
        md.Table(['t'], [md.Column('a', dt.Integer()), md.Column('a', dt.Integer())])
