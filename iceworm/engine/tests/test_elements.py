import pytest

from .. import elements as els
from .. import targets as tars
from ...utils import serde


def test_refs():
    r = els.Ref[tars.Table](['hi'])
    assert repr(r) == "Ref[Table](['hi'])"

    rs = serde.serialize(r)
    assert rs == ('hi',)
    rd = serde.deserialize(rs, els.Ref[tars.Table])
    assert rd == r

    l = els.Ref[tars.Table](['x'])
    r = els.Ref[tars.Function](['x'])
    assert l != r

    with pytest.raises(TypeError):
        els.Ref[int]  # noqa
