"""
TODO:
 - DomainInvalidation
 - LookupInvalidation
 - sensors - s3, sftp, user
  - * codechange *
"""
from omnibus import dataclasses as dc
from omnibus import lang

from .. import domains as doms
from ..types import QualifiedName
from ..utils import cron
from .targets import Target


class InvalidatorKind(dc.Enum):
    pass


class InvalidatorKinds(lang.Namespace):

    class Scheduled(InvalidatorKind):
        spec: cron.Spec = dc.field(coerce=cron.Spec.of)


class Invalidator(Target):
    table: QualifiedName
    kind: InvalidatorKind


class Invalidation(dc.Enum):
    table: QualifiedName


class DomainInvalidation(Invalidation):
    domain: doms.Domain
