import sqlalchemy.ext.compiler  # noqa
import sqlalchemy as sa


class DropTableIfExists(sa.sql.expression.Executable, sa.sql.expression.ClauseElement):

    def __init__(self, name) -> None:
        super().__init__()

        self.name = name


@sa.ext.compiler.compiles(DropTableIfExists)
def visit_drop_table_if_exists(element: DropTableIfExists, compiler, **kwargs):
    return 'DROP TABLE IF EXISTS %s' % (
        compiler.preparer.quote(element.name),
    )


class CreateTableAs(sa.sql.expression.Executable, sa.sql.expression.ClauseElement):

    def __init__(self, name, columns, query) -> None:
        super().__init__()

        self.name = name
        self.columns = columns
        self.query = query


@sa.ext.compiler.compiles(CreateTableAs)
def visit_create_table_as(element: CreateTableAs, compiler, **kwargs):
    return 'CREATE TABLE %s (%s) AS %s' % (
        compiler.preparer.quote(element.name),
        element.columns,
        compiler.process(element.query),
    )
