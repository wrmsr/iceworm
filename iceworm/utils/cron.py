"""
https://en.wikipedia.org/wiki/Cron
"""
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc

from .utils import seq


T = ta.TypeVar('T')


class Enum(dc.Pure):
    lst: ta.Sequence[str]
    dct: ta.Mapping[str, int]


def _enum(l: ta.Sequence[T]) -> ta.Mapping[T, int]:
    return Enum(ocol.frozenlist(l), ocol.frozendict(map(reversed, enumerate(l))))


MONTHS = _enum([
    'jan',
    'feb',
    'mar',
    'apr',
    'may',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec',
])


WEEKDAYS = _enum([
    'sun',
    'mon',
    'tue',
    'wed',
    'thu',
    'fri',
    'sat',
    'sun',
])


class Range(dc.Pure):
    min: int = dc.field(check=int.__instancecheck__)
    max: int = dc.field(check=int.__instancecheck__)

    def __post_init__(self) -> None:
        check.arg(self.min <= self.max)

    def __str__(self) -> str:
        return f'[{self.min}, {self.max}]' if self.min != self.max else str(self.min)

    def __contains__(self, i: int) -> bool:
        return self.min <= check.isinstance(i, int) <= self.max


class Field(dc.Pure):
    name: str
    idx: int
    rng: Range
    enum: ta.Optional[Enum] = None


FIELDS = [
    Field('minute', 0, Range(0, 59)),
    Field('hour', 1, Range(0, 23)),
    Field('day', 2, Range(1, 31)),
    Field('month', 3, Range(1, 12), MONTHS),
    Field('weekday', 4, Range(0, 6), WEEKDAYS),
]


class Item(dc.Pure):
    rngs: ta.Sequence[Range] = dc.field(coerce=seq, check=lambda l: l and all(isinstance(o, Range) for o in l))

    def __str__(self) -> str:
        return f"{','.join(self.rngs)}" if len(self.rngs) > 1 else str(check.single(self.rngs))

    def __iter__(self) -> ta.Iterator:
        return iter(self.rngs)


class Entry(dc.Pure):
    minute: ta.Optional[Item] = dc.field(None, kwonly=True)
    hour: ta.Optional[Item] = dc.field(None, kwonly=True)
    day: ta.Optional[Item] = dc.field(None, kwonly=True)
    month: ta.Optional[Item] = dc.field(None, kwonly=True)
    weekday: ta.Optional[Item] = dc.field(None, kwonly=True)

    def __str__(self):
        return ' '.join(str(i) if i is not None else '*' for f in FIELDS for i in [getattr(self, f.name)])


def parse(s: str) -> Entry:
    parts = s.strip().split()
    check.arg(len(parts) == 5)
    kw = {}
    for p, f in zip(parts, FIELDS):
        if p == '*':
            continue
        n = int(p)
        check.arg(n in f.rng)
        kw[f.name] = Item([Range(n, n)])
    return Entry(**kw)


SPECIALS = {
    'hourly': '0 * * * *',
    'daily': '0 0 * * *',
    'weekly': '0 0 * * 0',
    'monthly': '0 0 1 * *',
    'yearly': '0 0 1 1 *',
    'annually': '0 0 1 1 *',
    'midnight': '0 0 * * *',
}
