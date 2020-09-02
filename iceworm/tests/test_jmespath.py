import collections.abc
import dataclasses as dc

import jmespath as jp


@dc.dataclass(frozen=True)
class Foo:
    bar: str


class ObjInterp(jp.visitor.TreeInterpreter):

    def visit_field(self, node, value):
        if isinstance(value, collections.abc.Mapping):
            return value.get(node['value'])
        else:
            return getattr(value, node['value'], None)


def test_jmespath():
    print(jp.search('foo.bar', {'foo': {'bar': 'baz'}}))

    expr = 'foo.bar'
    data = {'foo': Foo('baz')}
    pr = jp.parser.Parser().parse(expr)
    interp = ObjInterp()
    res = interp.visit(pr.parsed, data)
    print(res)
