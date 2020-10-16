"""
TODO:
 - siteanalysis.. anns not meta
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
import os.path
import typing as ta

from omnibus import check
from omnibus import collections as col
from omnibus import dataclasses as dc
from omnibus import lang
from omnibus.serde.objects import yaml as oyaml

from .. import elements as els
from ...trees import nodes as no
from ...trees import parsing as par  # noqa
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


class SiteLoaded(els.Annotation):
    abs_path: str


def get_site(el: els.Element) -> ta.Optional[Site]:
    cur = el
    while True:
        try:
            o = cur.meta[els.Origin]
        except KeyError:
            return None
        cur = o.element
        if isinstance(cur, Site) and SiteLoaded in cur.anns:
            return cur


class SiteProcessor(els.ElementProcessor):

    @classmethod
    def phases(cls) -> ta.Iterable[els.Phase]:
        return [els.Phases.SITES]

    def match(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        return [s for s in elements.get_type_set(Site) if SiteLoaded not in s.anns]

    def process(self, elements: els.ElementSet) -> ta.Iterable[els.Element]:
        def load(s: Site) -> ta.Iterable[els.Element]:
            sos = [sb for sb in els.iter_origins(s) if isinstance(sb, Site) and SiteLoaded in sb.anns]
            if sos:
                base_path = os.path.dirname(sos[0].anns[SiteLoaded].abs_path)
            else:
                base_path = os.getcwd()

            abs_path = os.path.abspath(os.path.join(base_path, s.path))

            ls = dc.replace(
                s,
                anns={**s.anns, SiteLoaded: SiteLoaded(abs_path)},
                meta={els.Origin: els.Origin(s)},
            )

            lst = [ls]

            fmt = FORMATS_BY_EXTENSION[(s.format if s.format else s.path.split('.')[-1]).lower()]

            if fmt is Formats.YAML:
                with open(abs_path, 'r') as f:
                    src = f.read()

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
                                meta={els.Origin: els.Origin(ls)},
                            )
                            lst.append(el)

            elif fmt is Formats.SQL:
                from .. import rules as rls

                if os.path.isdir(abs_path):
                    for fn in os.listdir(abs_path):
                        if not fn.endswith('.sql'):
                            continue

                        with open(os.path.join(abs_path, fn), 'r') as f:
                            src = f.read()

                        sn, tn, _ = fn.split('.')
                        sel = check.isinstance(check.single(par.parse_stmts(src)), no.Select)  # noqa

                        lst.append(
                            rls.TableAsSelect(
                                [sn, tn],
                                src.strip(' \r\n;'),
                                anns={SourceLocation: SourceLocation(s.path, 1)},
                                meta={els.Origin: els.Origin(ls)},
                            )
                        )

                else:
                    with open(abs_path, 'r') as f:
                        src = f.read()

                    stmts = par.parse_stmts(src)
                    for stmt in stmts:
                        ctas = check.isinstance(stmt, no.CreateTable)
                        sel = check.isinstance(ctas.select, no.Select)  # noqa

                        breakpoint()

            else:
                raise TypeError(fmt)

            return lst

        return [
            r
            for e in elements
            for r in (load(e) if isinstance(e, Site) and SiteLoaded not in e.anns else [e])
        ]
