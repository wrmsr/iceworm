"""
TODO:
 - QualifiedName visitability.. somewhere
 - CreateOrReplaceTable (w/ prefixes)
 - batching for snowflake...
"""
from omnibus import dataclasses as dc
import sqlalchemy as sa
import sqlalchemy.ext.compiler  # noqa

from ..types import QualifiedName


@dc.dataclass(frozen=True)
class QualifiedNameElement(sa.sql.expression.ClauseElement):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)


@sa.ext.compiler.compiles(QualifiedNameElement)
def visit_qualified_name(element: QualifiedNameElement, compiler, **kwargs):
    return '%s' % (
        '.'.join(compiler.preparer.quote(p) for p in element.name),
    )


@dc.dataclass(frozen=True)
class DropTableIfExists(sa.sql.expression.Executable, sa.sql.expression.ClauseElement):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)


@sa.ext.compiler.compiles(DropTableIfExists)
def visit_drop_table_if_exists(element: DropTableIfExists, compiler, **kwargs):
    return 'DROP TABLE IF EXISTS %s' % (
        '.'.join(compiler.preparer.quote(p) for p in element.name),
    )


@dc.dataclass(frozen=True)
class CreateTableAs(sa.sql.expression.Executable, sa.sql.expression.ClauseElement):
    name: sa.sql.visitors.Visitable = dc.field(check=lambda o: isinstance(o, sa.sql.visitors.Visitable))
    query: sa.sql.visitors.Visitable = dc.field(check=lambda o: isinstance(o, sa.sql.visitors.Visitable))


@sa.ext.compiler.compiles(CreateTableAs)
def visit_create_table_as(element: CreateTableAs, compiler, **kwargs):
    return 'CREATE TABLE %s AS %s' % (
        compiler.process(element.name),
        compiler.process(element.query),
    )
