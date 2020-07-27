from omnibus import lang
import pytest

from .. import nodes as no
from .. import types


def test_cache():
    qn = no.QualifiedNameNode.of(['hi', 'there'])
    assert qn.name == types.QualifiedName(('hi', 'there'))


def test_sealed():
    with pytest.raises(lang.SealedException):
        class Barf(no.Node):  # noqa
            pass
