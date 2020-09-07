"""
TODO:
 - cfgable qualifiedname mangling of queries
 - ** parsing of sql files, de-jinjaficatiton happens here **
  - track pre/post jinja src locs
  - track macro lineage
  - 'ordered' sql sequences / fragments come from here
   - element representation - linked list?
"""
from .elements import Element


class Site(Element):
    pass
