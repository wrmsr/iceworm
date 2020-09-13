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
from ..trees import analysis as ana
from ..trees import datatypes as tdatatypes
from ..trees import nodes as no
from ..trees import origins
from ..trees import rendering  # noqa
from ..trees import symbols
from ..trees import transforms as ttfm
from ..trees.types import AstQuery
from ..types import QualifiedName
from ..utils import unique_dict


class InferTableProcessor(els.ElementProcessor):

    def __init__(
            self,
            ctors: ctrs.ConnectorSet,
    ) -> None:
        super().__init__()

        self._ctors = ctrs.ConnectorSet.of(ctors)

    @classmethod
    def dependencies(cls) -> ta.Iterable[ta.Type['els.ElementProcessor']]:
        return {*super().dependencies(), els.queries.QueryBasicAnalysisElementProcesor}

    class Instance:

        def __init__(self, owner: 'InferTableProcessor', input: els.ElementSet) -> None:
            super().__init__()

            self._owner = check.isinstance(owner, InferTableProcessor)
            self._input = check.isinstance(input, els.ElementSet)

        @properties.cached
        @property
        def tables_by_name(self) -> ta.Mapping[QualifiedName, tars.Table]:
            return unique_dict(
                (QualifiedName([ele.connector.id, *ele.name]), self._input[ele.table])
                for ele in self._input.get_type_set(tars.Materialization)
            )

        @properties.cached
        @property
        def table_names_by_id(self) -> ta.Mapping[els.Id, QualifiedName]:
            return unique_dict((ele.id, name) for name, ele in self.tables_by_name.items())

        @properties.cached
        @property
        def ele_seq(self) -> ta.Sequence[els.Element]:
            return list(self._input)

        @properties.cached
        @property
        def idxs_by_id(self):
            return {e.id: i for i, e in enumerate(self.ele_seq)}

        @properties.cached
        @property
        def id_dep_sets_by_id(self) -> ta.Mapping[str, ta.AbstractSet[str]]:
            dct: ta.Dict[str, ta.Set[str]] = {}
            for ele in self._input:
                if not isinstance(ele, tars.Table):
                    continue

                rows = check.single(rt for rt in self._input.get_type_set(tars.Rows) if rt.table == ele)
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
                check.isinstance(self._input[id], tars.Table)
                for step in ocol.toposort({k: set(v) for k, v in self.id_dep_sets_by_id.items()})
                for id in step
            ]

            given_tables: ta.Dict[QualifiedName, md.Table] = {}
            lst = list(self._input)
            for ele in topo:
                if ele.md is not None:
                    continue

                rows = check.single(rt for rt in self._input.get_type_set(tars.Rows) if rt.table == ele)

                name = self.table_names_by_id[ele.id]
                md_table = self.infer_table(
                    check.isinstance(rows.query, AstQuery).root,
                    given_tables,
                    name=name,
                )

                idx = self.idxs_by_id[ele.id]
                check.state(lst[idx] is ele)
                lst[idx] = dc.replace(ele, md=md_table, meta={**ele.meta, els.Origin: els.Origin(ele)})

                given_tables[name] = md_table

            return els.ElementSet.of(lst)

        def reflect(self, name: QualifiedName) -> ta.Sequence[md.Object]:
            objs = []

            if len(name) > 1 and name[0] in self._owner._ctors:
                ctor = self._owner._ctors[name[0]]
                with contextlib.closing(ctor.connect()) as conn:
                    connobjs = conn.reflect([QualifiedName(name[1:])])
                    if connobjs:
                        objs.append(check.single(connobjs.values()))

            for ctor in self._owner._ctors:
                with contextlib.closing(ctor.connect()) as conn:
                    connobjs = conn.reflect([name])
                    if connobjs:
                        objs.extend(connobjs.values())

            return objs

        def infer_table(
                self,
                root: no.Node,
                given_tables: ta.Mapping[QualifiedName, md.Table],
                *,
                name: ta.Optional[QualifiedName] = None,
        ) -> md.Table:
            table_names = {
                tn.name.name
                for tn in ana.basic(root).get_node_type_set(no.Table)
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

            dts = tdatatypes.analyze(root, oris, cat)
            tt = check.isinstance(dts.dts_by_node[root], dt.Table)

            # ren = rendering.render(root)
            # print(ren)  # FIXME: update query

            # FIXME: pg.c defined in terms of generated pg.b, need iterativity
            return md.Table(
                name if name is not None else ['$anon'],
                [md.Column(n, t) for n, t in tt.columns],
            )

    def processes(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return [t for t in elements.get_type_set(tars.Table) if t.md is None]

    def process(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return self.Instance(self, elements).output
