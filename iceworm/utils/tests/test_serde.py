import datetime
import enum
import typing as ta
import uuid

from omnibus import dataclasses as dc
import pytest

from .. import serde
from ... import types as ty


class Pt(dc.Pure):
    x: int
    y: int


class Box(dc.Frozen):
    lo: Pt
    hi: Pt


class Zbox(Box):
    z: int


def test_serde():
    def rt(o, t=None):
        s = serde.serialize(o)
        d = serde.deserialize(s, t or type(o))
        assert d == o

    rt(2)
    rt(2, ta.Optional[int])
    rt(None, ta.Optional[int])

    class E(enum.Enum):
        A = 'a'
        B = 'b'

    rt(E.A)
    rt(E.B)

    rt([0, 1], ta.Sequence[int])
    rt([0, None], ta.Sequence[ta.Optional[int]])

    rt({0: 1}, ta.Mapping[int, int])
    rt({0: None}, ta.Mapping[int, ta.Optional[int]])

    rt({1, 2}, ta.AbstractSet[int])

    assert serde.deserialize([[0, 1], [2, 3]], ta.Mapping[int, int]) == {0: 1, 2: 3}
    assert serde.deserialize({0: 1, 2: 3}, ta.Mapping[int, int]) == {0: 1, 2: 3}

    with pytest.raises(serde.DeserializationException):
        serde.deserialize(None, int)

    rt(Pt(1, 2))

    rt(Box(Pt(1, 2), Pt(3, 4)))
    rt(Zbox(Pt(1, 2), Pt(3, 4), 5))

    rt(b'abc\0d')
    rt(datetime.datetime.now().date())
    rt(datetime.datetime.now().time())
    rt(datetime.datetime.now())
    rt(uuid.uuid4())


def test_code_serde():
    src = 'x: x + 2'
    lam = ty.Lambda(src)
    assert lam.fn(420) == 422

    assert serde.deserialize({'lambda': 'x: x + 10'}, ty.Lambda).fn(20) == 30

    s = serde.serialize(lam)
    assert s == {'lambda': {'src': src}}
    d = serde.deserialize(s, ty.Lambda)
    assert d.fn(422) == 424

    class Thing0(dc.Pure):
        code: ty.Code

    s = serde.serialize(Thing0(lam))
    assert s == {'thing0': {'code': {'lambda': {'src': src}}}}
    d = serde.deserialize(s, Thing0)
    assert d.code.fn(424) == 426

    class Thing1(dc.Pure):
        lam: ty.Lambda

    s = serde.serialize(Thing1(lam))
    assert s == {'thing1': {'lam': {'src': src}}}
    d = serde.deserialize(s, Thing1)
    assert d.lam.fn(426) == 428
