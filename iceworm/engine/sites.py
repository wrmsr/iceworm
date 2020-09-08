"""
TODO:
 - cfgable qualifiedname mangling of queries
 - ** parsing of sql files, de-jinjaficatiton happens here **
  - track pre/post jinja src locs
  - track macro lineage
  - 'ordered' sql sequences / fragments come from here
   - element representation - linked list?
 - 'caching' wrong word, cache in dev but static in prod
  - 'compilation' isn't even right as it really jits
  - jinja, parses, analyses, ultimately just elements
   - strip site? mark site as processed/loaded?
   - diff between actually just dumb caches (jinja, trees) and 'artifacts' (elements) ?
  - required for commit and prod, prod will not boot uncompiled
   - pre-commit, enforce at boot
"""
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus.serde.objects import yaml as oyaml

from . import elements as els
from ..utils import serde


class SourceLocation(els.Annotation):
    path: str = dc.field(check=lambda s: isinstance(s, str) and s)
    line: int = dc.field(check=lambda i: isinstance(i, int) and i >= 0)


class Site(els.Element):

    dc.metadata({els.processing.PhaseFrozen: els.processing.PhaseFrozen(els.processing.Phases.SITES)})

    path: str = dc.field(check=lambda s: isinstance(s, str) and s)


class SiteProcessor(els.ElementProcessor):

    @classmethod
    def phases(cls) -> ta.Iterable[els.processing.Phase]:
        return [els.processing.Phases.SITES]

    def processes(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return elements.get_type_set(Site)

    def process(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        def load(s: Site) -> ta.Iterable[els.Element]:
            with open(s.path, 'r') as f:
                src = f.read()
            lst = []
            with lang.disposing(oyaml.WrappedLoaders.base(src)) as loader:
                while loader.check_data():
                    node = loader.get_data()
                    for child in check.isinstance(node.value, ta.Sequence):
                        uchild = oyaml.unwrap(child)
                        el = serde.deserialize(uchild, els.Element)
                        sloc = SourceLocation(s.path, child.node.start_mark.line)
                        el = dc.replace(el, anns={**el.anns, SourceLocation: sloc})
                        lst.append(el)
            return lst
        return [r for e in elements for r in (load(e) if isinstance(e, Site) else [e])]
