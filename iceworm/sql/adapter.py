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

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
import sqlalchemy as sa  # noqa

from ..utils import configable as cfgabl
from ..utils import serde


AdapterT = ta.TypeVar('AdapterT', bound='Adapter')
AdapterConfigT = ta.TypeVar('AdapterConfigT', bound='Adapter.Config')


class Adapter(cfgabl.Configable[AdapterConfigT], lang.Abstract):

    class Config(dc.Enum, cfgabl.Configable.Config):
        dc.metadata({
            serde.Name: lambda cls: lang.decamelize(cfgabl.get_impl(cls).__name__[:-7]),
        })

    def __init__(self, config: AdapterConfigT) -> None:
        super().__init__(config)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        check.state(cls.__name__.endswith('Adapter'))

    def build_range(self, num):
        raise NotImplementedError

    def render_query(self, stmt: sa.sql.visitors.Visitable) -> str:
        return str(stmt.compile(compile_kwargs={'literal_binds': True}))
