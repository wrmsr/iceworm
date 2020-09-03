import dataclasses as dc
import typing as ta

from ..utils import dc_only


@dc.dataclass(frozen=True)
class Pt:
    x: ta.Optional[int] = None
    y: ta.Optional[int] = None
    xs: ta.Optional[ta.Sequence[int]] = None
    ys: ta.Optional[ta.Sequence[int]] = None


def test_dc_only():
    assert dc_only(Pt(), [])

    assert dc_only(Pt(x=0), ['x'])
    assert dc_only(Pt(x=0), ['x'], all=True)

    assert not dc_only(Pt(x=0), [])
    assert not dc_only(Pt(x=0, y=1), ['x'])

    assert not dc_only(Pt(x=0, y=1), ['x'])
    assert dc_only(Pt(x=0, y=1), ['x', 'y'])
    assert dc_only(Pt(x=0, y=1), ['x', 'y'], all=True)
    assert dc_only(Pt(x=0), ['x', 'y'])
    assert not dc_only(Pt(x=0), ['x', 'y'], all=True)

    assert dc_only(Pt(xs=[]), ['xs'])
    assert not dc_only(Pt(xs=[]), ['xs'], all=True)
