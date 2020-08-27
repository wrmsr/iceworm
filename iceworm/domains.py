import abc
import typing as ta

from omnibus import check
from omnibus import defs
from omnibus import lang

from . import datatypes as dt


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
    def discrete_values(self) -> 'DiscreteValues':
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
            return SortedValueSet.none(type)
        elif type.is_equatable:
            return EquatableValueSet.none(type)
        else:
            return AllOrNoneValueSet.none(type)

    @staticmethod
    def all(type: dt.Datatype) -> 'ValueSet':
        if type.is_sortable:
            return SortedValueSet.all(type)
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
        raise NotImplementedError

    @property
    def is_all(self) -> bool:
        raise NotImplementedError

    @property
    def is_single_value(self) -> bool:
        raise NotImplementedError

    def contains_value(self, value: ta.Any) -> bool:
        pass

    def intersect(self, other: 'ValueSet') -> 'ValueSet':
        pass

    def union(self, other: 'ValueSet') -> 'ValueSet':
        pass

    def complement(self) -> 'ValueSet':
        pass


class DiscreteValues(lang.Abstract):

    @abc.abstractproperty
    def is_white_list(self) -> bool:
        raise NotImplementedError

    @abc.abstractproperty
    def values(self) -> ta.Collection[ta.Any]:
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
