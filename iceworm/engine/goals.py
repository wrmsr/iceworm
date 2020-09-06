"""
TODO:
 - all, backfill, ddl, check, ...
 - views are elements, goals are like backfill and day and ddl
  - goals take elements and make ops, ops get rewritten and shit
  - ‘rules’?
  - ‘subsystems’? muh
  - CreateTableAs = rule, 'create table foo as select * from …' = .. rule 'call'? 'instantiation'?, wo.View = element
"""
import typing as ta

from omnibus import dataclasses as dc


class Goal(dc.Enum):

    @property
    def name(self) -> ta.Optional[str]:
        return None


class Invalidate(Goal):
    pass
