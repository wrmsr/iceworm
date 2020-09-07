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
from .elements import Element


class Site(Element):
    pass
