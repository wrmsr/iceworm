import sqlalchemy as sa
import sqlalchemy.sql.elements

from .. import alchemy
from .. import nodes as no


def test_alchemy():
    node = no.Integer(420)
    xlat = alchemy.transmute(node)
    assert isinstance(xlat, sa.sql.elements.BindParameter)
