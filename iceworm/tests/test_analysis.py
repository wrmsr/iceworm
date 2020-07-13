import pytest

from .. import analysis as ana
from .. import nodes as no


@pytest.mark.xfail()
def test_names():
    root = no.Select([
        no.FunctionCall(
            no.QualifiedNameNode.of('a', 'b')
        )
    ])

    basic = ana.basic(root)
    print(basic.get_node_type_set(no.QualifiedNameNode))
