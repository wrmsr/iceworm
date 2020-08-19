import re


SIMPLE_JINJA_PATTERN = re.compile(r'[A-Za-z_]+')


def is_simple_jinja(buf: str) -> bool:
    return SIMPLE_JINJA_PATTERN.fullmatch(buf) is not None


def test_simple_jinja():
    assert is_simple_jinja('x')
    assert not is_simple_jinja('x[0]')
    assert not is_simple_jinja('x | y')
