"""
TODO:
 - *** CONNECTOR TABLES ADDED TO ELEMENTS AS TABLES AND R/O MATERIALIZATIONS, GIVEN ID'S ***
 - 'processed' sql query attribute?
 - ** query elements get a Map[QualifiedName, Id] field (or att??)
"""
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties

from .. import elements as els
from ... import metadata as md
from ...trees import datatypes as tdt
from ...trees import nodes as no
from ...trees import origins
from ...trees import symbols
from ...trees import transforms as ttfm
from ...trees.types import AstQuery
from ...types import QualifiedName
from .reflect import ReflectReferencedTablesProcessor
from .targets import Materialization
from .targets import Rows
from .targets import Table


class InferTableProcessor(els.InstanceElementProcessor):

    @classmethod
    def cls_dependencies(cls) -> ta.Iterable[ta.Type[els.ElementProcessor]]:
        return {*super().cls_dependencies(), ReflectReferencedTablesProcessor, els.queries.QueryBasicAnalysis}

    class Instance(els.InstanceElementProcessor.Instance['InferTableProcessor']):

        @properties.cached
        def matches(self) -> ta.Iterable[els.Element]:
            ret = []
            for ele in self.input:
                if isinstance(ele, Table) and ele.md is None:
                    rows = check.single(rt for rt in self.input.get_type_set(Rows) if rt.table == ele)
                    ret.append(ele)
                    ret.append(rows)
            return ret

        @properties.cached
        @property
        def tables_by_name(self) -> ta.Mapping[QualifiedName, Table]:
            return ocol.unique_dict(
                (QualifiedName([ele.connector.id, *ele.name]), self.input[ele.table])
                for ele in self.input.get_type_set(Materialization)
            )

        @properties.cached
        @property
        def table_names_by_id(self) -> ta.Mapping[els.Id, QualifiedName]:
            return ocol.unique_dict((ele.id, name) for name, ele in self.tables_by_name.items())

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
                if not isinstance(ele, Table):
                    continue

                rows_eles = [rt for rt in self.input.get_type_set(Rows) if rt.table == ele]
                if not rows_eles:
                    continue
                rows = check.single(rows_eles)

                deps = {
                    self.tables_by_name[name].id
                    for n in self.input.analyze(els.queries.QueryBasicAnalysis)[rows][rows.query].get_node_type_set(no.Table)  # noqa
                    for name in [n.name.name]
                    if name in self.tables_by_name
                }

                check.not_in(ele.id, dct)
                dct[ele.id] = deps

            return dct

        @properties.stateful_cached
        def output(self) -> els.ElementSet:
            topo = [
                check.isinstance(self.input[id], Table)
                for step in ocol.toposort(self.id_dep_sets_by_id)
                for id in step
            ]

            given_tables: ta.Dict[QualifiedName, md.Table] = {
                n: check.isinstance(t.md, md.Table)
                for n, t in self.tables_by_name.items()
                if not self.id_dep_sets_by_id.get(t.id, [])
            }

            lst = list(self.ele_seq)
            for table in topo:
                table_idx = self.idxs[table]
                check.state(lst[table_idx] is table)
                name = self.table_names_by_id[table.id]
                if table.md is not None:
                    given_tables[name] = table.md
                    continue

                rows = check.single(rt for rt in self.input.get_type_set(Rows) if rt.table == table)
                rows_idx = self.idxs[rows]
                check.state(lst[rows_idx] is rows)

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

        def infer_table(
                self,
                rows: Rows,
                given_tables: ta.Mapping[QualifiedName, md.Table],
                *,
                name: ta.Optional[QualifiedName] = None,
        ) -> ta.Tuple[no.Node, md.Table]:
            root = check.isinstance(rows.query, AstQuery).root

            table_names = {
                tn.name.name
                for tn in self.input.analyze(els.queries.QueryBasicAnalysis)[rows][rows.query].get_node_type_set(no.Table)  # noqa
            }

            alias_sets_by_tbl: ta.MutableMapping[md.Object, ta.Set[QualifiedName]] = ocol.IdentityKeyDict()
            for tn in table_names:
                tbl = check.isinstance(given_tables[tn], md.Table)
                aset = alias_sets_by_tbl.setdefault(tbl, set())
                if tn != tbl.name:
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
            tt = check.isinstance(dts.dts_by_node[root], md.TableType)

            # FIXME: pg.c defined in terms of generated pg.b, need iterativity
            return root, md.Table(
                name if name is not None else ['$anon'],
                [md.Column(n, t) for n, t in tt.columns],
            )
