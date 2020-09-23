from omnibus import lang
from omnibus.dev.testing.helpers import skip_if_cant_import
from omnibus.serde.objects import yaml as oyaml


@skip_if_cant_import('_yaml')
def test_cyaml():
    src = """
x: 1
    """

    with lang.disposing(oyaml.WrappedLoaders.cbase(src)) as loader:
        assert loader.check_data()
        node = loader.get_data()
        assert node is not None
