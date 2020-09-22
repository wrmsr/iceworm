from omnibus import lang
from omnibus.serde.objects import yaml as oyaml
import pytest


@pytest.mark.xfail
def test_cyaml():
    src = """
x: 1
    """

    with lang.disposing(oyaml.WrappedLoaders.cbase(src)) as loader:
        assert loader.check_data()
        node = loader.get_data()
        assert node is not None
