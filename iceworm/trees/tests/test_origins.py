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
    ]:
        root = parsing.parse_statement(s)
        print(rendering.render(root))

        root = tfm.AliasRelationsTransformer(root)(root)
        root = tfm.LabelSelectItemsTransformer(root)(root)
        root = tfm.ExpandSelectsTransformer(root, cat)(root)
        print(rendering.render(root))

        syms = symbols.analyze(root, cat)
        oris = origins.analyze(root, syms)
        print(oris)
