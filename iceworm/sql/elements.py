"""
TODO:
 - fix
"""
from omnibus import check
import sqlalchemy as sa
import sqlalchemy.ext.compiler  # noqa
import sqlalchemy.sql.selectable  # noqa

from ..types import QualifiedName


class QualifiedNameElement(sa.sql.expression.ClauseElement):

    def __init__(self, name):
        super().__init__()
        self.name = QualifiedName.of(name)


@sa.ext.compiler.compiles(QualifiedNameElement)
def visit_qualified_name(element: QualifiedNameElement, compiler, **kwargs):
    return '%s' % (
        '.'.join(compiler.preparer.quote(p) for p in element.name),
    )


class DropTableIfExists(sa.sql.expression.Executable, sa.sql.expression.ClauseElement):

    def __init__(self, name):
        super().__init__()
        self.name = QualifiedName.of(name)


@sa.ext.compiler.compiles(DropTableIfExists)
def visit_drop_table_if_exists(element: DropTableIfExists, compiler, **kwargs):
    return 'DROP TABLE IF EXISTS %s' % (
        '.'.join(compiler.preparer.quote(p) for p in element.name),
    )


class CreateTableAs(sa.sql.expression.Executable, sa.sql.expression.ClauseElement):

    def __init__(self, name, query):
        super().__init__()
        self.name = name
        self.query = query


@sa.ext.compiler.compiles(CreateTableAs)
def visit_create_table_as(element: CreateTableAs, compiler, **kwargs):
    return 'CREATE TABLE %s AS %s' % (
        compiler.process(element.name),
        compiler.process(element.query),
    )


class ColumnListAlias(sa.sql.selectable.Alias):

    def _init(self, selectable, name, cols):
        super()._init(selectable, name)
        self.cols = [check.not_empty(check.isinstance(c, str)) for c in check.not_isinstance(cols, str)]


    @classmethod
    def _factory(cls, selectable, name, cols):
        return cls._construct(sa.sql.selectable._interpret_as_from(selectable), name, cols)


@sa.ext.compiler.compiles(ColumnListAlias)
def visit_column_list_alias(element: ColumnListAlias, compiler, **kwargs):
    s = compiler.visit_alias(element, **kwargs)
    s += '(' + ', '.join(compiler.preparer.quote(c) for c in element.cols) + ')'
    return s


column_list_alias = ColumnListAlias._factory
create_table_as = CreateTableAs
drop_table_if_exists = DropTableIfExists
qualified_name = QualifiedNameElement
