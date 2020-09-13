"""
TODO:
 - balance between dialect-specific elements and adapter methods
  - decree: if it can be an element make it an element, if it's 'procedural' then adapter
  - ** HOEWVER ** if it can be done with existing elements, make a method that returns those..
   - introspectiible, rewritiable, etc - strongly prefer asts
 - better string rendering
  - https://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
  - snowflake (json)
  - pg (bytes)
"""
import typing as ta

from omnibus import dataclasses as dc
from omnibus import lang
import sqlalchemy as sa  # noqa

from ..utils import configable as cfgable


AdapterT = ta.TypeVar('AdapterT', bound='Adapter')
AdapterConfigT = ta.TypeVar('AdapterConfigT', bound='Adapter.Config')


class Adapter(cfgable.Configable[AdapterConfigT], lang.Abstract):

    class Config(dc.Enum, cfgable.Configable.Config):
        pass

    def __init__(self, config: AdapterConfigT) -> None:
        super().__init__(config)

    def build_range(self, num):
        raise NotImplementedError

    def render_query(self, stmt: sa.sql.visitors.Visitable) -> str:
        return str(stmt.compile(compile_kwargs={'literal_binds': True}))
