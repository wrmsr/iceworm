"""
TODO:
 - DomainInvalidation
 - TableInvalidation
"""
from omnibus import dataclasses as dc

from .. import domains as doms
from ..types import QualifiedName


class Invalidation(dc.Enum):
    table: QualifiedName


class DomainInvalidation(Invalidation):
    domain: doms.Domain