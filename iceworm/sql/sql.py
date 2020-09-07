"""
TODO:
 - QualifiedName visitability.. somewhere
 - CreateOrReplaceTable (w/ prefixes)
 - batching for snowflake...
 - helper against sqla inserts with nonexisting columns :/
 - better string rendering
  - https://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
  - snowflake (json)
  - pg (bytes)
 - dialect abstraction, or elements?
  - range gen:
   - pg: `select i from generate_series(1, 5) s(i)`
   - sf: `select seq4() i from table(generator(rowcount => 10))`
"""
import sqlalchemy as sa
import sqlalchemy.ext.compiler  # noqa


def render_query(stmt: sa.sql.visitors.Visitable) -> str:
    return stmt.compile(compile_kwargs={'literal_binds': True})
