import sqlalchemy as sa

from ... import sql


def test_col_aliases():
    t = sa.table('t')
    at = sql.column_list_alias(t, 'barf', ['a'])
    stmt = sa.select('*').select_from(at)
    assert str(stmt).split() == 'SELECT * FROM t AS barf(a)'.split()
