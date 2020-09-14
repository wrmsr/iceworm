import contextlib
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties

from .. import connectors as ctrs
from .. import elements as els
from ... import metadata as md
from ...trees import nodes as no
from ...types import QualifiedName
from ...utils import unique_dict
from .targets import Materialization
from .targets import Rows
from .targets import Table


class ReflectReferencedTablesProcessor(els.InstanceElementProcessor):

    def __init__(
            self,
            ctors: ctrs.ConnectorSet,
    ) -> None:
        super().__init__()

        self._ctors = ctrs.ConnectorSet.of(ctors)

    @classmethod
    def dependencies(cls) -> ta.Iterable[ta.Type['els.ElementProcessor']]:
        return {*super().dependencies(), els.queries.QueryBasicAnalysisElementProcessor}

    class Instance(els.InstanceElementProcessor.Instance['ReflectReferencedTablesProcessor']):

        @properties.cached
        @property
        def table_name_sets_by_rows_eles(self) -> ta.Mapping[Rows, ta.AbstractSet[QualifiedName]]:
            return ocol.IdentityKeyDict(
                (ele, {
                    tn.name.name
                    for tn in els.queries.get_basic(ele, ele.query).get_node_type_set(no.Table)
                })
                for ele in self.input.get_type_set(Rows)
            )

        @properties.cached
        @property
        def rows_ele_sets_by_table_name(self) -> ta.Mapping[QualifiedName, ta.AbstractSet[Rows]]:
            ret = {}
            for ele, tns in self.table_name_sets_by_rows_eles.items():
                for tn in tns:
                    ret.setdefault(tn, ocol.IdentitySet()).add(ele)
            return ret

        @properties.cached
        @property
        def tables_by_name(self) -> ta.Mapping[QualifiedName, Table]:
            return unique_dict(
                (QualifiedName([ele.connector.id, *ele.name]), self.input[ele.table])
                for ele in self.input.get_type_set(Materialization)
            )

        @properties.cached
        @property
        def matches(self) -> ta.AbstractSet[els.Element]:
            ret = ocol.IdentitySet()
            for table_name, rows_eles in self.rows_ele_sets_by_table_name.items():
                if table_name in self.tables_by_name:
                    continue
                ret.update(rows_eles)
            return ret

        def reflect(self, name: QualifiedName) -> ta.Sequence[md.Object]:
            objs = []

            if len(name) > 1 and name[0] in self.owner._ctors:
                ctor = self.owner._ctors[name[0]]
                with contextlib.closing(ctor.connect()) as conn:
                    connobjs = conn.reflect([QualifiedName(name[1:])])
                    if connobjs:
                        objs.append(check.single(connobjs.values()))

            for ctor in self.owner._ctors:
                with contextlib.closing(ctor.connect()) as conn:
                    connobjs = conn.reflect([name])
                    if connobjs:
                        objs.extend(connobjs.values())

            return objs

        @properties.stateful_cached
        @property
        def output(self) -> els.ElementSet:
            alias_sets_by_md_table: ta.MutableMapping[md.Object, ta.Set[QualifiedName]] = ocol.IdentityKeyDict()
            for table_name in self.rows_ele_sets_by_table_name:
                if table_name in self.tables_by_name:
                    continue

                objs = list(self.reflect(table_name))
                obj = check.isinstance(check.single(objs), md.Table)

                aset = alias_sets_by_md_table.setdefault(obj, set())
                if table_name != obj.name:
                    aset.add(table_name)

            new = []
            for md_table, aliases in alias_sets_by_md_table.items():
                for alias in aliases:
                    id: els.Id = '/'.join(alias)
                    ctor = self.owner._ctors[alias[0]]
                    new.extend([
                        Table(id, md_table),
                        Materialization(id, ctor.id, alias[1:], readonly=True),
                    ])

            return els.ElementSet.of([
                *[e for e in self.input if e not in self.matches],
                *[dc.replace(e, meta={els.Origin: els.Origin(e)}) for e in self.matches],
                *new,
            ])
