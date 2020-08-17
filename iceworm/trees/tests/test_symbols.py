from .. import nodes as no
from .. import symbols as syms
from ... import metadata as md


def test_symbols():
    root = no.Select([
        no.ExprSelectItem(
            no.FunctionCallExpr(
                no.FunctionCall(
                    no.QualifiedNameNode.of(['a', 'b'])
                ),
            ),
        ),
    ])
    print(root)

    ana = syms.analyze(root, md.Catalog([]))
    print(ana)
