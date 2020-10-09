from .. import annotations as an
from ... import serde


class TestAnn(an.Annotation, abstract=True):
    pass


class TestAnns(an.Annotations[TestAnn]):
    pass


class A(TestAnn):
    pass


class B(TestAnn):
    v: int


def test_annotations():
    anns = TestAnns()
    s = serde.serialize(anns)
    assert s == {'test_anns': {}}
    d = serde.deserialize(s, TestAnns)
    assert anns == d

    anns = TestAnns([A(), B(1)])
    assert anns[B].v == 1

    s = serde.serialize(anns)
    d = serde.deserialize(s, TestAnns)
    assert anns == d

    anns = TestAnns({**{A: A(), B: B(1)}, B: B(2)})
    assert anns[B].v == 2

    anns2 = TestAnns({**anns, B: B(3)})
    assert anns[A] is anns2[A]
    assert anns2[B].v == 3

    anns2 = TestAnns(anns)
    assert anns == anns2
