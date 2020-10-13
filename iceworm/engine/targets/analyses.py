import abc
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus import properties

from .. import connectors as ctrs
from .. import elements as els
from ...trees import nodes as no
from ...types import QualifiedName
from .targets import Materialization
from .targets import Rows
from .targets import Table


class RowsTableDependencies(dc.Frozen, allow_setattr=True):

    tables_by_name: ta.Mapping[QualifiedName, Table] = dc.field(
        coerce=lambda d: ocol.FrozenDict(
            (QualifiedName.of(n), t)
            for n, t in check.isinstance(d, ta.Mapping).items()
        )
    )

    @properties.cached
    @property
    def name_sets_by_table(self) -> els.ElementMap[Table, ta.AbstractSet[QualifiedName]]:
        ret = {}
        for n, t in self.tables_by_name.items():
            ret.setdefault(t, set()).add(n)
        return els.ElementMap(ret)


class AbstractTableDependenciesAnalysis(els.Analysis, lang.Abstract):

    @abc.abstractproperty
    def _strict(self) -> bool:
        raise NotImplementedError

    @classmethod
    def cls_dependencies(cls) -> ta.Iterable[ta.Type[els.Dependable]]:
        return {*super().cls_dependencies(), els.queries.QueryBasicAnalysis}

    @properties.cached
    @property
    def tables_by_name(self) -> ta.Mapping[QualifiedName, Table]:
        return ocol.unique_dict(
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
    def by_rows(self) -> els.ElementMap[Rows, RowsTableDependencies]:
        return els.ElementMap(
            (ele, RowsTableDependencies({
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


class TableDependenciesAnalysis(AbstractTableDependenciesAnalysis, lang.Final):
    _strict = False


class NamespaceAnalysis(els.Analysis):

    @properties.cached
    @property
    def namespace(self) -> ta.Mapping[ctrs.Connector.Config, ta.Mapping[Table, ta.AbstractSet[Materialization]]]:
        dct = ocol.IdentityKeyDict()
        for mat in self.elements.get_type_set(Materialization):
            dct.setdefault(self.elements[mat.connector], ocol.IdentityKeyDict()).setdefault(self.elements[mat.table], ocol.IdentitySet()).add(mat)  # noqa0j0
        return els.ElementMap((ctr, els.ElementMap((tbl, els.ElementSet(mats)) for tbl, mats in d2.items())) for ctr, d2 in dct.items())  # noqa
