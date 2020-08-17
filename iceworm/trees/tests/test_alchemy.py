import sqlalchemy as sa
import sqlalchemy.sql.elements

from .. import alchemy as alch
from .. import nodes as no


def test_alchemy():
    node = no.Integer(420)
    xlat = alch.transmute(node)
    assert isinstance(xlat, sa.sql.elements.BindParameter)
