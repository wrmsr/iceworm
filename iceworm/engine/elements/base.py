"""
TODO:
 - class Id? like Ref? comparison validity via issubclass? or, due to cyclic def, just refuses to cmp vs str?
 - 'project'? 'world'?
  - 'mount'-like 'grafts' of dirs with configs: mangling, templating, etc
 - sql files, directory structure, yamls, generators
  - datagrip as ide? .sql scripts out of order, go-to-def?
  - subdirs as schemas?
  - sql files could start with 'use <conn>'
  - * temp / scoped tables *
  - ** temp / scoped funcs - table and scalar **
  - temp elements gc'd whenever possible, code to cleanup zombies
  - make json comments the norm?
 - lib freestanding, cfg in monorepo? up to datasci really
 - pluggable mangling - users can write cifer$abc, run in datagrip goes to users schema, mangled at load by iw
  - mangling here is for datagrip / user, not ice - ice doesnt need it
 - 'scopes' not files
  - lol, whoa, scoped sql variables?
  - files written as executable tests?
  - no if statements = actually good - explicitly take 'both sides'
 - accept vs reject vs ignore replace
 - modeling something as simple as an if statement from cfg service..
  - flatten?
  - patmatcher
  - idiom: insert into foo select * from bar where exists (select 1 from config where key = 'a' and value = 'b')
   - optimize fact config is 'static' and known, convert into if statement
   - optimize away inserts from known empty tables
   - support in ctes
 - loops
  - tbl funcs vs star templates
  - either way an expansion, but table funcs more powerful
 - dc style 'profiles' on tables?
 - lol, templated (which always means jinja) sql files
  - header can declare deps, injected into context: {foo: Foo, bar: 'Bar[int]'}
 - 'internal'?
 - individual 'processed' anns
 - tok: 'push complexity to the plan' - obv cant as much, but still have ops to xform
  - but recursive as ops contain query trees
  - is there an equiv of 'jitfuncs'? basic blocks? everything between joins? everything between cross-conn joins?
   - everything between *elements*?
  - can still split, is not opaque, can analyse into
  - simplifies viz
  - does split/merge happen on the fly? reactive coalescing?
 - insert into pagerduty.alerts (to, body) select 'dp@cb.com', 'not enough things' where (
     select count(*) from (select null from things where ds = today() limit 5)) < 5
  - lol, system table of failures, insert into pagerduty.alerts select … from system.failures where table_name = ...
 - give everything a name? type:filename:line:col:seq?
 - id lookup suggestion ( https://docs.python.org/3/library/difflib.html#difflib.get_close_matches )
 - custom datatypes, desugared to binary + udfs? proto?

** *NOT* nested **

blob:
 - really, 'state' as configured by 'build' can be considered just a bigass sql file - a giant mass of creates / inserts
 - could be shipped to service without flip
 - like, sorta - 1G csvs could but shouldn't
 - still want pre-verification
 - task/thread/subsystem that frequently writes connector schemas somewhere
  - to s3, a-p (sites?) can use for pre-verification
 - lol, meta, written to an s3 connector, tables all the way down
 - need connectors? have connectors?
 - 'create connector'? borderline bad divergence from snowflake, but all-sql is powerful
 - really all sql with hot comments
"""
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang

from ...utils import annotations as anns
from ...utils import build_dc_repr
from ...utils import nodal


Id = str


def id_check(obj: ta.Any) -> bool:
    return isinstance(obj, Id) and obj


def optional_id_check(obj: ta.Any) -> bool:
    return obj is None or (isinstance(obj, Id) and obj)


class Annotation(anns.Annotation, abstract=True):
    pass


class Annotations(anns.Annotations[Annotation]):

    @classmethod
    def _ann_cls(cls) -> ta.Type[Annotation]:
        return Annotation


class Element(dc.Enum, nodal.Nodal['Element'], reorder=True):

    id: ta.Optional[Id] = dc.field(None, check=optional_id_check, kwonly=True)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        nf = dc.fields_dict(cls)['id']
        check.state(nf.type in (Id, ta.Optional[Id]))

    anns: Annotations = nodal.new_anns_field(Annotations)
    meta: ta.Mapping[ta.Any, ta.Any] = nodal.new_meta_field(Annotation)

    @classmethod
    def _nodal_cls(cls) -> ta.Type['Element']:
        return Element

    __repr__ = build_dc_repr


class Origin(Annotation):
    element: Element


class Frozen(lang.Marker):
    pass
