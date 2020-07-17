from .. import nodes as no
from .. import types


def test_cache():
    qn = no.QualifiedNameNode.of(['hi', 'there'])
    assert qn.name == types.QualifiedName(('hi', 'there'))
