from omnibus import lang
from omnibus import dataclasses as dc
import pytest

from .. import nodes as no
from ... import types


def test_cache():
    qn = no.QualifiedNameNode.of(['hi', 'there'])
    assert qn.name == types.QualifiedName(('hi', 'there'))


def test_sealed():
    with pytest.raises(lang.SealedException):
        class Barf(no.Node):  # noqa
            pass


def test_checks():
    no.AliasedRelation(
        no.Table(
            no.QualifiedNameNode.of(['t'])),
        no.Identifier('t'))

    with pytest.raises(dc.CheckException):
        no.AliasedRelation(
            no.AliasedRelation(
                no.Table(
                    no.QualifiedNameNode.of(['t'])),
                no.Identifier('t')),
            no.Identifier('t'))
