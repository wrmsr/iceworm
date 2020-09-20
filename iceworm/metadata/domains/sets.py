import abc
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import defs
from omnibus import lang

from .. import datatypes as dt
from .ranges import Marker
from .ranges import Range


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

    def intersect(self, other: 'ValueSet') -> 'AllOrNoneValueSet':
        other = self._check_compat(other)
        return AllOrNoneValueSet(self._type, self._is_all and other._is_all)

    def union(self, other: 'ValueSet') -> 'AllOrNoneValueSet':
        other = self._check_compat(other)
        return AllOrNoneValueSet(self._type, self._is_all or other._is_all)

    def complement(self) -> 'AllOrNoneValueSet':
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

    def intersect(self, other: 'ValueSet') -> 'EquatableValueSet':
        other = self._check_compat(other)
        if self._is_white_list and other._is_white_list:
            return EquatableValueSet(self._type, True, self._values & other._values)
        elif self._is_white_list:
            return EquatableValueSet(self._type, True, self._values - other._values)
        elif other._is_white_list:
            return EquatableValueSet(self._type, False, other._values - self._values)
        else:
            return EquatableValueSet(self._type, False, other._values | self._values)

    def union(self, other: 'ValueSet') -> 'EquatableValueSet':
        other = self._check_compat(other)
        if self._is_white_list and other._is_white_list:
            return EquatableValueSet(self._type, True, self._values | other._values)
        elif self._is_white_list:
            return EquatableValueSet(self._type, False, other._values - self._values)
        elif other._is_white_list:
            return EquatableValueSet(self._type, False, self._values - other._values)
        else:
            return EquatableValueSet(self._type, False, other._values & self._values)

    def complement(self) -> 'EquatableValueSet':
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
        return SortedRangeSet(type, [Range.all(type)])

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

    @property
    def single_value(self) -> ta.Any:
        check.state(self.is_single_value)
        return check.single(self._low_indexed_ranges.values()).single_value

    def contains_value(self, value: ta.Any) -> bool:
        return self._includes_marker(Marker.exactly(self._type, value))

    def _check_marker_compat(self, marker: Marker) -> Marker:
        if marker.type.py_type != self._type:
            raise TypeError(marker)
        return marker

    def _includes_marker(self, marker: Marker) -> bool:
        self._check_marker_compat(marker)
        try:
            floor = next(self._low_indexed_ranges.ritemsfrom(marker))
        except StopIteration:
            return False
        return floor[1].includes(marker)

    def _check_compat(self, other: 'ValueSet') -> 'SortedRangeSet':
        if other.type.py_type != self._type:
            raise TypeError(other)
        if not isinstance(other, SortedRangeSet):
            raise TypeError(other)
        return ta.cast(SortedRangeSet, other)

    def intersect(self, other: 'ValueSet') -> 'SortedRangeSet':
        other = self._check_compat(other)
        raise NotImplementedError

    def union(self, other: 'ValueSet') -> 'SortedRangeSet':
        other = self._check_compat(other)
        raise NotImplementedError

    def complement(self) -> 'ValueSet':
        raise NotImplementedError
