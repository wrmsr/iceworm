from omnibus import dispatch
import sqlalchemy as sa
import sqlalchemy.sql.elements

from . import nodes as no


class Transmuter(dispatch.Class):
    transmute = dispatch.property()

    def transmute(self, node: no.Node) -> sa.sql.elements.Visitable:  # noqa
        raise TypeError(node)

    def transmute(self, node: no.Integer) -> sa.sql.elements.Visitable:  # noqa
        return sa.literal(node.value)


def transmute(node: no.Node) -> sa.sql.elements.Visitable:
    return Transmuter().transmute(node)
