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
"""
from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lifecycles as lc
import sqlalchemy as sa

from ..utils import configable as cfgabl
from .adapter import Adapter


class ObjectManager(lc.ContextManageableLifecycle, cfgabl.Configable['ObjectManager.Config']):

    class Config(dc.Pure, cfgabl.Configable.Config):
        pass

    def __init__(self, engine: sa.engine.Engine, adapter: Adapter, config: Config = Config()) -> None:
        super().__init__(config=config)

        self._engine = check.isinstance(engine, sa.engine.Engine)
        self._adapter = check.isinstance(adapter, Adapter)
