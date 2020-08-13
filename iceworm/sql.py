from omnibus import check
import sqlalchemy as sa
import sqlalchemy.ext.compiler  # noqa

from .types import QualifiedName


class QualifiedNameElement(sa.sql.expression.ClauseElement):

    def __init__(self, name: QualifiedName) -> None:
        super().__init__()

        self.name = check.isinstance(name, QualifiedName)


@sa.ext.compiler.compiles(QualifiedNameElement)
def visit_qualified_name(element: QualifiedNameElement, compiler, **kwargs):
    return '%s' % (
        '.'.join(compiler.preparer.quote(p) for p in element.name),
    )


class DropTableIfExists(sa.sql.expression.Executable, sa.sql.expression.ClauseElement):

    def __init__(self, name) -> None:
        super().__init__()

        self.name = name


@sa.ext.compiler.compiles(DropTableIfExists)
def visit_drop_table_if_exists(element: DropTableIfExists, compiler, **kwargs):
    return 'DROP TABLE IF EXISTS %s' % (
        compiler.process(element.name),
    )


class CreateTableAs(sa.sql.expression.Executable, sa.sql.expression.ClauseElement):

    def __init__(self, name, query) -> None:
        super().__init__()

        self.name = name
        self.query = query


@sa.ext.compiler.compiles(CreateTableAs)
def visit_create_table_as(element: CreateTableAs, compiler, **kwargs):
    return 'CREATE TABLE %s AS %s' % (
        compiler.process(element.name),
        compiler.process(element.query),
    )
