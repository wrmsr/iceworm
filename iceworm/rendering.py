from omnibus import dispatch

from . import nodes as no


class Renderer(dispatch.Class):
    render = dispatch.property()

    def render(self, node: no.Node) -> str:  # noqa
        raise TypeError(node)

    def render(self, node: no.Identifier) -> str:  # noqa
        return node.name

    def render(self, node: no.Integer) -> str:  # noqa
        return str(node.value)

    def render(self, node: no.FunctionCall) -> str:  # noqa
        return self.render(node.name) + '(' + ', '.join(self.render(a) for a in node.args) + ')'

    def render(self, node: no.SelectItem) -> str:  # noqa
        return self.render(node.expr) + ((' as ' + self.render(node.label)) if node.label is not None else '')

    def render(self, node: no.Table) -> str:  # noqa
        return self.render(node.name)

    def render(self, node: no.Select) -> str:  # noqa
        return (
                'select ' +
                ', '.join(self.render(i) for i in node.items) +
                ((' from ' + ', '.join(self.render(r) for r in node.relations)) if node.relations else '')
        )

    def render(self, node: no.BinaryExpr) -> str:  # noqa
        return self.render(node.left) + ' ' + node.op.name.lower() + ' ' + self.render(node.right)

    def render(self, node: no.UnaryExpr) -> str:  # noqa
        return node.op.name.lower() + ' ' + self.render(node.value)

    def render(self, node: no.Join) -> str:  # noqa
        return self.render(node.left) + ' join ' + self.render(node.right)


def render(node: no.Node) -> str:
    return Renderer().render(node)
