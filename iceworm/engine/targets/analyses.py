import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties

from .. import elements as els
from ...trees import nodes as no
from ...types import QualifiedName
from ...utils import unique_dict
from .targets import Materialization
from .targets import Rows
from .targets import Table


class TableDependencies(dc.Frozen, allow_setattr=True):

    tables_by_name: ta.Mapping[QualifiedName, Table] = dc.field(
        coerce=lambda d: ocol.FrozenDict(
            (QualifiedName.of(n), t)
            for n, t in check.isinstance(d, ta.Mapping).items()
        )
    )

    @properties.cached
    @property
    def name_sets_by_table(self) -> els.ElementMap[els.Element, ta.AbstractSet[QualifiedName]]:
        ret = {}
        for n, t in self.tables_by_name.items():
            ret.setdefault(t, set()).add(n)
        return els.ElementMap(ret)


class TableDependenciesAnalysis(els.Analysis):
    _strict: bool = False

    @classmethod
    def cls_dependencies(cls) -> ta.Iterable[ta.Type[els.Dependable]]:
        return {*super().cls_dependencies(), els.queries.QueryBasicAnalysis}

    @properties.cached
    @property
    def tables_by_name(self) -> ta.Mapping[QualifiedName, Table]:
        return unique_dict(
            (QualifiedName([ele.connector.id, *ele.name]), self.elements[ele.table])
            for ele in self.elements.get_type_set(Materialization)
        )

    @properties.cached
    @property
    def name_sets_by_table(self) -> els.ElementMap[Table, ta.AbstractSet[QualifiedName]]:
        ret = {}
        for n, t in self.tables_by_name.items():
            ret.setdefault(t, set()).add(n)
        return els.ElementMap(ret)

    @properties.cached
    @property
    def by_element(self) -> els.ElementMap[els.Element, TableDependencies]:
        return els.ElementMap(
            (ele, TableDependencies({
                qn: self.tables_by_name[qn]
                for qn in qns
                if self._strict or qn in self.tables_by_name
            }))
            for ele in self.elements.get_type_set(Rows)
            for qns in [{
                t.name.name
                for t in self.elements.analyze(els.queries.QueryBasicAnalysis)[ele][ele.query].get_node_type_set(no.Table)  # noqa
            }]
        )

    def __getitem__(self, ele: Rows) -> TableDependencies:
        return self.by_element[ele]


class StrictTableDependenciesAnalysis(TableDependenciesAnalysis):
    _strict: bool = True
