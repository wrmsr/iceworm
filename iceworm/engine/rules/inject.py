import typing as ta

from omnibus import check
from omnibus import inject as inj
import omnibus.inject.scopes  # noqa

from .. import elements as els
from .base import RuleElementProcessor
from .base import RuleProcessor


def bind_rule_processor(binder: inj.Binder, cls: ta.Type[RuleProcessor], phase: els.Phase) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, RuleProcessor)
    check.isinstance(phase, els.Phase)
    scope = els.inject.get_scope(els.PhasePair(phase, els.SubPhases.MAIN))

    binder.bind(cls, in_=scope)
    binder.new_set_binder(RuleProcessor, annotated_with=phase, in_=scope).bind(to=cls)

    def provide_element_processor(rp: cls) -> RuleElementProcessor[cls]:
        return RuleElementProcessor(rp)

    binder.bind_callable(provide_element_processor, in_=scope)
    binder.new_set_binder(els.ElementProcessor, annotated_with=phase, in_=scope).bind(to_provider=RuleElementProcessor[cls])  # noqa
