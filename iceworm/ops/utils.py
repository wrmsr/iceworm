import typing as ta

from omnibus import check

from ..trees import analysis as tana
from ..trees import nodes as no
from ..trees import parsing as par
from ..types import QualifiedName


def is_simple_select(root: no.Select) -> bool:
    check.isinstance(root, no.Select)
    return (
            not root.where and
            not root.top_n and
            not root.set_quantifier and
            not root.group_by and
            not root.having and
            not root.qualify and
            not root.order_by and
            not root.limit
    )


def parse_simple_select_tables(query: str) -> ta.AbstractSet[QualifiedName]:
    root = check.isinstance(par.parse_statement(query), no.Select)
    if not is_simple_select(root):
        raise ValueError(root)
    basic = tana.basic(root)
    if not all(isinstance(r, (no.Table, no.AliasedRelation)) for r in basic.get_node_type_set(no.Relation)):
        raise ValueError(root)
    return {tn.name.name for tn in basic.get_node_type_set(no.Table)}


def parse_simple_select_table(query: str, *, star: bool = False) -> QualifiedName:
    root = check.isinstance(par.parse_statement(query), no.Select)
    if not is_simple_select(root):
        raise ValueError(root)
    basic = tana.basic(root)
    if not star:
        if list(root.items) == [no.AllSelectItem()]:
            raise ValueError(root)
    if not all(isinstance(r, (no.Table, no.AliasedRelation)) for r in basic.get_node_type_set(no.Relation)):
        raise ValueError(root)
    tns = [tn.name.name for tn in basic.get_node_type_set(no.Table)]
    if len(tns) != 1:
        raise ValueError(root)
    return check.single(tns)
