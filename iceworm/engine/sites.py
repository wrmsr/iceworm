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

from omnibus import dataclasses as dc

from . import elements as els


class Site(els.Element):

    dc.metadata({els.processing.PhaseFrozen: els.processing.PhaseFrozen(els.processing.Phases.SITES)})


class SiteProcessor(els.ElementProcessor):

    @classmethod
    def phases(cls) -> ta.Iterable[els.processing.Phase]:
        return [els.processing.Phases.SITES]

    def processes(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        raise NotImplementedError

    def process(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        raise NotImplementedError
