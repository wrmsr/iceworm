"""
TODO:
 - postgres, hive, presto
 - spark? need dialect?
"""
from omnibus import dispatch
import sqlalchemy as sa
import sqlalchemy.sql.elements

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
