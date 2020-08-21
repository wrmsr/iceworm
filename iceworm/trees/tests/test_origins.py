from .. import origins
from .. import parsing
from .. import rendering
from .. import symbols
from .. import transforms as tfm
from ... import datatypes as dt
from ... import metadata as md


def test_origins():
    cat = md.Catalog([
        md.Table(['t0'], [
            md.Column('a', dt.Integer()),
            md.Column('b', dt.Integer()),
        ]),
        md.Table(['t1'], [
            md.Column('a', dt.Integer()),
            md.Column('c', dt.Integer()),
        ]),
    ])

    for s in [
        'select t0.a from t0',
        'select 5',
        'select t0.a + 5 from t0',
        'select t0.a + t0.b from t0',
        'select t0.a + t0.b + 5 from t0',
        'select f(t0.a + 1) + t0.b + 2 from t0',
    ]:
        root = parsing.parse_statement(s)
        print(rendering.render(root))

        root = tfm.AliasRelationsTransformer(root)(root)
        root = tfm.LabelSelectItemsTransformer(root)(root)
        root = tfm.ExpandSelectsTransformer(root, cat)(root)
        print(rendering.render(root))

        syms = symbols.analyze(root, cat)
        oris = origins.analyze(root, syms)

        print()

        def rec(v, p):
            print(p + str(v))
            for s in v.srcs:
                rec(s, p + '  ')

        for k, v in oris.exports_by_node_by_name[root].items():
            print(k)
            rec(v, '')

        print()
        print()
