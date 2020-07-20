from .. import datatypes as dt
from .. import metadata as md
from .. import nodes as no
from .. import transforms as tfm
from ..types import QualifiedName


def test_replace_names():
    root = no.Select([
        no.ExprSelectItem(
            no.FunctionCallExpr(
                no.FunctionCall(
                    no.QualifiedNameNode.of(['a', 'b'])
                ),
            ),
        ),
    ])

    xform = tfm.replace_names(root, {QualifiedName.of_dotted('a.b'): QualifiedName.of_dotted('c.d')})
    print(xform)


def test_expand_selects():
    cat = md.Catalog([
        md.Table('t', [
            md.Column('a', dt.Integer()),
            md.Column('b', dt.Integer()),
        ])
    ])

    root = no.Select(
        [
            no.AllSelectItem(),
        ],
        [
            no.Table(
                no.QualifiedNameNode.of(['t']),
            ),
        ],
    )

    res = tfm.ExpandSelectsTransformer(cat)(root)
    print(res)
