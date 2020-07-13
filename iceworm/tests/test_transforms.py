import pytest

from .. import nodes as no
from .. import transforms as tfm


@pytest.mark.xfail()
def test_replace_names():
    root = no.Select([
        no.FunctionCall(
            no.QualifiedNameNode.of(['a', 'b'])
        )
    ])

    xform = tfm.replace_names(root, {})
    print(xform)
