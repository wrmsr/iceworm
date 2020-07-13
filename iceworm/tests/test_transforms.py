from .. import nodes as no
from .. import transforms as tfm
from ..types import QualifiedName


def test_replace_names():
    root = no.Select([
        no.ExprSelectItem(
            no.FunctionCall(
                no.QualifiedNameNode.of(['a', 'b'])
            ),
        ),
    ])

    xform = tfm.replace_names(root, {QualifiedName.of_dotted('a.b'): QualifiedName.of_dotted('c.d')})
    print(xform)
