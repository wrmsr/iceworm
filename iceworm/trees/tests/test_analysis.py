from .. import analysis as ana
from .. import nodes as no


def test_names():
    root = no.Select([
        no.ExprSelectItem(
            no.FunctionCallExpr(
                no.FunctionCall(
                    no.QualifiedNameNode.of(['a', 'b'])
                ),
            ),
        ),
    ])

    basic = ana.basic(root)
    print(basic.get_node_type_set(no.QualifiedNameNode))
    assert basic.parents_by_node
