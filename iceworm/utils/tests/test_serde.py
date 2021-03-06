import datetime
import enum
import typing as ta
import uuid

from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus.serde import mapping as sm
import pytest

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
        s = sm.serialize(o, t)
        d = sm.deserialize(s, t or type(o))
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

    assert sm.deserialize([[0, 1], [2, 3]], ta.Mapping[int, int]) == {0: 1, 2: 3}
    assert sm.deserialize({0: 1, 2: 3}, ta.Mapping[int, int]) == {0: 1, 2: 3}

    rt(Pt(1, 2))

    rt(Box(Pt(1, 2), Pt(3, 4)))
    rt(Zbox(Pt(1, 2), Pt(3, 4), 5))

    rt(b'abc\0d')
    rt(datetime.datetime.now().date())
    rt(datetime.datetime.now().time())
    rt(datetime.datetime.now())
    rt(uuid.uuid4())

    sm.serialize(ocol.FrozenDict({1: 2, 3: 4}), ta.Mapping[int, int])


def test_reraise():
    with pytest.raises(sm.DeserializationException):
        sm.deserialize(None, int)


def test_code_serde():
    src = 'x: x + 2'
    lam = ty.Lambda(src)
    assert lam.fn(420) == 422

    assert sm.deserialize('x: x + 10', ty.Lambda).fn(20) == 30
    assert sm.deserialize({'lambda': 'x: x + 10'}, ty.Code).fn(20) == 30

    s = sm.serialize(lam, ty.Code)
    assert s == {'lambda': {'src': src}}
    d = sm.deserialize(s, ty.Code)
    assert d.fn(422) == 424

    class Thing0(dc.Pure):
        code: ty.Code

    s = sm.serialize(Thing0(lam))
    assert s == {'code': {'lambda': {'src': src}}}
    d = sm.deserialize(s, Thing0)
    assert d.code.fn(424) == 426

    class Thing1(dc.Pure):
        lam: ty.Lambda

    s = sm.serialize(Thing1(lam))
    assert s == {'lam': {'src': src}}
    d = sm.deserialize(s, Thing1)
    assert d.lam.fn(426) == 428


class A(dc.Pure):
    a: ta.Optional['A'] = None


def test_rec():
    sd = sm.serde(A)

    a = A(A())

    s = sd.serialize(a)
    d = sd.deserialize(s)

    assert d == a
