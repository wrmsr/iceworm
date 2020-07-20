"""
TODO:
 - postgres, hive, presto
 - spark? need dialect?
"""
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


class MetadataAdapter(dispatch.Class):
    from_sa = dispatch.property()
    to_sa = dispatch.property()

    def from_sa(self, sa_type: sa.sql.sqltypes.TypeEngine) -> dt.Datatype:  # noqa
        if isinstance(sa_type, sa.Integer):
            return dt.Integer()
        else:
            raise TypeError(sa_type)

    def from_sa(self, sa_col: sa.Column) -> md.Column:  # noqa
        return md.Column(
            name=sa_col.name,
            type=self.from_sa(sa_col.type),
        )

    def from_sa(self, sa_tbl: sa.Table) -> md.Table:  # noqa
        return md.Table(
            name=sa_tbl.name,
            columns=[self.from_sa(sa_col) for sa_col in sa_tbl.columns],
            schema=sa_tbl.schema,
        )


METADATA_ADAPTER = MetadataAdapter()

from_metadata = METADATA_ADAPTER.to_sa
to_metadata = METADATA_ADAPTER.from_sa
