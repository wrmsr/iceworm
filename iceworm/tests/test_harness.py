"""
TODO:
 - pytest injector scopes:
  - lifecycle callbacks
 - still use pytest for parameterization
 - 'harness' dep?
 - inj mods reg in conftests?
  - watch imports
"""
from _pytest.fixtures import FixtureRequest # noqa
from omnibus import inject as inj
import omnibus.inject.scopes  # noqa
import pytest

from .harness import Harness
from .harness import Scope


def provider():
    def inner(fn):
        def new(cls):
            return fn()
        cls = type(fn.__name__, (), {'__new__': new})
        return cls
    return inner


@provider()
def some_url() -> str:
    return 'a url'


@pytest.mark.xfail()
def test_harness():
    bnd = inj.create_binder()
    bnd.bind(some_url)
    ij = inj.create_injector(bnd)
    assert ij[some_url] == 'a url'
    with pytest.raises(Exception):
        ij[5]  # noqa


def test_harness_2(harness: Harness):
    req: FixtureRequest = harness[inj.Key(FixtureRequest, Scope.FUNCTION)]
    print(req.function)
    req2 = harness[FixtureRequest]
    assert req2 is req
