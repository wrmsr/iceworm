"""
TODO:
 - funuctions, procs, views, tables?
 - temp, transient, gc'd
 - snowflake, pg
 - sha-suffixed, revision tagged
 - ** coordinated through engine's pg coord? **
  - still want here, iface it - pluggable policies
   - connection_snitch
   - comment_scan

select pid, backend_start from pg_stat_activity
"""
from omnibus import check
from omnibus import configs as cfgs
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import lifecycles as lc
import sqlalchemy as sa

from .adapter import Adapter


class ObjectType(lang.AutoEnum):
    FUNCTION = ...
    TABLE = ...
    VIEW = ...


class NamingPolicy:
    pass


class ObjectManager(lc.ContextManageableLifecycle, cfgs.Configurable['ObjectManager.Config']):

    class Config(dc.Pure, cfgs.Config):
        pass

    def __init__(self, engine: sa.engine.Engine, adapter: Adapter, config: Config = Config()) -> None:
        super().__init__(config=config)

        self._engine = check.isinstance(engine, sa.engine.Engine)
        self._adapter = check.isinstance(adapter, Adapter)

    def get_tag(self) -> str:
        raise NotImplementedError

    def tag_object(self) -> str:
        raise NotImplementedError

    def get_active_tags(self) -> str:
        raise NotImplementedError

    def get_orphan_objects(self) -> str:
        raise NotImplementedError
