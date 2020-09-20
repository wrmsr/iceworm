"""
TODO:
 - ->omni ?
"""
import abc
import enum
import functools
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import defs
from omnibus import lang

from . import datatypes as dt


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
    def exactly(cls, type: dt.Datatype, value: T) -> 'Marker[T]':
        return cls(type, value, Bound.EXACTLY)

    @classmethod
    def upper_unbounded(cls, type: dt.Datatype) -> 'Marker[T]':
        return cls(type, None, Bound.BELOW)

    @classmethod
    def lower_unbounded(cls, type: dt.Datatype) -> 'Marker[T]':
        return cls(type, None, Bound.ABOVE)

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


class DiscreteValues(lang.Abstract):

    @abc.abstractproperty
    def is_white_list(self) -> bool:
        raise NotImplementedError

    @abc.abstractproperty
    def values(self) -> ta.Collection[ta.Any]:
        raise NotImplementedError


class ValueSet(lang.Abstract):

    @abc.abstractproperty
    def type(self) -> dt.Datatype:
        raise NotImplementedError

    @abc.abstractproperty
    def is_none(self) -> bool:
        raise NotImplementedError

    @abc.abstractproperty
    def is_all(self) -> bool:
        raise NotImplementedError

    @abc.abstractproperty
    def is_single_value(self) -> bool:
        raise NotImplementedError

    @property
    def single_value(self) -> ta.Any:
        raise TypeError

    @abc.abstractmethod
    def contains_value(self, value: ta.Any) -> bool:
        raise NotImplementedError

    @property
    def discrete_values(self) -> DiscreteValues:
        raise TypeError

    @property
    def ranges(self) -> 'Ranges':
        raise TypeError

    @abc.abstractmethod
    def intersect(self, other: 'ValueSet') -> 'ValueSet':
        raise NotImplementedError

    @abc.abstractmethod
    def union(self, other: 'ValueSet') -> 'ValueSet':
        raise NotImplementedError

    @abc.abstractmethod
    def complement(self) -> 'ValueSet':
        raise NotImplementedError

    def overlaps(self, other: 'ValueSet') -> bool:
        return not self.intersect(other).is_none

    def subtract(self, other: 'ValueSet') -> 'ValueSet':
        return self.intersect(other.complement())

    def contains(self, other: 'ValueSet') -> bool:
        return self.union(other) == self

    @staticmethod
    def none(type: dt.Datatype) -> 'ValueSet':
        if type.is_sortable:
            return SortedRangeSet.none(type)
        elif type.is_equatable:
            return EquatableValueSet.none(type)
        else:
            return AllOrNoneValueSet.none(type)

    @staticmethod
    def all(type: dt.Datatype) -> 'ValueSet':
        if type.is_sortable:
            return SortedRangeSet.all(type)
        elif type.is_equatable:
            return EquatableValueSet.all(type)
        else:
            return AllOrNoneValueSet.all(type)


class AllOrNoneValueSet(ValueSet, lang.Final):

    def __init__(self, type: dt.Datatype, is_all: bool) -> None:
        super().__init__()

        self._type = check.isinstance(type, dt.Datatype)
        self._is_all = check.isinstance(is_all, bool)

    defs.basic('type', 'is_all')

    @classmethod
    def none(cls, type: dt.Datatype) -> ValueSet:
        return cls(type, False)

    @classmethod
    def all(cls, type: dt.Datatype) -> ValueSet:
        return cls(type, True)

    @property
    def type(self) -> dt.Datatype:
        return self._type

    @property
    def is_none(self) -> bool:
        return not self._is_all

    @property
    def is_all(self) -> bool:
        return self._is_all

    @property
    def is_single_value(self) -> bool:
        return False

    def contains_value(self, value: ta.Any) -> bool:
        if not isinstance(value, self._type.py_type):
            raise TypeError(value)
        return self._is_all

    def _check_compat(self, other: 'ValueSet') -> 'AllOrNoneValueSet':
        if other.type.py_type != self._type:
            raise TypeError(other)
        if not isinstance(other, AllOrNoneValueSet):
            raise TypeError(other)
        return ta.cast(AllOrNoneValueSet, other)

    def intersect(self, other: 'ValueSet') -> 'ValueSet':
        other = self._check_compat(other)
        return AllOrNoneValueSet(self._type, self._is_all and other._is_all)

    def union(self, other: 'ValueSet') -> 'ValueSet':
        other = self._check_compat(other)
        return AllOrNoneValueSet(self._type, self._is_all or other._is_all)

    def complement(self) -> 'ValueSet':
        return AllOrNoneValueSet(self._type, not self._is_all)


class EquatableValueSet(ValueSet, lang.Final):

    def __init__(self, type: dt.Datatype, is_white_list: bool, values: ta.Iterable[ta.Any]) -> None:
        super().__init__()

        self._type = check.isinstance(type, dt.Datatype)
        self._is_white_list = check.isinstance(is_white_list, bool)
        self._values = frozenset(check.not_isinstance(values, str))

    defs.basic('type', 'is_white_list', 'values')

    @classmethod
    def none(cls, type: dt.Datatype) -> ValueSet:
        return cls(type, True, [])

    @classmethod
    def all(cls, type: dt.Datatype) -> ValueSet:
        return cls(type, False, [])

    @property
    def type(self) -> dt.Datatype:
        return self._type

    @property
    def is_white_list(self) -> bool:
        return self._is_white_list

    @property
    def values(self) -> ta.AbstractSet[ta.Any]:
        return self._values

    @property
    def is_none(self) -> bool:
        return self._is_white_list and not self._values

    @property
    def is_all(self) -> bool:
        return not self._is_white_list and not self._values

    @property
    def is_single_value(self) -> bool:
        return self._is_white_list and len(self._values) == 1

    @property
    def single_value(self) -> ta.Any:
        check.state(self.is_single_value)
        return check.single(self._values)

    def contains_value(self, value: ta.Any) -> bool:
        return self._is_white_list == (value in self._values)

    def _check_compat(self, other: 'ValueSet') -> 'EquatableValueSet':
        if other.type.py_type != self._type:
            raise TypeError(other)
        if not isinstance(other, EquatableValueSet):
            raise TypeError(other)
        return ta.cast(EquatableValueSet, other)

    def intersect(self, other: 'ValueSet') -> 'ValueSet':
        other = self._check_compat(other)
        if self._is_white_list and other._is_white_list:
            return EquatableValueSet(self._type, True, self._values & other._values)
        elif self._is_white_list:
            return EquatableValueSet(self._type, True, self._values - other._values)
        elif other._is_white_list:
            return EquatableValueSet(self._type, False, other._values - self._values)
        else:
            return EquatableValueSet(self._type, False, other._values | self._values)

    def union(self, other: 'ValueSet') -> 'ValueSet':
        other = self._check_compat(other)
        if self._is_white_list and other._is_white_list:
            return EquatableValueSet(self._type, True, self._values | other._values)
        elif self._is_white_list:
            return EquatableValueSet(self._type, False, other._values - self._values)
        elif other._is_white_list:
            return EquatableValueSet(self._type, False, self._values - other._values)
        else:
            return EquatableValueSet(self._type, False, other._values & self._values)

    def complement(self) -> 'ValueSet':
        return EquatableValueSet(self._type, not self._is_white_list, self._values)


class SortedRangeSet(ValueSet, lang.Final):

    def __init__(self, type: dt.Datatype, ranges: ta.Iterable[Range]) -> None:
        super().__init__()

        self._type = check.isinstance(type, dt.Datatype)
        self._ranges = [check.isinstance(r, Range) for r in ranges]
        check.state(self._type.is_sortable)

        self._ranges.sort(key=lambda r: r.low)

        dct: ocol.SortedMapping[Marker, Range] = ocol.SkipListDict()

        cur = self._ranges[0] if self._ranges else None
        for nxt in self._ranges[1:]:
            if cur.overlaps(nxt) or cur.high.is_adjacent(nxt.low):
                cur = cur.span(nxt)
            else:
                dct[cur.low] = cur
                cur = nxt
        if cur is not None:
            dct[cur.low] = cur

        if isinstance(self._type, dt.Boolean):
            true_allowed = False
            false_allowed = False
            for k, v in dct.items():
                if v.includes(Marker.exactly(dt.Boolean(), True)):
                    true_allowed = True
                if v.includes(Marker.exactly(dt.Boolean(), False)):
                    false_allowed = True

            if true_allowed and false_allowed:
                dct = ocol.SkipListDict()
                dct[Range.all(dt.Boolean()).low] = Range.all(dt.Boolean())

        self._low_indexed_ranges = dct

    defs.basic('type', 'ranges')

    @classmethod
    def none(cls, type: dt.Datatype) -> ValueSet:
        return cls(type, [])

    @classmethod
    def all(cls, type: dt.Datatype) -> ValueSet:
        raise NotImplementedError

    @property
    def type(self) -> dt.Datatype:
        return self._type

    @property
    def ranges(self) -> ta.Sequence[Range]:
        return self._ranges

    @property
    def is_none(self) -> bool:
        return not self._ranges

    @property
    def is_all(self) -> bool:
        return len(self._ranges) == 1 and self.ranges[0].is_all

    @property
    def is_single_value(self) -> bool:
        return len(self._ranges) == 1 and self.ranges[0].is_single_value

    def contains_value(self, value: ta.Any) -> bool:
        raise NotImplementedError

    def intersect(self, other: 'ValueSet') -> 'ValueSet':
        raise NotImplementedError

    def union(self, other: 'ValueSet') -> 'ValueSet':
        raise NotImplementedError

    def complement(self) -> 'ValueSet':
        raise NotImplementedError


class Domain(lang.Final):

    def __init__(self, values: ValueSet, null_allowed: bool) -> None:
        super().__init__()

        self._values = check.isinstance(values, ValueSet)
        self._null_allowed = check.isinstance(null_allowed, bool)

    defs.basic('values', 'nulls_allowed')

    @classmethod
    def none(cls, type: dt.Datatype) -> 'Domain':
        return cls(ValueSet.none(type), False)

    @classmethod
    def all(cls, type: dt.Datatype) -> 'Domain':
        return cls(ValueSet.all(type), False)

    @property
    def type(self) -> dt.Datatype:
        return self._values.type

    @property
    def values(self) -> ValueSet:
        return self._values

    @property
    def nulls_allowed(self) -> bool:
        return self._null_allowed

    @property
    def is_none(self) -> bool:
        return self._values.is_none and not self._null_allowed

    @property
    def is_all(self) -> bool:
        return self._values.is_all and self._null_allowed

    @property
    def is_single_value(self) -> bool:
        return not self._null_allowed and self._values.is_single_value

    @property
    def is_nullable_single_value(self) -> bool:
        if self._null_allowed:
            return self.is_none
        else:
            return self._values.is_single_value

    @property
    def is_only_null(self) -> bool:
        return self._values.is_none and self._null_allowed

    @property
    def single_value(self) -> ta.Any:
        if not self.is_single_value:
            raise TypeError(self)
        return self._values.single_value

    @property
    def nullable_single_value(self) -> ta.Any:
        if not self.is_nullable_single_value:
            raise TypeError(self)
        if self._null_allowed:
            return None
        else:
            return self._values.single_value

    def includes_nullable_value(self, value: ta.Any) -> bool:
        if value is None:
            return self._null_allowed
        else:
            return self._values.contains_value(value)

    def _check_compat(self, other: 'Domain') -> 'Domain':
        if other.type.py_type != self._values.type:
            raise TypeError(other)
        if not isinstance(other, Domain):
            raise TypeError(other)
        return ta.cast(Domain, other)

    def overlaps(self, other: 'Domain') -> bool:
        other = self._check_compat(other)
        return not self.intersect(other).is_none

    def contains(self, other: 'Domain') -> bool:
        other = self._check_compat(other)
        return self.union(other) == self

    def intersect(self, other: 'Domain') -> 'Domain':
        other = self._check_compat(other)
        return Domain(self._values.intersect(other._values), self._null_allowed and other._null_allowed)

    def union(self, other: 'Domain') -> 'Domain':
        other = self._check_compat(other)
        return Domain(self._values.union(other._values), self._null_allowed or other._null_allowed)

    def complement(self) -> 'Domain':
        return Domain(self._values.complement(), not self._null_allowed)

    def subtract(self, other: 'Domain') -> 'Domain':
        other = self._check_compat(other)
        return Domain(self._values.subtract(other._values), self._null_allowed and other._null_allowed)


class TupleDomain:
    pass
