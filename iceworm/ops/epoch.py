import datetime
import typing as ta

from omnibus import check
from omnibus import defs
from omnibus import spans


Timespan = spans.Span[datetime.datetime]


class Epoch:

    def __init__(self, timespan: ta.Optional[Timespan] = None) -> None:
        super().__init__()

        self._timespan = check.isinstance(timespan, (spans.Span, None))

    defs.repr('timespan')

    @property
    def timespan(self) -> ta.Optional[Timespan]:
        return self._timespan
