"""
TODO:
 - pytest injector scopes: function, class, module, package, session
  - lifecycle callbacks
 - still use pytest for parameterization
 - 'harness' dep?
 - inj mods reg in conftests?
  - watch imports
"""
from omnibus import inject as inj
import pytest


def provider():
    def inner(fn):
        def new(cls):
            return fn()
        cls = type(fn.__name__, (), {'__new__': new})
        return cls
    return inner


@provider()
def some_url():
    return 'a url'


@pytest.mark.xfail()
def test_harness():
    bnd = inj.create_binder()
    bnd.bind(some_url)
    ij = inj.create_injector(bnd)
    assert ij[some_url] == 'a url'
    with pytest.raises(Exception):
        ij[5]  # noqa
