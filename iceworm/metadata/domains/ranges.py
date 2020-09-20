import enum
import functools
import typing as ta

from omnibus import check
from omnibus import defs

from .. import datatypes as dt


T = ta.TypeVar('T')
U = ta.TypeVar('U')


class Bound(enum.Enum):
    BELOW = 1
    EXACTLY = 2
    ABOVE = 3


@functools.total_ordering
class Marker(ta.Generic[T]):

    def __init__(self, type: dt.Datatype, value: ta.Optional[T], bound: Bound) -> None:
        super().__init__()

        self._type = check.isinstance(type, dt.Datatype)
        self._value = value
        self._bound = check.isinstance(bound, Bound)
        check.state(self._type.is_sortable)
        check.state(not (value is None and bound == Bound.EXACTLY))

    defs.basic('type', 'value', 'bound')

    @classmethod
    def upper_unbounded(cls, type: dt.Datatype) -> 'Marker[T]':
        return cls(type, None, Bound.BELOW)

    @classmethod
    def lower_unbounded(cls, type: dt.Datatype) -> 'Marker[T]':
        return cls(type, None, Bound.ABOVE)

    @classmethod
    def above(cls, type: dt.Datatype, value: T) -> 'Marker[T]':
        return cls(type, value, Bound.ABOVE)

    @classmethod
    def exactly(cls, type: dt.Datatype, value: T) -> 'Marker[T]':
        return cls(type, value, Bound.EXACTLY)

    @classmethod
    def below(cls, type: dt.Datatype, value: T) -> 'Marker[T]':
        return cls(type, value, Bound.BELOW)

    @classmethod
    def min(cls, marker1: 'Marker', marker2: 'Marker') -> 'Marker[T]':
        return marker1 if marker1 <= marker2 else marker2

    @classmethod
    def max(cls, marker1: 'Marker', marker2: 'Marker') -> 'Marker[T]':
        return marker1 if marker1 >= marker2 else marker2

    @property
    def type(self) -> dt.Datatype:
        return self._type

    @property
    def value(self) -> ta.Optional[T]:
        return self._value

    @property
    def bound(self) -> Bound:
        return self._bound

    def __lt__(self, other: 'Marker[T]') -> bool:
        if type(self) is not type(other):
            return NotImplemented
        else:
            return \
                self._value < other._value and \
                self._bound.value < other._bound.value

    def __str__(self) -> str:
        prefix = '<' if self._bound == Bound.BELOW else '>' if self._bound == Bound.ABOVE else ''
        value = '...' if self._value is None else str(self._value)
        return prefix + value

    @property
    def is_none(self) -> bool:
        return self._value is None and self._bound == Bound.EXACTLY

    @property
    def is_all(self) -> bool:
        return self._value is None and self._bound != Bound.EXACTLY

    def _check_compat(self, other: 'Marker') -> 'Marker':
        check.isinstance(other, Marker)
        if other._type != self._type:
            raise TypeError(other)
        return other

    @property
    def is_upper_unbounded(self) -> bool:
        return self._value is None and self._bound == Bound.BELOW

    @property
    def is_lower_unbounded(self) -> bool:
        return self._value is None and self._bound == Bound.ABOVE

    def is_adjacent(self, other: 'Marker') -> bool:
        self._check_compat(other)
        if self.is_upper_unbounded or self.is_lower_unbounded or other.is_upper_unbounded or other.is_lower_unbounded:
            return False
        if self._value != other._value:
            return False
        return (
                (self._bound == Bound.EXACTLY and other._bound != Bound.EXACTLY) or
                (self._bound != Bound.EXACTLY and other._bound == Bound.EXACTLY)
        )


class Range(ta.Generic[T]):

    UNBOUNDED: 'Range' = None
    EMPTY: 'Range' = None

    def __init__(self, low: Marker[T], high: Marker[T]) -> None:
        super().__init__()

        self._low = check.isinstance(low, Marker)
        self._high = check.isinstance(high, Marker)

        check.state(low.type == high.type)
        if low.is_none or high.is_none:
            if not (low.is_none and high.is_none):
                raise ValueError(f'Lower {low!r} and high {high!r} must both be none')
        if low.bound == Bound.BELOW:
            raise ValueError(f'Present low {low!r} should never be BELOW')
        if high.bound == Bound.ABOVE:
            raise ValueError(f'Present high {high!r} should never be ABOVE')
        if low.value is not None and high.value is not None and low.value > high.value:
            raise ValueError(f'Lower {low!r} > high {high!r}')

    defs.basic('low', 'high')

    @classmethod
    def all(cls, type: dt.Datatype) -> 'Range[T]':
        return cls(Marker.lower_unbounded(type), Marker.upper_unbounded(type))

    # @classmethod
    # def greater_than(cls, type: dt.Datatype) -> 'Range[T}]':
    #     return cls(Marker.ab)

    @property
    def low(self) -> Marker[T]:
        return self._low

    @property
    def high(self) -> Marker[T]:
        return self._high

    @property
    def type(self) -> dt.Datatype:
        return self._low._type

    def __contains__(self, item: Marker[T]) -> bool:
        if type(self) is not Marker:
            return NotImplemented
        else:
            return not (self._high < item) and not (item < self._low)

    def __str__(self) -> str:
        if self.is_none:
            return '()'
        lblock = '[' if self._low.bound == Bound.EXACTLY else '('
        rblock = ']' if self._high.bound == Bound.EXACTLY else ')'
        lvalue = '...' if self._low.value is None else str(self._low.value)
        rvalue = '...' if self._high.value is None else str(self._high.value)
        return lblock + lvalue + ',' + rvalue + rblock

    @property
    def is_none(self) -> bool:
        if self._low.is_none:
            return True
        elif self._low.bound == Bound.EXACTLY and self._high.bound == Bound.EXACTLY:
            return False
        elif self._low.is_all or self._high.is_all:
            return False
        else:
            return not self._low.value < self._high.value

    @property
    def is_all(self) -> bool:
        return self._low.is_all and self._high.is_all

    @property
    def is_single_value(self) -> bool:
        return self._low.bound == Bound.EXACTLY and self._low == self._high

    @property
    def single_value(self) -> T:
        check.state(self.is_single_value)
        return self._low.value

    def _check_compat(self, other: 'Range') -> 'Range':
        check.isinstance(other, Range)
        if other._low._type != self._low._type:
            raise TypeError(other)
        return other

    def _check_marker_compat(self, marker: Marker) -> Marker:
        check.isinstance(marker, Marker)
        if marker._type != self._low._type:
            raise TypeError(marker)
        return marker

    def overlaps(self, other: 'Range') -> bool:
        self._check_compat(other)
        return self._low <= other._high and other._low <= self._high

    def includes(self, marker: Marker) -> bool:
        self._check_marker_compat(marker)
        return self._low <= marker and self._high >= marker

    def contains(self, other: 'Range') -> bool:
        self._check_marker_compat(other)
        return self._low <= other._low and self._high >= other._high

    def span(self, other: 'Range') -> 'Range[T]':
        self._check_compat(other)
        low_marker = Marker.min(self._low, other._low)
        high_marker = Marker.max(self._high, other._high)
        return Range(low_marker, high_marker)


def _mod_align_up(value: T, alignment: U) -> T:
    modulo = value % alignment
    if modulo:
        return value + (alignment - modulo)
    else:
        return value


def _equiv(l: T, r: T) -> bool:
    return not (l < r or r < l)


def aligned_range(
        rng: Range[T],
        alignment: U,
        align_up: ta.Callable[[T, U], T] = _mod_align_up
) -> ta.Iterator[Range[T]]:
    check.not_none(rng.low.value)
    check.not_none(rng.high.value)
    ty = rng.low.type

    def yield_inclusive_aligned_values() -> ta.Iterator[T]:
        cur = align_up(rng.low.value, alignment)
        while cur < rng.high.value:
            yield cur
            cur += alignment

        if _equiv(cur, rng.high.value) and rng.high.bound != Bound.BELOW:
            yield cur

    def yield_inclusive_aligned_low_markers() -> ta.Iterator[Marker[T]]:
        yield rng.low

        it = yield_inclusive_aligned_values()
        try:
            value = next(it)
        except StopIteration:
            pass
        else:
            if not _equiv(value, rng.low.value):
                yield Marker(ty, value, Bound.EXACTLY)

        for value in it:
            yield Marker(ty, value, Bound.EXACTLY)

    def yield_ranges() -> ta.Iterator[Range[T]]:
        it = yield_inclusive_aligned_low_markers()
        low = next(it)

        for next_low in it:
            yield Range(low, Marker(ty, next_low.value, Bound.BELOW))
            low = next_low

        yield Range(low, rng.high)

    return yield_ranges()
