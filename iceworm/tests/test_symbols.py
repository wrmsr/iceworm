from .. import nodes as no
from .. import symbols as syms


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

    root_scope = syms.SymbolScope(root)
    print(syms._Analyzer()(root, root_scope))
