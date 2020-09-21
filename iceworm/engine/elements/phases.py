import functools
import itertools
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang


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


class Phases(lang.ValueEnum):
    BOOTSTRAP = Phase('bootstrap')
    SITES = Phase('sites')
    RULES = Phase('rules')
    CONNECTORS = Phase('connectors')
    TARGETS = Phase('targets')
    PLAN = Phase('plan')
    FINALIZE = Phase('finalize')


del _seq
check.state(all(n == v.name.upper() for n, v in Phases._by_name.items()))
PHASES = list(Phases._by_value)


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


class SubPhases(lang.ValueEnum):
    PRE = SubPhase('Pre')
    MAIN = SubPhase('Main')
    POST = SubPhase('Post')


del _seq
check.state(all(n == v.name.upper() for n, v in SubPhases._by_name.items()))
SUB_PHASES = list(SubPhases._by_value)


class PhasePair(dc.Pure):
    phase: Phase = dc.field(check=lambda o: isinstance(o, Phase))
    sub_phase: SubPhase = dc.field(check=lambda o: isinstance(o, SubPhase))

    @property
    def name(self) -> str:
        return (
            (self.sub_phase.name.lower().capitalize() if self.sub_phase is not SubPhases.MAIN else '') +
            self.phase.name.lower().capitalize()
        )
