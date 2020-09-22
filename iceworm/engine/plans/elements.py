"""
TODO:
 - 'Refresher' complement to 'Invalidator'?
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
from omnibus import dataclasses as dc
from omnibus import lang

from .. import elements as els
from .. import ops
from .. import targets as tars
from ... import metadata as md
from ...types import QualifiedName
from ...utils import cron


class InvalidatorTrigger(dc.Enum):
    pass


class InvalidatorTriggers(lang.Namespace):

    class Scheduled(InvalidatorTrigger):
        spec: cron.Spec = dc.field(coerce=cron.Spec.of)


class Invalidator(els.Element):

    dc.metadata({
        els.PhaseFrozen: els.PhaseFrozen(els.Phases.PLAN),
    })

    target: els.Ref[tars.Target]
    trigger: InvalidatorTrigger


class Invalidation(dc.Enum):
    table: QualifiedName


class DomainInvalidation(Invalidation):
    domain: md.domains.Domain


class Refresher:
    target: els.Ref[tars.Materialization]
    op: ops.Op
