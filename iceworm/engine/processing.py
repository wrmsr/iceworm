"""
TODO:
 - 'processed' sql query attribute?
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
from ..trees import parsing as par
from ..trees import rendering  # noqa
from ..trees import symbols
from ..trees import transforms as ttfm
from ..types import QualifiedName
from ..utils import unique_dict


class InferTableProcessor(els.ElementProcessor):

    def __init__(
            self,
            ctors: ta.Iterable[ctrs.Connector],
    ) -> None:
        super().__init__()

        self._ctors = ctrs.ConnectorSet.of(ctors)

    class Instance:

        def __init__(self, owner: 'InferTableProcessor', input: els.ElementSet) -> None:
            super().__init__()

            self._owner = check.isinstance(owner, InferTableProcessor)
            self._input = check.isinstance(input, els.ElementSet)

        @properties.stateful_cached
        def output(self) -> els.ElementSet:
            ele_tns = unique_dict(
                (ele.dst, self._input[ele.table]) for ele in self._input.get_element_type_set(tars.Materialization))
            tele_ids = unique_dict((ele.id, qn) for qn, ele in ele_tns.items())

            ts = els.ElementSet(self._input)
            tn_deps: ta.Dict[str, ta.Set[str]] = {}
            tn_idxs = {}
            for i, ele in enumerate(ts):
                if isinstance(ele, tars.Table):
                    tn_idxs[ele.id] = i
                    # TODO: get single Materialization, do.. something..
                    rows = check.single(rt for rt in ts.get_element_type_set(tars.Rows) if rt.table == ele)
                    root = par.parse_statement(rows.query)
                    deps = {
                        ele_tns[n.name.name].id
                        for n in ana.basic(root).get_node_type_set(no.Table) if n.name.name in ele_tns
                    }
                    check.not_in(ele.id, tn_deps)
                    tn_deps[ele.id] = deps

            given_tables: ta.Mapping[QualifiedName, md.Table] = {}

            ts = list(ts)
            topo = list(ocol.toposort(tn_deps))
            for sup in topo:
                for tn in sup:
                    ele: tars.Table = self._input[tn]
                    if ele.md is None:
                        rows = check.single(rt for rt in self._input.get_element_type_set(tars.Rows) if rt.table == ele)
                        mdt = self.infer_table(rows.query, given_tables)
                        qn = tele_ids[ele.id]
                        mdt = dc.replace(mdt, name=qn)
                        i = tn_idxs[ele.id]
                        tsi = ts[i]
                        ts[i] = dc.replace(tsi, md=mdt, anns={**tsi.anns, els.Origin: els.Origin(tsi)})
                        given_tables[qn] = mdt

            return els.ElementSet.of(ts)

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

        def infer_table(self, query: str, given_tables: ta.Mapping[QualifiedName, md.Table]) -> md.Table:
            root = par.parse_statement(query)

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
                ['$anon'],
                [md.Column(n, t) for n, t in tt.columns],
            )

    def processes(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return [t for t in elements.get_element_type_set(tars.Table) if t.md is None]

    def process(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return self.Instance(self, elements).output
