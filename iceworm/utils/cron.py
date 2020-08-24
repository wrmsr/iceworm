import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc


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


class Field(dc.Pure):
    name: str
    idx: int
    min: int
    max: int
    enum: ta.Optional[Enum] = None


FIELDS = [
    Field('minute', 0, 0, 59),
    Field('hour', 1, 0, 23),
    Field('day', 2, 1, 31),
    Field('month', 3, 1, 12, MONTHS),
    Field('weekday', 4, 0, 6, WEEKDAYS),
]


class Entry(dc.Pure):
    minute: ta.Optional[int] = dc.field(None, kwonly=True)
    hour: ta.Optional[int] = dc.field(None, kwonly=True)
    day: ta.Optional[int] = dc.field(None, kwonly=True)
    month: ta.Optional[int] = dc.field(None, kwonly=True)
    weekday: ta.Optional[int] = dc.field(None, kwonly=True)


def parse(s: str) -> Entry:
    parts = s.strip().split()
    check.arg(len(parts) == 5)
    kw = {}
    for p, f in zip(parts, FIELDS):
        if p == '*':
            continue
        n = int(p)
        kw[f.name] = n
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
