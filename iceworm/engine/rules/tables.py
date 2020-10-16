import typing as ta

from omnibus import dataclasses as dc

from .. import elements as els
from .. import targets as tars
from ... import metadata as md_
from ...trees.types import Query
from ...types import QualifiedName
from .base import Rule
from .base import RuleProcessor


class TableAsSelect(Rule):
    table: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: Query = dc.field(coerce=Query.of)

    md: ta.Optional[md_.Table] = dc.field(None, check_type=(md_.Table, None), kwonly=True)


class TableAsSelectProcessor(RuleProcessor[TableAsSelect]):
    rule_cls = TableAsSelect

    def process(self, rule: TableAsSelect) -> ta.Iterable[els.Element]:
        cn, tn = rule.table
        ten = cn + '/' + tn
        return [
            tars.Table(ten, md=rule.md),
            tars.Materialization(ten, cn, [tn]),
            tars.Rows(ten, rule.query),
        ]


class InsertedRows(Rule):
    table: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: Query = dc.field(coerce=Query.of)


class InsertedRowsProcessor(RuleProcessor[InsertedRows]):
    rule_cls = InsertedRows

    def process(self, rule: InsertedRows) -> ta.Iterable[els.Element]:
        cn, tn = rule.table
        ten = cn + '/' + tn
        return [
            tars.Rows(ten, rule.query),
        ]
