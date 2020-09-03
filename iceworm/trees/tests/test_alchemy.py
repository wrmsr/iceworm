import sqlalchemy as sa
import sqlalchemy.sql.elements

from .. import alchemy as alch
from .. import nodes as no
from .. import parsing as par


def test_alchemy():
    node = no.Integer(420)
    xlat = alch.transmute(node)
    assert isinstance(xlat, sa.sql.elements.BindParameter)

    for query in [
        'select 1',
        'select * from barf',
        'select * from a join b',
        'select * from a join b where 1',
        'select * from a join b where a.b',
        'select * from a join b where a.b and 2',
        'select * from a join b where a.b and 2 > 3',
    ]:
        print(query)
        stmt = alch.transmute(par.parse_statement(query + ';'))
        print(stmt)
        print()
