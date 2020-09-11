import abc
import functools
import itertools
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang

from .base import Element
from .collections import ElementSet


_seq = itertools.count()


@functools.total_ordering
class Phase(dc.Pure, eq=False, order=False):
    name: str
    seq: int = dc.field(kwonly=True, default_factory=lambda: next(_seq))

    def __lt__(self, other: ta.Any) -> bool:
        check.isinstance(other, Phase)
        return self.seq < other.seq

    def __add__(self, i: int) -> 'Phase':
        check.isinstance(i, int)
        n = self.seq + i
        return PHASES[n]

    def __sub__(self, i: int) -> 'Phase':
        check.isinstance(i, int)
        n = self.seq - i
        check.state(n >= 0)
        return PHASES[n]


del _seq


class Phases(lang.ValueEnum, ignore=['all']):
    BOOTSTRAP = Phase('bootstrap')
    SITES = Phase('sites')
    RULES = Phase('rules')
    CONNECTORS = Phase('connectors')
    TARGETS = Phase('targets')
    FINALIZE = Phase('finalize')

    @classmethod
    def all(cls) -> ta.List[Phase]:
        return list(cls._by_value)


check.state(all(n == v.name.upper() for n, v in Phases._by_name.items()))
PHASES = Phases.all()


_seq = itertools.count()


@functools.total_ordering
class SubPhase(dc.Pure, eq=False, order=False):
    name: str
    seq: int = dc.field(kwonly=True, default_factory=lambda: next(_seq))

    def __lt__(self, other: ta.Any) -> bool:
        check.isinstance(other, SubPhase)
        return self.seq < other.seq

    def __add__(self, i: int) -> 'SubPhase':
        check.isinstance(i, int)
        n = self.seq + i
        return SUB_PHASES[n]

    def __sub__(self, i: int) -> 'SubPhase':
        check.isinstance(i, int)
        n = self.seq - i
        check.state(n >= 0)
        return SUB_PHASES[n]


del _seq


class SubPhases(lang.ValueEnum, ignore=['all']):
    PRE = SubPhase('Pre')
    MAIN = SubPhase('Main')
    POST = SubPhase('Post')

    @classmethod
    def all(cls) -> ta.List[SubPhase]:
        return list(cls._by_value)


check.state(all(n == v.name.upper() for n, v in SubPhase._by_name.items()))
SUB_PHASES = SubPhases.all()


class PhasePair(dc.Pure):
    phase: Phase = dc.field(check=lambda o: isinstance(o, Phase))
    sub_phase: SubPhase = dc.field(check=lambda o: isinstance(o, SubPhase))
