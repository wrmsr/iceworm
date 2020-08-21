from .. import nodes as no
from .. import origins
from .. import parsing
from .. import rendering
from .. import symbols
from .. import transforms as tfm
from ... import datatypes as dt
from ... import metadata as md
from ...types import QualifiedName


def test_replace_names():
    root = no.Select([
        no.ExprSelectItem(
            no.FunctionCallExpr(
                no.FunctionCall(
                    no.QualifiedNameNode.of(['a', 'b'])))),
    ])

    xform = tfm.replace_names(root, {QualifiedName.of_dotted('a.b'): QualifiedName.of_dotted('c.d')})
    print(xform)


def test_expand_selects():
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
        'select * from t0',
        'select * from t1',
        'select * from t0, t1',
    ]:
        root = parsing.parse_statement(s)

        print(rendering.render(root))

        root = tfm.AliasRelationsTransformer(root)(root)
        root = tfm.LabelSelectItemsTransformer(root)(root)
        root = tfm.ExpandSelectsTransformer(root, cat)(root)
        print(root)

        print(rendering.render(root))

        syms = symbols.analyze(root, cat)
        print(syms)
        print(syms.resolutions)

        oris = origins.analyze(root, syms)
        print(oris)

        print()

        for k, v in oris.exports_by_node_by_name[root].items():
            print(k)
            while True:
                print(v)
                if isinstance(v, origins.Leaf):
                    break
                v = v.src
            print()

        print()
