"""
TODO:
 - SandboxedEnvironment? worthless?
 - ugh, LINE NUMBERS
 - SortedMapping[int, int] ? :/
 - also need to feed to serde
 - ugh, escape helper? {{ user.username|e }} - better if it’s not there?
 - lol, yaml jinja? :|
  - * line tracking there too lol *
 - extensions: jinja, j2
"""
import re

import jinja2


SIMPLE_JINJA_PATTERN = re.compile(r'[A-Za-z_]+')


def is_simple_jinja(buf: str) -> bool:
    return SIMPLE_JINJA_PATTERN.fullmatch(buf) is not None


class StrictEnvironment(jinja2.Environment):

    def getitem(self, obj, argument):
        try:
            return obj[argument]
        except (AttributeError, TypeError, LookupError):
            return self.undefined(obj=obj, name=argument)

    def getattr(self, obj, attribute):
        try:
            return getattr(obj, attribute)
        except AttributeError:
            return self.undefined(obj=obj, name=attribute)


def test_simple_jinja():
    assert is_simple_jinja('x')
    assert not is_simple_jinja('x[0]')
    assert not is_simple_jinja('x | y')


def test_rendering():
    tmpl = jinja2.Template('{%- macro hi(foo) -%} hi {{ foo -}}{% endmacro -%} {{ hi(x) }}')
    assert tmpl.render(x=1)
