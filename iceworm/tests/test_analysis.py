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

    dct = ana.collect_name_references(root)
    print(dct)
