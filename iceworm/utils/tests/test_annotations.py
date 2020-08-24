import typing as ta

from .. import annotations as an
from .. import serde


class TestAnn(an.Annotation, abstract=True):
    pass


class TestAnns(an.Annotations):

    @classmethod
    def _ann_cls(cls) -> ta.Type[TestAnn]:
        return TestAnn


class A(TestAnn):
    pass


class B(TestAnn):
    v: int


def test_annotations():
    anns = TestAnns([A(), B(1)])
    assert anns[B].v == 1

    s = serde.serialize(anns)
    d = serde.deserialize(s, TestAnns)
    assert anns == d

    anns = TestAnns({**{A: A(), B: B(1)}, B: B(2)})
    assert anns[B].v == 2

    anns2 = TestAnns({**anns.dct, B: B(3)})
    assert anns[A] is anns2[A]
    assert anns2[B].v == 3
