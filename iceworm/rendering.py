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


T = ta.TypeVar('T')
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
    __call__ = dispatch.property()

    def __call__(self, node: NoneType) -> Part:  # noqa
        return []

    def __call__(self, node: no.Node) -> Part:  # noqa
        raise TypeError(node)

    def paren(self, node: no.Node) -> Part:  # noqa
        return Paren(self(node)) if needs_paren(node) else self(node)

    def __call__(self, node: no.AliasedRelation) -> Part:  # noqa
        return [
            self.paren(node.relation),
            ['as', self(node.alias)] if node.alias is not None else [],
            Paren(List([self(i) for i in node.columns])) if node.columns else [],
        ]

    def __call__(self, node: no.AllSelectItem) -> Part:  # noqa
        return '*'

    def __call__(self, node: no.Between) -> Part:  # noqa
        return [
            self(node.value),
            'between',
            self(node.lower),
            'and',
            self(node.upper),
        ]

    def __call__(self, node: no.BinaryExpr) -> Part:  # noqa
        return [
            self.paren(node.left),
            node.op.value,
            self.paren(node.right),
        ]

    def __call__(self, node: no.Case) -> Part:  # noqa
        return [
            'case',
            self(node.value),
            [self(i) for i in node.items] if node.items else [],
            ['else', self(node.default)] if node.default is not None else [],
            'end',
        ]

    def __call__(self, node: no.CaseItem) -> Part:  # noqa
        return ['when', self(node.when), 'then', self(node.then)]

    def __call__(self, node: no.Cast) -> Part:  # noqa
        return Concat([self(node.value), '::', self(node.type)])

    def __call__(self, node: no.CastCall) -> Part:  # noqa
        return Concat(['cast', Paren([self(node.value), 'as', self(node.type)])])

    def __call__(self, node: no.Cte) -> Part:  # noqa
        return [self(node.name), 'as', Paren(self(node.select))]

    def __call__(self, node: no.CteSelect) -> Part:  # noqa
        return ['with', List([self(c) for c in node.ctes]), self(node.select)]

    def __call__(self, node: no.CurrentRowFrameBound) -> Part:  # noqa
        return ['current', 'row']

    def __call__(self, node: no.Date) -> Part:  # noqa
        return ['date', self(node.value)]

    def __call__(self, node: no.Decimal) -> Part:  # noqa
        return node.value

    def __call__(self, node: no.DoubleFrame) -> Part:  # noqa
        return [
            node.rows_or_range.value,
            'between',
            self(node.min),
            'and',
            self(node.max),
        ]

    def __call__(self, node: no.EFalse) -> Part:  # noqa
        return 'false'

    def __call__(self, node: no.ETrue) -> Part:  # noqa
        return 'true'

    def __call__(self, node: no.ExprSelectItem) -> Part:  # noqa
        return [
            self.paren(node.value),
            ['as', self(node.label)] if node.label is not None else [],
        ]

    def __call__(self, node: no.Extract) -> Part:  # noqa
        return Concat(['extract', Paren([self(node.part), 'from', self(node.value)])])

    def __call__(self, node: no.FlatGrouping) -> Part:  # noqa
        return List([self(i) for i in node.items])

    def __call__(self, node: no.Float) -> Part:  # noqa
        return node.value

    def __call__(self, node: no.FunctionCall) -> Part:  # noqa
        return [
            Concat([
                self(node.name),
                Paren([
                    node.set_quantifier.value if node.set_quantifier is not None else [],
                    List([self.paren(a) for a in [*node.args, *node.kwargs]]),
                ]),
            ]),
            [node.nulls.value, 'nulls'] if node.nulls is not None else [],
            [
                'within', 'group', Paren([
                    'order', 'by',
                    List([self(g) for g in node.within_group])
                ])
            ] if node.within_group else [],
            ['over', Paren([self(node.over)])] if node.over is not None else [],
        ]

    def __call__(self, node: no.FunctionCallExpr) -> Part:  # noqa
        return self(node.call)

    def __call__(self, node: no.FunctionCallRelation) -> Part:  # noqa
        return self(node.call)

    def __call__(self, node: no.GroupingSet) -> Part:  # noqa
        return Paren(List([self(i) for i in node.items]))

    def __call__(self, node: no.Identifier) -> Part:  # noqa
        return quote(node.name, '"')

    def __call__(self, node: no.IdentifierAllSelectItem) -> Part:  # noqa
        return Concat([self(node.identifier), '.*'])

    def __call__(self, node: no.InJinja) -> Part:  # noqa
        return [
            self(node.needle),
            'not' if node.not_ else [], 'in',
            '{{', node.text, '}}',
        ]

    def __call__(self, node: no.InList) -> Part:  # noqa
        return [
            self(node.needle),
            'not' if node.not_ else [], 'in',
            Paren(List([self.paren(e) for e in node.haystack])),
        ]

    def __call__(self, node: no.InSelect) -> Part:  # noqa
        return [
            self(node.needle),
            'not' if node.not_ else [], 'in',
            Paren(self(node.haystack)),
        ]

    def __call__(self, node: no.Integer) -> Part:  # noqa
        return str(node.value)

    def __call__(self, node: no.Interval) -> Part:  # noqa
        return ['interval', self(node.value)]

    def __call__(self, node: no.IsNull) -> Part:  # noqa
        return [self(node.value), 'is', 'not' if node.not_ else [], 'null']

    def __call__(self, node: no.JinjaExpr) -> Part:  # noqa
        return ['{{', node.text, '}}']

    def __call__(self, node: no.JinjaRelation) -> Part:  # noqa
        return ['{{', node.text, '}}']

    def __call__(self, node: no.Join) -> Part:  # noqa
        return [
            self(node.left),
            node.type.value if node.type != no.JoinType.DEFAULT else [],
            'join',
            self(node.right),
            List([
                ['on', self(node.condition)] if node.condition is not None else [],
                ['using', Paren(List([self(i) for i in node.using]))] if node.using is not None else [],
            ])
        ]

    def __call__(self, node: no.Kwarg) -> Part:  # noqa
        return [self(node.name), '=>', self(node.value)]

    def __call__(self, node: no.Lateral) -> Part:  # noqa
        return ['lateral', self(node.relation)]

    def __call__(self, node: no.Like) -> Part:  # noqa
        return [
            self(node.value),
            'not' if node.not_ else [],
            node.kind.value,
            ['any', Paren(List([self(p) for p in node.patterns]))]
            if len(node.patterns) != 1 else self(next(iter(node.patterns))),
            ['escape', self(node.escape)] if node.escape is not None else [],
        ]

    def __call__(self, node: no.Null) -> Part:  # noqa
        return 'null'

    def __call__(self, node: no.NumFrameBound) -> Part:  # noqa
        return [str(node.num), node.precedence.value]

    def __call__(self, node: no.Over) -> Part:  # noqa
        return [
            ['partition', 'by', List([self(e) for e in node.partition_by])] if node.partition_by else [],
            ['order', 'by', List([self(e) for e in node.order_by])] if node.order_by else [],
            self(node.frame),
        ]

    def __call__(self, node: no.Pivot) -> Part:  # noqa
        return [
            self(node.relation),
            Concat(['pivot', Paren([
                self(node.func),
                Paren(self(node.pivot_col)),
                'for',
                self(node.value_col),
                'in',
                Paren(List([self(e) for e in node.values])),
            ])]),
        ]

    def __call__(self, node: no.QualifiedNameNode) -> Part:  # noqa
        return '.'.join(self(i) for i in node.parts)

    def __call__(self, node: no.Select) -> Part:  # noqa
        return [
            'select',
            ['top', self(node.top_n)] if node.top_n is not None else [],
            node.set_quantifier.value if node.set_quantifier is not None else [],
            List([self(i) for i in node.items]),
            ['from', List([self.paren(r) for r in node.relations])] if node.relations else [],
            ['where', self(node.where)] if node.where is not None else [],
            ['group', 'by', self(node.group_by)] if node.group_by is not None else [],
            ['having', self(node.having)] if node.having is not None else [],
            ['qualify', self(node.qualify)] if node.qualify is not None else [],
            ['order', 'by', List([self(e) for e in node.order_by])] if node.order_by else [],
            ['limit', str(node.limit)] if node.limit is not None else [],
        ]

    def __call__(self, node: no.SelectExpr) -> Part:  # noqa
        return self(node.select)

    def __call__(self, node: no.SelectRelation) -> Part:  # noqa
        return Paren(self(node.select))

    def __call__(self, node: no.SetsGrouping) -> Part:  # noqa
        return ['grouping', 'sets', Paren(List([self(i) for i in node.sets]))]

    def __call__(self, node: no.SingleFrame) -> Part:  # noqa
        return [node.rows_or_range.value, self(node.bound)]

    def __call__(self, node: no.SortItem) -> Part:  # noqa
        return [
            self(node.value),
            node.direction.value if node.direction is not None else [],
            ['nulls', node.nulls.value] if node.nulls is not None else [],
        ]

    def __call__(self, node: no.StarExpr) -> Part:  # noqa
        return '*'

    def __call__(self, node: no.String) -> Part:  # noqa
        return quote(node.value, "'")

    def __call__(self, node: no.Table) -> Part:  # noqa
        return self(node.name)

    def __call__(self, node: no.TypeSpec) -> Part:  # noqa
        return [
            self(node.name),
            Paren(List([self(a) for a in node.args])) if node.args else [],
        ]

    def __call__(self, node: no.UnaryExpr) -> Part:  # noqa
        parts = [node.op.value, self.paren(node.value)]
        return Concat(parts) if node.op != no.UnaryOp.NOT else parts

    def __call__(self, node: no.UnboundedFrameBound) -> Part:  # noqa
        return ['unbounded', node.precedence.value]

    def __call__(self, node: no.SetSelect) -> Part:  # noqa
        return [
            self(node.left),
            [self(i) for i in node.items] if node.items else [],
        ]

    def __call__(self, node: no.SetSelectItem) -> Part:  # noqa
        return [
            node.kind.value,
            node.set_quantifier.value if node.set_quantifier is not None else [],
            self(node.right),
        ]

    def __call__(self, node: no.Unpivot) -> Part:  # noqa
        return [
            self(node.relation),
            Concat(['unpivot', Paren([
                self(node.value_col),
                'for',
                self(node.name_col),
                'in',
                Paren(List([self(c) for c in node.pivot_cols])),
            ])]),
        ]

    def __call__(self, node: no.Traversal) -> Part:  # noqa
        return Concat([
            self(node.value),
            ':',
            *[
                ('[' + r + ']') if isinstance(k, no.Integer) else (('.' if i else '') + r)
                for i, k in enumerate(node.keys)
                for r in [self(k)]
            ],
        ])


def _drop_empties(it: T) -> ta.List[T]:
    return [e for e in it if not (
        isinstance(e, collections.abc.Sequence) and
        not e and
        not isinstance(e, str)
    )]


def compact_part(part: Part) -> Part:
    if isinstance(part, str):
        return part
    elif isinstance(part, collections.abc.Sequence):
        return _drop_empties(compact_part(c) for c in part)
    elif isinstance(part, Paren):
        return Paren(compact_part(part.part))
    elif isinstance(part, List):
        parts = _drop_empties(compact_part(c) for c in part.parts)
        return List(parts, part.delimiter) if parts else []
    elif isinstance(part, Concat):
        parts = _drop_empties(compact_part(c) for c in part.parts)
        return Concat(parts) if parts else []
    else:
        raise TypeError(part)


def render_part(part: Part, buf: io.StringIO) -> None:
    if isinstance(part, str):
        buf.write(part)
    elif isinstance(part, collections.abc.Sequence):
        for i, c in enumerate(part):
            if i:
                buf.write(' ')
            render_part(c, buf)
    elif isinstance(part, Paren):
        buf.write('(')
        render_part(part.part, buf)
        buf.write(')')
    elif isinstance(part, List):
        for i, c in enumerate(part.parts):
            if i:
                buf.write(part.delimiter + ' ')
            render_part(c, buf)
    elif isinstance(part, Concat):
        for c in part.parts:
            render_part(c, buf)
    else:
        raise TypeError(part)


def render(node: no.Node) -> str:
    part = Renderer()(node)
    compact = compact_part(part)
    buf = io.StringIO()
    render_part(compact, buf)
    return buf.getvalue()
