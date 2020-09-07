import pytest

from .. import elements as els
from .. import targets as tars
from ...utils import serde


def test_refs():
    r = els.Ref[tars.Table]('hi')
    assert isinstance(r, els.Ref)
    assert isinstance(r, els.Ref[tars.Table])  # noqa
    assert not isinstance(r, els.Ref[tars.Function])  # noqa
    assert repr(r) == "Ref[Table]('hi')"

    with pytest.raises(TypeError):
        r == 'hi'  # noqa

    rs = serde.serialize(r)
    assert rs == 'hi'
    rd = serde.deserialize(rs, els.Ref[tars.Table])
    assert rd == r

    rx = els.Ref[tars.Table]('x')
    ry = els.Ref[tars.Table]('y')
    assert rx != ry
    assert rx < ry
    assert ry > rx

    fx = els.Ref[tars.Function]('x')
    with pytest.raises(TypeError):
        assert rx != fx
    with pytest.raises(TypeError):
        assert rx < fx

    tx = tars.Table('x')
    ty = tars.Table('y')
    assert rx == tx
    assert rx != ty
    with pytest.raises(TypeError):
        rx < tx  # noqa
    fx = tars.Function('x')
    with pytest.raises(TypeError):
        rx == fx  # noqa

    with pytest.raises(TypeError):
        els.Ref[int]  # noqa
