"""
TODO:
 - only quote when necessary (for extract)
 - pretty output - no duplication in a pprint.py
  - include comments (reqs carrying antlr into nodes)
"""
import collections.abc
import io
import typing as ta

from omnibus import dataclasses as dc
from omnibus import dispatch

from . import nodes as no
from .quoting import quote


NoneType = type(None)


Part = ta.Union[str, ta.Sequence['Part'], 'DataPart']


class DataPart(dc.Enum):
    pass


class Paren(DataPart):
    part: Part


class List(DataPart):
    parts: ta.Sequence[ta.Optional[Part]]
    delimiter: str = ','


class Concat(DataPart):
    parts: ta.Sequence[Part]


NEEDS_PAREN_TYPES: ta.AbstractSet[ta.Type[no.Node]] = {
    no.BinaryExpr,
    no.IsNull,
    no.SelectExpr,
}


def needs_paren(node: no.Node) -> bool:
    return type(node) in NEEDS_PAREN_TYPES


class Renderer(dispatch.Class):
    render = dispatch.property()

    def render(self, node: NoneType) -> Part:  # noqa
        return []

    def render(self, node: no.Node) -> Part:  # noqa
        raise TypeError(node)

    def paren_render(self, node: no.Node) -> Part:  # noqa
        return Paren(self.render(node)) if needs_paren(node) else self.render(node)

    def render(self, node: no.AliasedRelation) -> Part:  # noqa
        return [
            self.paren_render(node.relation),
            ['as', self.render(node.alias)] if node.alias is not None else [],
            Paren(List([self.render(i) for i in node.columns])) if node.columns else [],
        ]

    def render(self, node: no.AllSelectItem) -> Part:  # noqa
        return '*'

    def render(self, node: no.Between) -> Part:  # noqa
        return [
            self.render(node.value),
            'between',
            self.render(node.lower),
            'and',
            self.render(node.upper),
        ]

    def render(self, node: no.BinaryExpr) -> Part:  # noqa
        return [
            self.paren_render(node.left),
            node.op.value,
            self.paren_render(node.right),
        ]

    def render(self, node: no.Case) -> Part:  # noqa
        return [
            'case',
            self.render(node.value),
            [self.render(i) for i in node.items] if node.items else [],
            ['else', self.render(node.default)] if node.default is not None else [],
            'end',
        ]

    def render(self, node: no.CaseItem) -> Part:  # noqa
        return ['when', self.render(node.when), 'then', self.render(node.then)]

    def render(self, node: no.Cast) -> Part:  # noqa
        return Concat([self.render(node.value), '::', self.render(node.type)])

    def render(self, node: no.CastCall) -> Part:  # noqa
        return Concat(['cast', Paren([self.render(node.value), 'as', self.render(node.type)])])

    def render(self, node: no.Cte) -> Part:  # noqa
        return [self.render(node.name), 'as', Paren(self.render(node.select))]

    def render(self, node: no.CteSelect) -> Part:  # noqa
        return ['with', List([self.render(c) for c in node.ctes]), self.render(node.select)]

    def render(self, node: no.CurrentRowFrameBound) -> Part:  # noqa
        return ['current', 'row']

    def render(self, node: no.Date) -> Part:  # noqa
        return ['date', self.render(node.value)]

    def render(self, node: no.Decimal) -> Part:  # noqa
        return node.value

    def render(self, node: no.DoubleFrame) -> Part:  # noqa
        return [
            node.rows_or_range.value,
            'between',
            self.render(node.min),
            'and',
            self.render(node.max),
        ]

    def render(self, node: no.EFalse) -> Part:  # noqa
        return 'false'

    def render(self, node: no.ETrue) -> Part:  # noqa
        return 'true'

    def render(self, node: no.ExprSelectItem) -> Part:  # noqa
        return [
            self.paren_render(node.value),
            ['as', self.render(node.label)] if node.label is not None else [],
        ]

    def render(self, node: no.Extract) -> Part:  # noqa
        return Concat(['extract', Paren([self.render(node.part), 'from', self.render(node.value)])])

    def render(self, node: no.FlatGrouping) -> Part:  # noqa
        return List([self.render(i) for i in node.items])

    def render(self, node: no.Float) -> Part:  # noqa
        return node.value

    def render(self, node: no.FunctionCall) -> Part:  # noqa
        return Concat([
            self.render(node.name),
            Paren([
                node.set_quantifier.value if node.set_quantifier is not None else [],
                List([self.paren_render(a) for a in [*node.args, *node.kwargs]]),
            ]),
            [node.nulls.value, 'nulls'] if node.nulls is not None else [],
            [
                'within', 'group', Paren([
                    'order', 'by',
                    List([self.render(g) for g in node.within_group])
                ])
            ] if node.within_group else [],
            ['over', Paren([self.render(node.over)])] if node.over is not None else [],
        ])

    def render(self, node: no.FunctionCallExpr) -> Part:  # noqa
        return self.render(node.call)

    def render(self, node: no.FunctionCallRelation) -> Part:  # noqa
        return self.render(node.call)

    def render(self, node: no.GroupingSet) -> Part:  # noqa
        return Paren(List([self.render(i) for i in node.items]))

    def render(self, node: no.Identifier) -> Part:  # noqa
        return quote(node.name, '"')

    def render(self, node: no.IdentifierAllSelectItem) -> Part:  # noqa
        return Concat([self.render(node.identifier), '.*'])

    def render(self, node: no.InJinja) -> Part:  # noqa
        return [
            self.render(node.needle),
            'not' if node.not_ else [], 'in',
            '{{', node.text, '}}',
        ]

    def render(self, node: no.InList) -> Part:  # noqa
        return [
            self.render(node.needle),
            'not' if node.not_ else [], 'in',
            Paren(List([self.paren_render(e) for e in node.haystack])),
        ]

    def render(self, node: no.InSelect) -> Part:  # noqa
        return [
            self.render(node.needle),
            'not' if node.not_ else [], 'in',
            Paren(self.render(node.haystack)),
        ]

    def render(self, node: no.Integer) -> Part:  # noqa
        return str(node.value)

    def render(self, node: no.Interval) -> Part:  # noqa
        return ['interval', self.render(node.value)]

    def render(self, node: no.IsNull) -> Part:  # noqa
        return [self.render(node.value), 'is', 'not' if node.not_ else [], 'null']

    def render(self, node: no.JinjaExpr) -> Part:  # noqa
        return ['{{', node.text, '}}']

    def render(self, node: no.JinjaRelation) -> Part:  # noqa
        return ['{{', node.text, '}}']

    def render(self, node: no.Join) -> Part:  # noqa
        return [
            self.render(node.left),
            node.type.value if node.type != no.JoinType.DEFAULT else [],
            'join',
            self.render(node.right),
            List([
                ['on', self.render(node.condition)] if node.condition is not None else [],
                ['using', Paren(List([self.render(i) for i in node.using]))] if node.using is not None else [],
            ])
        ]

    def render(self, node: no.Kwarg) -> Part:  # noqa
        return [self.render(node.name), '=>', self.render(node.value)]

    def render(self, node: no.Lateral) -> Part:  # noqa
        return ['lateral', self.render(node.relation)]

    def render(self, node: no.Like) -> Part:  # noqa
        return [
            self.render(node.value),
            (' not' if node.not_ else ''),
            node.kind.value,
            ['any', Paren(List([self.render(p) for p in node.patterns]))]
            if len(node.patterns) != 1 else self.render(next(iter(node.patterns))),
            ['escape', self.render(node.escape)] if node.escape is not None else [],
        ]

    def render(self, node: no.Null) -> Part:  # noqa
        return 'null'

    def render(self, node: no.NumFrameBound) -> Part:  # noqa
        return [str(node.num), node.precedence.value]

    def render(self, node: no.Over) -> Part:  # noqa
        return [
            ['partition', 'by', List([self.render(e) for e in node.partition_by])] if node.partition_by else [],
            ['order', 'by', List([self.render(e) for e in node.order_by])] if node.order_by else [],
            self.render(node.frame),
        ]

    def render(self, node: no.Pivot) -> Part:  # noqa
        return [
            self.render(node.relation),
            Concat(['pivot', Paren([
                self.render(node.func),
                Paren(self.render(node.pivot_col)),
                'for',
                self.render(node.value_col),
                'in',
                Paren(List([self.render(e) for e in node.values])),
            ])]),
        ]

    def render(self, node: no.QualifiedNameNode) -> Part:  # noqa
        return '.'.join(self.render(i) for i in node.parts)

    def render(self, node: no.Select) -> Part:  # noqa
        return [
            'select',
            ['top', self.render(node.top_n)] if node.top_n is not None else [],
            node.set_quantifier.value if node.set_quantifier is not None else [],
            List([self.render(i) for i in node.items]),
            ['from', List([self.paren_render(r) for r in node.relations])] if node.relations else [],
            ['where', self.render(node.where)] if node.where is not None else [],
            ['group', 'by', self.render(node.group_by)] if node.group_by is not None else [],
            ['having', self.render(node.having)] if node.having is not None else [],
            ['qualify', self.render(node.qualify)] if node.qualify is not None else [],
            ['order', 'by', List([self.render(e) for e in node.order_by])] if node.order_by else [],
            ['limit', str(node.limit)] if node.limit is not None else [],
        ]

    def render(self, node: no.SelectExpr) -> Part:  # noqa
        return self.render(node.select)

    def render(self, node: no.SelectRelation) -> Part:  # noqa
        return Paren(self.render(node.select))

    def render(self, node: no.SetsGrouping) -> Part:  # noqa
        return ['grouping', 'sets', Paren(List([self.render(i) for i in node.sets]))]

    def render(self, node: no.SingleFrame) -> Part:  # noqa
        return [node.rows_or_range.value, self.render(node.bound)]

    def render(self, node: no.SortItem) -> Part:  # noqa
        return [
            self.render(node.value),
            node.direction.value if node.direction is not None else [],
            ['nulls', node.nulls.value] if node.nulls is not None else [],
        ]

    def render(self, node: no.StarExpr) -> Part:  # noqa
        return '*'

    def render(self, node: no.String) -> Part:  # noqa
        return quote(node.value, "'")

    def render(self, node: no.Table) -> Part:  # noqa
        return self.render(node.name)

    def render(self, node: no.TypeSpec) -> Part:  # noqa
        return [
            self.render(node.name),
            Paren(List([self.render(a) for a in node.args])) if node.args else [],
        ]

    def render(self, node: no.UnaryExpr) -> Part:  # noqa
        return [node.op.value, self.paren_render(node.value)]

    def render(self, node: no.UnboundedFrameBound) -> Part:  # noqa
        return ['unbounded', node.precedence.value]

    def render(self, node: no.SetSelect) -> Part:  # noqa
        return [
            self.render(node.left),
            [self.render(i) for i in node.items] if node.items else [],
        ]

    def render(self, node: no.SetSelectItem) -> Part:  # noqa
        return [
            node.kind.value,
            node.set_quantifier.value if node.set_quantifier is not None else [],
            self.render(node.right),
        ]

    def render(self, node: no.Unpivot) -> Part:  # noqa
        return [
            self.render(node.relation),
            Concat(['unpivot', Paren([
                self.render(node.value_col),
                'for',
                self.render(node.name_col),
                'in',
                Paren(List([self.render(c) for c in node.pivot_cols])),
            ])]),
        ]

    def render(self, node: no.Traversal) -> Part:  # noqa
        return Concat([
            self.render(node.value),
            ':',
            *[
                ('[' + r + ']') if isinstance(k, no.Integer) else (('.' if i else '') + r)
                for i, k in enumerate(node.keys)
                for r in [self.render(k)]
            ],
        ])


def render_part(part: Part, buf: io.StringIO) -> None:
    if isinstance(part, str):
        buf.write(part)
    elif isinstance(part, collections.abc.Sequence):
        raise NotImplementedError
    elif isinstance(part, Paren):
        raise NotImplementedError
    elif isinstance(part, List):
        raise NotImplementedError
    elif isinstance(part, Concat):
        raise NotImplementedError
    else:
        raise TypeError(part)


def render(node: no.Node) -> str:
    part = Renderer().render(node)
    buf = io.StringIO()
    render_part(part, buf)
    return buf.getvalue()
