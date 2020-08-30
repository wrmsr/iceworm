import contextlib
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties

from . import connectors as ctrs
from . import targets as tars
from .. import datatypes as dt
from .. import metadata as md
from ..trees import analysis as ana
from ..trees import datatypes as tdatatypes
from ..trees import nodes as no
from ..trees import origins
from ..trees import parsing as par
from ..trees import rendering
from ..trees import symbols
from ..trees import transforms as ttfm
from ..types import QualifiedName


class TargetProcessor:

    def __init__(
            self,
            input: ta.Iterable[tars.Target],
            ctors: ta.Iterable[ctrs.Connector],
    ) -> None:
        super().__init__()

        self._input = tars.TargetSet.of(input)
        self._ctors = ctrs.ConnectorSet.of(ctors)

    @property
    def input(self) -> tars.TargetSet:
        return self._input

    @property
    def ctors(self) -> ctrs.ConnectorSet:
        return self._ctors

    @properties.cached
    def output(self) -> tars.TargetSet:
        ts = list(self._input)
        for i in range(len(ts)):
            tar = ts[i]
            if isinstance(tar, tars.Table):
                if tar.md is None:
                    rows = check.single(rt for rt in ts if isinstance(rt, tars.Rows) and rt.table == tar.name)
                    mdt = self.infer_table(rows.query)
                    ts[i] = dc.replace(ts[i], md=mdt)

        raise NotImplementedError

    def reflect(self, name: QualifiedName) -> ta.Sequence[md.Object]:
        objs = []

        if len(name) > 1 and name[0] in self._ctors:
            ctor = self._ctors[name[0]]
            with contextlib.closing(ctor.connect()) as conn:
                connobjs = conn.reflect([QualifiedName(name[1:])])
                if connobjs:
                    objs.append(check.single(connobjs.values()))

        for ctor in self._ctors:
            with contextlib.closing(ctor.connect()) as conn:
                connobjs = conn.reflect([name])
                if connobjs:
                    objs.extend(connobjs.values())

        return objs

    def infer_table(self, query: str) -> md.Table:
        root = par.parse_statement(query)

        table_names = {
            tn.name.name
            for tn in ana.basic(root).get_node_type_set(no.Table)
        }

        alias_sets_by_tbl: ta.MutableMapping[md.Object, ta.Set[QualifiedName]] = ocol.IdentityKeyDict()
        for tn in table_names:
            objs = list(self.reflect(tn))
            if not objs:
                raise Exception  # InferenceError
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

        print(cat)

        root = ttfm.AliasRelationsTransformer(root)(root)
        root = ttfm.ExpandSelectsTransformer(root, cat)(root)
        root = ttfm.LabelSelectItemsTransformer(root)(root)
        print(rendering.render(root))

        syms = symbols.analyze(root, cat)
        oris = origins.analyze(root, syms)

        dts = tdatatypes.analyze(root, oris, cat)
        tt = check.isinstance(dts.dts_by_node[root], dt.Table)

        ren = rendering.render(root)
        print(ren)

        # FIXME: pg.c defined in terms of generated pg.b, need iterativity
        return md.Table(
            ['$anon'],
            [md.Column(n, t) for n, t in tt.columns],
        )
