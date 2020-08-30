"""
TODO:
 - all, backfill, ddl, check, ...
 - views are targets, goals are like backfill and day and ddl
  - goals take targets and make ops, ops get rewritten and shit
  - ‘rules’?
  - ‘subsystems’? muh
  - CreateTableAs = rule, 'create table foo as select * from …' = .. rule 'call'? 'instantiation'?, wo.View = target
"""
import typing as ta

from omnibus import dataclasses as dc


class Goal(dc.Enum):

    @property
    def name(self) -> ta.Optional[str]:
        return None


class Invalidation(Goal):
    pass
