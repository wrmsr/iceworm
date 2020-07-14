import typing as ta

from omnibus import dispatch

from . import nodes as no
from .quoting import quote


def paren(s: str) -> str:
    return '(' + s + ')'


NEEDS_PAREN_TYPES: ta.AbstractSet[ta.Type[no.Node]] = {
    no.BinaryExpr,
    no.IsNull,
    no.SelectExpr,
}


def needs_paren(node: no.Node) -> bool:
    return type(node) in NEEDS_PAREN_TYPES


class Renderer(dispatch.Class):
    render = dispatch.property()

    def render(self, node: no.Node) -> str:  # noqa
        raise TypeError(node)

    def paren_render(self, node: no.Node) -> str:  # noqa
        return paren(self.render(node)) if needs_paren(node) else self.render(node)

    def render(self, node: no.AliasedRelation) -> str:  # noqa
        return (
                self.paren_render(node.relation) +
                ((' as ' + self.render(node.alias)) if node.alias is not None else '')
        )

    def render(self, node: no.AllSelectItem) -> str:  # noqa
        return '*'

    def render(self, node: no.BinaryExpr) -> str:  # noqa
        return self.paren_render(node.left) + ' ' + node.op.value + ' ' + self.paren_render(node.right)

    def render(self, node: no.Case) -> str:  # noqa
        return (
                'case' +
                ((' ' + self.render(node.value)) if node.value is not None else '') +
                ((' ' + ' '.join(self.render(i) for i in node.items)) if node.items else '') +
                ((' else ' + self.render(node.default)) if node.default is not None else '') +
                ' end'
        )

    def render(self, node: no.CaseItem) -> str:  # noqa
        return 'when ' + self.render(node.when) + ' then ' + self.render(node.then)

    def render(self, node: no.Cast) -> str:  # noqa
        return self.render(node.value) + ' :: ' + self.render(node.type)

    def render(self, node: no.Cte) -> str:  # noqa
        return self.render(node.name) + ' as ' + paren(self.render(node.select))

    def render(self, node: no.CteSelect) -> str:  # noqa
        return 'with ' + ', '.join(self.render(c) for c in node.ctes) + ' ' + self.render(node.select)

    def render(self, node: no.Decimal) -> str:  # noqa
        return node.value

    def render(self, node: no.EFalse) -> str:  # noqa
        return 'false'

    def render(self, node: no.ETrue) -> str:  # noqa
        return 'true'

    def render(self, node: no.ExprSelectItem) -> str:  # noqa
        return self.paren_render(node.value) + ((' as ' + self.render(node.label)) if node.label is not None else '')

    def render(self, node: no.Float) -> str:  # noqa
        return node.value

    def render(self, node: no.FunctionCall) -> str:  # noqa
        return (
                self.render(node.name) +
                paren(', '.join(self.paren_render(a) for a in [*node.args, *node.kwargs])) +
                ((' over ' + paren(self.render(node.over))) if node.over is not None else '')
        )

    def render(self, node: no.FunctionCallExpr) -> str:  # noqa
        return self.render(node.call)

    def render(self, node: no.FunctionCallRelation) -> str:  # noqa
        return self.render(node.call)

    def render(self, node: no.GroupBy) -> str:  # noqa
        return ', '.join(self.render(i) for i in node.items)

    def render(self, node: no.GroupItem) -> str:  # noqa
        return self.render(node.value)

    def render(self, node: no.Identifier) -> str:  # noqa
        return quote(node.name, '"')

    def render(self, node: no.IdentifierAllSelectItem) -> str:  # noqa
        return self.render(node.identifier) + '.*'

    def render(self, node: no.Ilike) -> str:  # noqa
        return (
                self.render(node.value) +
                (' not' if node.not_ else '') +
                ' ilike ' +
                self.render(node.pattern)
        )

    def render(self, node: no.InJinja) -> str:  # noqa
        return (
                self.render(node.needle) +
                (' not' if node.not_ else '') +
                ' in {{ ' +
                node.text +
                ' }}'
        )

    def render(self, node: no.InList) -> str:  # noqa
        return (
                self.render(node.needle) +
                (' not' if node.not_ else '') +
                ' in ' +
                paren(', '.join(self.paren_render(e) for e in node.haystack))
        )

    def render(self, node: no.InSelect) -> str:  # noqa
        return (
            self.render(node.needle) +
            (' not' if node.not_ else '') +
            ' in ' +
            paren(self.render(node.haystack))
        )

    def render(self, node: no.Integer) -> str:  # noqa
        return str(node.value)

    def render(self, node: no.IsNull) -> str:  # noqa
        return self.render(node.value) + ' is ' + ('not ' if node.not_ else '') + 'null'

    def render(self, node: no.JinjaExpr) -> str:  # noqa
        return '{{ ' + node.text + '}}'

    def render(self, node: no.JinjaRelation) -> str:  # noqa
        return '{{ ' + node.text + '}}'

    def render(self, node: no.Join) -> str:  # noqa
        return (
                self.render(node.left) +
                ' ' +
                ((node.type.value + ' ') if node.type != no.JoinType.DEFAULT else '') +
                'join ' +
                self.render(node.right) +
                ((' on ' + self.render(node.condition)) if node.condition is not None else '')
        )

    def render(self, node: no.Kwarg) -> str:  # noqa
        return self.render(node.name) + ' => ' + self.render(node.value)

    def render(self, node: no.Lateral) -> str:  # noqa
        return 'lateral ' + self.render(node.relation)

    def render(self, node: no.Like) -> str:  # noqa
        return (
                self.render(node.value) +
                (' not' if node.not_ else '') +
                ' like ' +
                self.render(node.pattern)
        )

    def render(self, node: no.Null) -> str:  # noqa
        return 'null'

    def render(self, node: no.Over) -> str:  # noqa
        return (
                (('partition by ' + self.render(node.partition_by)) if node.partition_by is not None else '') +
                (('order by ' + ', '.join(self.render(e) for e in node.order_by)) if node.order_by else '')
        )

    def render(self, node: no.Pivot) -> str:  # noqa
        return (
                self.render(node.relation) +
                ' pivot(' +
                self.render(node.func) +
                '(' +
                self.render(node.pivot_col) +
                ') for ' +
                self.render(node.value_col) +
                ' in (' +
                ', '.join(self.render(e) for e in node.values) +
                '))'
        )

    def render(self, node: no.QualifiedNameNode) -> str:  # noqa
        return '.'.join(self.render(i) for i in node.parts)

    def render(self, node: no.Select) -> str:  # noqa
        return (
                'select ' +
                (('top ' + self.render(node.top_n) + ' ') if node.top_n is not None else '') +
                ((node.set_quantifier.value + ' ') if node.set_quantifier is not None else '') +
                ', '.join(self.render(i) for i in node.items) +
                ((' from ' + ', '.join(self.paren_render(r) for r in node.relations)) if node.relations else '') +
                ((' where ' + self.render(node.where)) if node.where is not None else '') +
                ((' group by ' + self.render(node.group_by)) if node.group_by is not None else '') +
                ((' having ' + self.render(node.having)) if node.having is not None else '') +
                ((' order by ' + ', '.join(self.render(e) for e in node.order_by)) if node.order_by else '')
        )

    def render(self, node: no.SelectExpr) -> str:  # noqa
        return self.render(node.select)

    def render(self, node: no.SelectRelation) -> str:  # noqa
        return paren(self.render(node.select))

    def render(self, node: no.SortItem) -> str:  # noqa
        return self.render(node.value) + ((' ' + node.direction.value) if node.direction is not None else '')

    def render(self, node: no.StarExpr) -> str:  # noqa
        return '*'

    def render(self, node: no.String) -> str:  # noqa
        return quote(node.value, "'")

    def render(self, node: no.Table) -> str:  # noqa
        return self.render(node.name)

    def render(self, node: no.UnaryExpr) -> str:  # noqa
        return node.op.value + ' ' + self.paren_render(node.value)

    def render(self, node: no.UnionItem) -> str:  # noqa
        return (
                'union ' +
                ((node.set_quantifier.value + ' ') if node.set_quantifier is not None else '') +
                self.render(node.right)
        )

    def render(self, node: no.UnionSelect) -> str:  # noqa
        return (
                self.render(node.left) +
                ((' ' + ' '.join(self.render(i) for i in node.items)) if node.items else '')
        )

    def render(self, node: no.Unpivot) -> str:  # noqa
        return (
                self.render(node.relation) +
                ' unpivot(' +
                self.render(node.value_col) +
                ' for ' +
                self.render(node.name_col) +
                ' in (' +
                ', '.join(self.render(c) for c in node.pivot_cols) +
                '))'
        )


def render(node: no.Node) -> str:
    return Renderer().render(node)
