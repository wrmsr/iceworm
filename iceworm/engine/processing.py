import contextlib
import inspect
import os.path
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import properties
import pytest

from . import connectors as ctrs
from . import ops
from . import targets as tars
from . import worlds as wo
from .. import datatypes as dt
from .. import metadata as md
from ..tests.helpers import pg_url
from ..trees import analysis as ana
from ..trees import datatypes as tdatatypes
from ..trees import nodes as no
from ..trees import origins
from ..trees import parsing as par
from ..trees import rendering
from ..trees import symbols
from ..trees import transforms as ttfm
from ..types import QualifiedName
from ..utils import secrets as sec
from .connectors import computed as cmp
from .connectors import files
from .connectors import sql
from .ops import execution as exe
from .ops import Op
from .ops import transforms as tfm


class TargetProcessor:

    def __init__(self, input: ta.Iterable[tars.Target]) -> None:
        super().__init__()

        self._input = tars.TargetSet.of(input)

    @properties.cached
    def output(self) -> tars.TargetSet:
        raise NotImplementedError

    # def infer_md_table(world: wo.World, query: str) -> md.Table:
    #     root = par.parse_statement(query)
    #
    #     table_names = {
    #         tn.name.name
    #         for tn in ana.basic(root).get_node_type_set(no.Table)
    #     }
    #
    #     alias_sets_by_tbl: ta.MutableMapping[md.Object, ta.Set[QualifiedName]] = ocol.IdentityKeyDict()
    #     for tn in table_names:
    #         objs = list(world.reflect(tn))
    #         if not objs:
    #             raise InferenceError
    #         obj = check.single(objs)
    #         aset = alias_sets_by_tbl.setdefault(obj, set())
    #         if tn != obj.name:
    #             aset.add(tn)
    #
    #     cat = md.Catalog(
    #         tables=[
    #             dc.replace(t, aliases={*t.aliases, *aset}) if aset else t
    #             for t, aset in alias_sets_by_tbl.items()
    #         ],
    #     )
    #
    #     print(cat)
    #
    #     root = ttfm.AliasRelationsTransformer(root)(root)
    #     root = ttfm.ExpandSelectsTransformer(root, cat)(root)
    #     root = ttfm.LabelSelectItemsTransformer(root)(root)
    #     print(rendering.render(root))
    #
    #     syms = symbols.analyze(root, cat)
    #     oris = origins.analyze(root, syms)
    #
    #     dts = tdatatypes.analyze(root, oris, cat)
    #     tt = check.isinstance(dts.dts_by_node[root], dt.Table)
    #
    #     ren = rendering.render(root)
    #     print(ren)
    #
    #     # FIXME: pg.c defined in terms of generated pg.b, need iterativity
    #     return md.Table(
    #         ['$anon'],
    #         [md.Column(n, t) for n, t in tt.columns],
    #     )
