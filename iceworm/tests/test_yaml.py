from omnibus.serde.objects import yaml as oyaml
import pytest
import yaml.scanner


def test_yaml():
    good = """
a:
  b: 0
  c: 1
a:
  b: 0
  c: 1
a:
  b: 0
  c: 1
a:
  b: 0
  c: 1
a:
  b: 0
  c: 1
    """

    bad = good + """
bad:
  a: b: 1
    """

    with pytest.raises(yaml.scanner.ScannerError):
        print(yaml.safe_load(bad))

    loader = oyaml.WrappedLoaders.base(good)
    vals = []
    try:
        while loader.check_data():
            vals.append(loader.get_data())
    finally:
        loader.dispose()
    print(vals)
