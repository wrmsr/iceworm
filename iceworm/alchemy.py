"""
TODO:
 - postgres, hive, presto
 - spark? need dialect?
"""
import typing as ta

from omnibus import check
from omnibus import dispatch
import sqlalchemy as sa
import sqlalchemy.sql.elements
import sqlalchemy.sql.sqltypes

from . import datatypes as dt
from . import metadata as md
from . import nodes as no


Visitable = sa.sql.elements.Visitable


class Transmuter(dispatch.Class):
    transmute = dispatch.property()

    def transmute(self, node: no.Node) -> Visitable:  # noqa
        raise TypeError(node)

    def transmute(self, node: no.Integer) -> Visitable:  # noqa
        return sa.literal(node.value)


def transmute(node: no.Node) -> Visitable:
    return Transmuter().transmute(node)


class FromInternal(dispatch.Class):

    def __init__(self, metadata: ta.Optional[sa.MetaData] = None) -> None:
        super().__init__()

        self._metadata = check.isinstance(metadata, sa.MetaData)

    __call__ = dispatch.property()

    def __call__(self, md_type: dt.Datatype) -> sa.Table:  # noqa
        if isinstance(md_type, dt.Integer):
            return sa.Integer()
        else:
            raise TypeError(md_type)

    def __call__(self, md_col: md.Column) -> sa.Table:  # noqa
        return sa.Column(
            md_col.name,
            self(md_col.type),
            primary_key=md_col.primary_key,
        )

    def __call__(self, md_tbl: md.Table) -> sa.Table:  # noqa
        return sa.Table(
            md_tbl.name,
            self._metadata,
            *[self(col) for col in md_tbl.columns]
        )


class ToInternal(dispatch.Class):

    __call__ = dispatch.property()

    def __call__(self, sa_type: sa.sql.sqltypes.TypeEngine) -> dt.Datatype:  # noqa
        if isinstance(sa_type, sa.Integer):
            return dt.Integer()
        else:
            raise TypeError(sa_type)

    def __call__(self, sa_col: sa.Column) -> md.Column:  # noqa
        return md.Column(
            name=sa_col.name,
            type=self(sa_col.type),
            primary_key=sa_col.primary_key,
        )

    def __call__(self, sa_tbl: sa.Table) -> md.Table:  # noqa
        return md.Table(
            name=sa_tbl.name,
            columns=[self(sa_col) for sa_col in sa_tbl.columns],
            schema_name=sa_tbl.schema,
        )
