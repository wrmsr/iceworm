from omnibus import check

from ..trees import nodes as no
from ..trees import parsing as par
from ..types import QualifiedName


def parse_simple_select_star_table(query: str) -> QualifiedName:
    root = check.isinstance(par.parse_statement(query), no.Select)
    check.state(list(root.items) == [no.AllSelectItem()])
    check.state(not root.where)
    check.state(not root.top_n)
    check.state(not root.set_quantifier)
    check.state(not root.group_by)
    check.state(not root.having)
    check.state(not root.qualify)
    check.state(not root.order_by)
    check.state(not root.limit)
    tn = check.isinstance(check.single(root.relations), no.Table)
    return tn.name.name
