import abc
import enum
import functools
import re
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
    __slots__ = (
        '_value',
        '_bound',
    )

    UNBOUNDED_BELOW: 'Marker' = None
    EMPTY: 'Marker' = None
    UNBOUNDED_ABOVE: 'Marker' = None

    def __init__(self, value: ta.Optional[T], bound: Bound) -> None:
        super().__init__()

        self._value = value
        self._bound = check.isinstance(bound, Bound)

    @classmethod
    def of(cls, value, bound) -> 'Marker':
        return cls(value, lang.parse_enum(bound, Bound))

    @property
    def value(self) -> ta.Optional[T]:
        return self._value

    @property
    def bound(self) -> Bound:
        return self._bound

    defs.repr('value', 'bound')
    defs.hash_eq('value', 'bound')

    def __lt__(self, other: 'Marker[T]') -> bool:
        if type(self) is not type(other):
            return NotImplemented
        else:
            return \
                self._value < other._value and \
                self._bound.value < other._bound._value

    def __str__(self) -> str:
        prefix = '<' if self._bonud == Bound.BELOW else '>' if self._bound == Bound.ABOVE else ''
        value = '...' if self._value is None else str(self._value)
        return prefix + value

    @property
    def is_none(self) -> bool:
        return self._value is None and self._bound == Bound.EXACTLY

    @property
    def is_all(self) -> bool:
        return self._value is None and self._bound != Bound.EXACTLY

    def to_dict(self):
        return {
            'value': self._value,
            'bound': self._bound._name,
        }

    @classmethod
    def from_dict(cls, dct):
        check.arg(set(dct.keys()) == {'value', 'bound'})
        return cls(dct['value'], lang.parse_enum(dct['bound'], Bound))

    to_json = _to_json = to_dict
    from_json = _from_json = from_dict


Marker.UNBOUNDED_BELOW = Marker(None, Bound.BELOW)
Marker.EMPTY = Marker(None, Bound.EXACTLY)
Marker.UNBOUNDED_ABOVE = Marker(None, Bound.ABOVE)


class Range(ta.Generic[T]):
    __slots__ = (
        '_low',
        '_high',
    )

    UNBOUNDED: 'Range' = None
    EMPTY: 'Range' = None

    def __init__(self, low: Marker[T], high: Marker[T]) -> None:
        super().__init__()

        self._low = check.isinstance(low, Marker)
        self._high = check.isinstance(high, Marker)

        if low.is_none or high.is_none:
            if not (low.is_none and high.is_none):
                raise ValueError(f'Lower {low!r} and high {high!r} must both be none')
        if low.bound == Bound.BELOW:
            raise ValueError(f'Present low {low!r} should never be BELOW')
        if high.bound == Bound.ABOVE:
            raise ValueError(f'Present high {high!r} should never be ABOVE')
        if low.value is not None and high.value is not None and low.value > high.value:
            raise ValueError(f'Lower {low!r} > high {high!r}')

    @classmethod
    def of(cls, low_value, low_bound, high_value, high_bound) -> 'Range':
        return Range(Marker.of(low_value, low_bound), Marker.of(high_value, high_bound))

    @property
    def low(self) -> Marker[T]:
        return self._low

    @property
    def high(self) -> Marker[T]:
        return self._high

    defs.repr('low', 'high')
    defs.hash_eq('low', 'high')

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

    PARSE_PATTERN = re.compile(r'([\(\[])([^,]+),([^\]\)]+)([\)\]])')

    @classmethod
    def parse(cls, s: str, *, coerce: ta.Callable[[str], T] = str) -> 'Range[T]':
        match = cls.PARSE_PATTERN.match(s)
        if not match:
            raise ValueError(s)
        lb, lv, uv, ub = match.groups()
        lv = coerce(lv) if lv != '...' else None
        uv = coerce(uv) if uv != '...' else None
        return cls(
            Marker.UNBOUNDED_ABOVE if lv is None else Marker(lv, Bound.ABOVE if lb == '(' else Bound.EXACTLY),
            Marker.UNBOUNDED_BELOW if uv is None else Marker(uv, Bound.BELOW if ub == ')' else Bound.EXACTLY),
        )

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

    def to_dict(self) -> dict:
        return {
            'low': self._low.to_dict(),
            'high': self._high.to_dict(),
        }

    @classmethod
    def from_dict(cls, dct):
        check.arg(set(dct.keys()) == {'low', 'high'})
        return cls(Marker.from_dict(dct['low']), Marker.from_dict(dct['high']))

    to_json = _to_json = to_dict
    from_json = _from_json = from_dict


Range.UNBOUNDED = Range(Marker.UNBOUNDED_ABOVE, Marker.UNBOUNDED_BELOW)
Range.EMPTY = Range(Marker.EMPTY, Marker.EMPTY)


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
                yield Marker(value, Bound.EXACTLY)

        for value in it:
            yield Marker(value, Bound.EXACTLY)

    def yield_ranges() -> ta.Iterator[Range[T]]:
        it = yield_inclusive_aligned_low_markers()
        low = next(it)

        for next_low in it:
            yield Range(low, Marker(next_low.value, Bound.BELOW))
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
        raise NotImplementedError

    def contains_value(self, value: ta.Any) -> bool:
        raise NotImplementedError

    def intersect(self, other: 'ValueSet') -> 'ValueSet':
        raise NotImplementedError

    def union(self, other: 'ValueSet') -> 'ValueSet':
        raise NotImplementedError

    def complement(self) -> 'ValueSet':
        raise NotImplementedError


class SortedRangeSet(ValueSet, lang.Final):

    def __init__(self, type: dt.Datatype, low_indexed_ranges: ocol.SortedMapping[Marker, Range]) -> None:
        super().__init__()

        self._type = check.isinstance(type, dt.Datatype)
        self._low_indexed_ranges = check.isinstance(low_indexed_ranges, ocol.SortedMapping)

        check.state(self._type.is_sortable)

        self._ranges = list(self._low_indexed_ranges.values())

    defs.basic('type', 'low_indexed_ranges')

    @classmethod
    def none(cls, type: dt.Datatype) -> ValueSet:
        raise NotImplementedError

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
        if other.type.py_type != self._type:
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
