"""
TODO:
 - * Materializer srcs specify DOMAINS *
 - region/lifetime-like..
 - DomainInvalidation
 - LookupInvalidation - 'ids' in s3, kafka.., compactable..
  - a Lookup invalidation is its own trigger..
 - sensors - s3, sftp, user
  - * codechange *
 - Invalidator takes an Invalidation
 - ** debouncer **
  - rx-y? http://reactivex.io/documentation/operators.html
 - kafka/cdc..
  - ideally compile whole shebang to a single flink/spark job
"""
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang

from .. import elements as els
from .. import ops
from .. import targets as tars
from ... import metadata as md
from ...utils import cron


class Invalidation(dc.Enum, sealed=True):
    target: els.Ref[tars.Materialization] = dc.field(coerce=els.Ref.cls(tars.Materialization).of)


class DomainInvalidation(Invalidation):
    domain: md.domains.TupleDomain[str] = dc.field(check=lambda o: isinstance(o, md.domains.TupleDomain))


class Materializer(els.Element):

    dc.metadata({
        els.PhaseFrozen: els.PhaseFrozen(els.Phases.PLAN),
    })

    target: els.Ref[tars.Materialization] = dc.field(coerce=els.Ref.cls(tars.Materialization).of)
    srcs: ta.AbstractSet[els.Ref[tars.Materialization]] = dc.field(
        coerce=lambda o: frozenset([els.Ref.cls(tars.Materialization).of(e) for e in check.not_isinstance(o, str)]))
    op: ops.Op = dc.field(check=lambda o: isinstance(o, ops.Op))


class InvalidatorTrigger(dc.Enum):
    pass


class InvalidatorTriggers(lang.Namespace):

    class Scheduled(InvalidatorTrigger):
        spec: cron.Spec = dc.field(coerce=cron.Spec.of)


class Invalidator(els.Element):

    dc.metadata({
        els.PhaseFrozen: els.PhaseFrozen(els.Phases.PLAN),
    })

    target: els.Ref[tars.Materialization] = dc.field(coerce=els.Ref.cls(tars.Materialization).of)
    trigger: InvalidatorTrigger = dc.field(check=lambda o: isinstance(o, InvalidatorTrigger))
