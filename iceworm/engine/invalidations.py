"""
TODO:
 - DomainInvalidation
 - LookupInvalidation
 - sensors - s3, sftp, user
"""
from omnibus import dataclasses as dc

from .. import domains as doms
from ..types import QualifiedName


class Invalidation(dc.Enum):
    table: QualifiedName


class DomainInvalidation(Invalidation):
    domain: doms.Domain
