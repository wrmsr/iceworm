import typing as ta

from omnibus import check
from omnibus import defs
from omnibus import lang

from .. import datatypes as dt
from .sets import ValueSet


T = ta.TypeVar('T')


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


class TupleDomain(ta.Generic[T]):

    def __init__(self, domains: ta.Mapping[T, Domain]) -> None:
        super().__init__()

        self._domains: ta.Mapping[T, Domain] = {t: check.isinstance(d, Domain) for t, d in domains.items()}

    def simplify(self) -> 'TupleDomain[T]':
        raise NotImplementedError
