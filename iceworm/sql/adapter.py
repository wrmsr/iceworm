"""
TODO:
 - balance between dialect-specific elements and adapter methods
  - decree: if it can be an element make it an element, if it's 'procedural' then adapter
  - ** HOEWVER ** if it can be done with existing elements, make a method that returns those..
   - introspectiible, rewritiable, etc - strongly prefer asts
"""
import sqlalchemy as sa  # noqa


class Adapter:

    def build_range(self, num):
        raise NotImplementedError
