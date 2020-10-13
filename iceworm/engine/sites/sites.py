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
 - auditing
  - git vs zipsafe - prefer zipsafe capability
  - scan whole package, build hash tree of all files?
  - use git rev too when present
  - IJ-style sqlitedb of index/catalog/metadata, scan/invalidate/rebuild on exec
  - CLI style usage for iterative ds dev
 - git aware sites - tag history, annotation, branches, etc, link to gh/pr/jira
 - site rule for loading dirs of csvs + create_table_as'ing them
"""
import typing as ta

from omnibus import check
from omnibus import collections as col
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus.serde.objects import yaml as oyaml

from .. import elements as els
from ...utils import serde


class SourceLocation(els.Annotation, els.Inherited):
    path: str = dc.field(check=lambda s: isinstance(s, str) and s)
    line: int = dc.field(check=lambda i: isinstance(i, int) and i >= 0)


class Format(dc.Pure, eq=False):
    name: str
    extensions: ta.Collection[str] = dc.field(check=lambda s: not isinstance(s, str))


class Formats(lang.ValueEnum):
    YAML = Format('yaml', {'yml', 'yaml'})
    SQL = Format('sql', {'sql'})


FORMATS_BY_EXTENSION: ta.Mapping[str, Format] = col.unique_dict((e, f) for f in Formats._by_value for e in f.extensions)


class Site(els.Element):

    dc.metadata({els.PhaseFrozen: els.PhaseFrozen(els.Phases.SITES)})

    path: str = dc.field(check=lambda s: isinstance(s, str) and s)
    format: ta.Optional[str] = None


class SiteProcessor(els.ElementProcessor):

    @classmethod
    def phases(cls) -> ta.Iterable[els.Phase]:
        return [els.Phases.SITES]

    def match(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return elements.get_type_set(Site)

    def process(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        def load(s: Site) -> ta.Iterable[els.Element]:
            with open(s.path, 'r') as f:
                src = f.read()

            fmt = FORMATS_BY_EXTENSION[(s.format if s.format else s.path.split('.')[-1]).lower()]

            if fmt is Formats.YAML:
                lst = []
                with lang.disposing(oyaml.WrappedLoaders.base(src)) as loader:
                    while loader.check_data():
                        node = loader.get_data()
                        for child in check.isinstance(node.value, ta.Sequence):
                            uchild = oyaml.unwrap(child)
                            el = serde.deserialize(uchild, els.Element)
                            sloc = SourceLocation(s.path, child.node.start_mark.line + 1)
                            el = dc.replace(
                                el,
                                anns={**el.anns, SourceLocation: sloc},
                                meta={els.Origin: els.Origin(s)},
                            )
                            lst.append(el)
                return lst

            elif fmt is Formats.SQL:
                # from ..trees import parsing as par
                raise NotImplementedError

            else:
                raise TypeError(fmt)

        return [r for e in elements for r in (load(e) if isinstance(e, Site) else [e])]
