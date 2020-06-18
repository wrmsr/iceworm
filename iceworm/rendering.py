from omnibus import dispatch

from . import nodes as no
from .quoting import quote


def paren(s: str) -> str:
    return '(' + s + ')'


class Renderer(dispatch.Class):
    render = dispatch.property()

    def render(self, node: no.Node) -> str:  # noqa
        raise TypeError(node)

    def render(self, node: no.AllSelectItem) -> str:  # noqa
        return '*'

    def render(self, node: no.BinaryExpr) -> str:  # noqa
        return paren(self.render(node.left)) + ' ' + node.op.value + ' ' + paren(self.render(node.right))

    def render(self, node: no.ExprSelectItem) -> str:  # noqa
        return paren(self.render(node.expr)) + ((' as ' + self.render(node.label)) if node.label is not None else '')

    def render(self, node: no.FunctionCall) -> str:  # noqa
        return self.render(node.name) + '(' + ', '.join(paren(self.render(a)) for a in node.args) + ')'

    def render(self, node: no.GroupBy) -> str:  # noqa
        return ', '.join(paren(self.render(e)) for e in node.exprs)

    def render(self, node: no.Identifier) -> str:  # noqa
        return quote(node.name, '"')

    def render(self, node: no.Integer) -> str:  # noqa
        return str(node.value)

    def render(self, node: no.Join) -> str:  # noqa
        return (
                self.render(node.left) +
                ' join ' +
                self.render(node.right) +
                ((' on ' + self.render(node.condition)) if node.condition is not None else '')
        )

    def render(self, node: no.Null) -> str:  # noqa
        return 'null'

    def render(self, node: no.Select) -> str:  # noqa
        return (
                'select ' +
                ', '.join(self.render(i) for i in node.items) +
                ((' from ' + ', '.join(self.render(r) for r in node.relations)) if node.relations else '') +
                ((' where ' + self.render(node.where)) if node.where is not None else '') +
                ((' group by ' + self.render(node.group_by)) if node.group_by is not None else '')
        )

    def render(self, node: no.String) -> str:  # noqa
        return quote(node.value, "'")

    def render(self, node: no.Table) -> str:  # noqa
        return self.render(node.name)

    def render(self, node: no.UnaryExpr) -> str:  # noqa
        return node.op.value + ' ' + paren(self.render(node.value))


def render(node: no.Node) -> str:
    return Renderer().render(node)
