import typing as ta

from omnibus import dataclasses as dc

from .. import elements as els
from .. import targets as tars
from ... import metadata as md_
from ...types import QualifiedName
from .base import RuleProcessor
from .base import Rule


class TableAsSelect(Rule):
    table: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))

    md: ta.Optional[md_.Table] = dc.field(None, check=lambda o: o is None or isinstance(o, md_.Table), kwonly=True)


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
    query: str = dc.field(check=lambda o: isinstance(o, str))


class InsertedRowsProcessor(RuleProcessor[InsertedRows]):
    rule_cls = InsertedRows

    def process(self, rule: InsertedRows) -> ta.Iterable[els.Element]:
        cn, tn = rule.table
        ten = cn + '/' + tn
        return [
            tars.Rows(ten, rule.query),
        ]
