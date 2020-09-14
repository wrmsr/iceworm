"""
TODO:
 - *** CONNECTOR TABLES ADDED TO ELEMENTS AS TABLES AND R/O MATERIALIZATIONS, GIVEN ID'S ***
 - 'processed' sql query attribute?
 - ** query elements get a Map[QualifiedName, Id] field (or att??)
"""
import contextlib
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties

from . import connectors as ctrs
from . import elements as els
from . import targets as tars
from .. import datatypes as dt
from .. import metadata as md
from ..trees import datatypes as tdt
from ..trees import nodes as no
from ..trees import origins
from ..trees import symbols
from ..trees import transforms as ttfm
from ..trees.types import AstQuery
from ..types import QualifiedName
from ..utils import unique_dict


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
        def table_name_sets_by_rows_eles(self) -> ta.Mapping[tars.Rows, ta.AbstractSet[QualifiedName]]:
            return ocol.IdentityKeyDict(
                (ele, {
                    tn.name.name
                    for tn in els.queries.get_basic(ele, ele.query).get_node_type_set(no.Table)
                })
                for ele in self.input.get_type_set(tars.Rows)
            )

        @properties.cached
        @property
        def rows_ele_sets_by_table_name(self) -> ta.Mapping[QualifiedName, ta.AbstractSet[tars.Rows]]:
            ret = {}
            for ele, tns in self.table_name_sets_by_rows_eles.items():
                for tn in tns:
                    ret.setdefault(tn, ocol.IdentitySet()).add(ele)
            return ret

        @properties.cached
        @property
        def tables_by_name(self) -> ta.Mapping[QualifiedName, tars.Table]:
            return unique_dict(
                (QualifiedName([ele.connector.id, *ele.name]), self.input[ele.table])
                for ele in self.input.get_type_set(tars.Materialization)
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
                        tars.Table(id, md_table),
                        tars.Materialization(id, ctor.id, alias[1:], readonly=True),
                    ])

            return els.ElementSet.of([
                *[e for e in self.input if e not in self.matches],
                *[dc.replace(e, meta={els.Origin: els.Origin(e)}) for e in self.matches],
                *new,
            ])


class InferTableProcessor(els.InstanceElementProcessor):

    def __init__(
            self,
            ctors: ctrs.ConnectorSet,
    ) -> None:
        super().__init__()

        self._ctors = ctrs.ConnectorSet.of(ctors)

    @classmethod
    def dependencies(cls) -> ta.Iterable[ta.Type['els.ElementProcessor']]:
        return {*super().dependencies(), ReflectReferencedTablesProcessor}

    class Instance(els.InstanceElementProcessor.Instance['InferTableProcessor']):

        @properties.cached
        def matches(self) -> ta.Iterable[els.Element]:
            ret = []
            for ele in self.input:
                if isinstance(ele, tars.Table) and ele.md is None:
                    rows = check.single(rt for rt in self.input.get_type_set(tars.Rows) if rt.table == ele)
                    ret.append(ele)
                    ret.append(rows)
            return ret

        @properties.cached
        @property
        def tables_by_name(self) -> ta.Mapping[QualifiedName, tars.Table]:
            return unique_dict(
                (QualifiedName([ele.connector.id, *ele.name]), self.input[ele.table])
                for ele in self.input.get_type_set(tars.Materialization)
            )

        @properties.cached
        @property
        def table_names_by_id(self) -> ta.Mapping[els.Id, QualifiedName]:
            return unique_dict((ele.id, name) for name, ele in self.tables_by_name.items())

        @properties.cached
        @property
        def ele_seq(self) -> ta.Sequence[els.Element]:
            return list(self.input)

        @properties.cached
        @property
        def idxs(self) -> ta.Mapping[els.Element, int]:
            return ocol.IdentityKeyDict((e, i) for i, e in enumerate(self.ele_seq))

        @properties.cached
        @property
        def id_dep_sets_by_id(self) -> ta.Mapping[str, ta.AbstractSet[str]]:
            dct: ta.Dict[str, ta.Set[str]] = {}
            for ele in self.input:
                if not isinstance(ele, tars.Table):
                    continue

                rows_eles = [rt for rt in self.input.get_type_set(tars.Rows) if rt.table == ele]
                if not rows_eles:
                    continue
                rows = check.single(rows_eles)

                deps = {
                    self.tables_by_name[name].id
                    for n in els.queries.get_basic(rows, rows.query).get_node_type_set(no.Table)
                    for name in [n.name.name]
                    if name in self.tables_by_name
                }

                check.not_in(ele.id, dct)
                dct[ele.id] = deps

            return dct

        @properties.stateful_cached
        def output(self) -> els.ElementSet:
            topo = [
                check.isinstance(self.input[id], tars.Table)
                for step in ocol.toposort(self.id_dep_sets_by_id)
                for id in step
            ]

            given_tables: ta.Dict[QualifiedName, md.Table] = {}
            lst = list(self.ele_seq)
            for table in topo:
                table_idx = self.idxs[table]
                check.state(lst[table_idx] is table)
                if table.md is not None:
                    continue

                rows = check.single(rt for rt in self.input.get_type_set(tars.Rows) if rt.table == table)
                rows_idx = self.idxs[rows]
                check.state(lst[rows_idx] is rows)

                name = self.table_names_by_id[table.id]
                root, md_table = self.infer_table(
                    rows,
                    given_tables,
                    name=name,
                )

                lst[rows_idx] = dc.replace(
                    rows,
                    query=AstQuery(root),
                    meta={els.Origin: els.Origin(rows)},
                )

                lst[table_idx] = dc.replace(
                    table,
                    md=md_table,
                    meta={els.Origin: els.Origin(table)},
                )

                given_tables[name] = md_table

            return els.ElementSet.of(lst)

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

        def infer_table(
                self,
                rows: tars.Rows,
                given_tables: ta.Mapping[QualifiedName, md.Table],
                *,
                name: ta.Optional[QualifiedName] = None,
        ) -> ta.Tuple[no.Node, md.Table]:
            root = check.isinstance(rows.query, AstQuery).root

            table_names = {
                tn.name.name
                for tn in els.queries.get_basic(rows, rows.query).get_node_type_set(no.Table)
            }

            alias_sets_by_tbl: ta.MutableMapping[md.Object, ta.Set[QualifiedName]] = ocol.IdentityKeyDict()
            for tn in table_names:
                if tn in given_tables:
                    alias_sets_by_tbl[given_tables[tn]] = set()
                else:
                    objs = list(self.reflect(tn))
                    obj = check.single(objs)
                    aset = alias_sets_by_tbl.setdefault(obj, set())
                    if tn != obj.name:
                        aset.add(tn)

            cat = md.Catalog(
                tables=[
                    dc.replace(t, aliases={*t.aliases, *aset}) if aset else t
                    for t, aset in alias_sets_by_tbl.items()
                ],
            )

            root = ttfm.AliasRelationsTransformer(root)(root)
            root = ttfm.ExpandSelectsTransformer(root, cat)(root)
            root = ttfm.LabelSelectItemsTransformer(root)(root)

            syms = symbols.analyze(root, cat)
            oris = origins.analyze(root, syms)

            dts = tdt.analyze(root, oris, cat)
            tt = check.isinstance(dts.dts_by_node[root], dt.Table)

            # FIXME: pg.c defined in terms of generated pg.b, need iterativity
            return root, md.Table(
                name if name is not None else ['$anon'],
                [md.Column(n, t) for n, t in tt.columns],
            )
