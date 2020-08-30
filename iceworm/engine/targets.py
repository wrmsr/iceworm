"""
TODO:
 - sql files, directory structure, yamls, generators
  - datagrip as ide? .sql scripts out of order, go-to-def?
  - subdirs as schemas?
  - sql files could start with 'use <conn>'
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
import operator
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc

from .. import metadata as md_
from ..types import QualifiedName
from ..utils import annotations as anns
from ..utils import serde


T = ta.TypeVar('T"')


class Annotation(anns.Annotation, abstract=True):
    pass


class Annotations(anns.Annotations[Annotation]):

    @classmethod
    def _ann_cls(cls) -> ta.Type[Annotation]:
        return Annotation


class Target(dc.Enum):

    anns: Annotations = dc.field(
        (),
        kwonly=True,
        repr=False,
        hash=False,
        compare=False,
        coerce=Annotations,
        metadata={serde.Ignore: operator.not_},
    )

    @property
    def name(self) -> ta.Optional[QualifiedName]:
        return None


class Origin(Annotation):
    target: Target


class Table(Target):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)
    md: ta.Optional[md_.Table] = dc.field(None, check=lambda o: o is None or isinstance(o, md_.Table))


class Rows(Target):
    table: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))

    name: ta.Optional[QualifiedName] = dc.field(None, coerce=QualifiedName.of_optional, kwonly=True)


class Function(Target):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)


class TargetSet:

    def __init__(self, targets: ta.Iterable[Target]) -> None:
        super().__init__()

        self._targets = [check.isinstance(e, Target) for e in targets]

        self._target_set = ocol.IdentitySet(self._targets)
        by_name = ocol.IdentityKeyDict()
        for target in self._targets:
            if target.name is not None:
                check.not_in(target.name, by_name)
                by_name[target.name] = target
        self._targets_by_name: ta.Mapping[QualifiedName, Target] = by_name
        self._node_sets_by_type: ta.Dict[type, ta.AbstractSet[Target]] = {}

    @classmethod
    def of(cls, it: ta.Iterable[Target]) -> 'TargetSet':
        if isinstance(it, cls):
            return it
        else:
            return cls(it)

    def get_target_type_set(self, ty: ta.Type[T]) -> ta.AbstractSet[T]:
        try:
            return self._node_sets_by_type[ty]
        except KeyError:
            ret = self._node_sets_by_type[ty] = ocol.IdentitySet(n for n in self._targets if isinstance(n, ty))
            return ret

    def __iter__(self) -> ta.Iterator[Target]:
        return iter(self._targets)

    def __contains__(self, key: ta.Union[QualifiedName, Target, type]) -> bool:
        if isinstance(key, QualifiedName):
            return key in self._targets_by_name
        elif isinstance(key, Target):
            return key in self._target_set
        elif isinstance(key, type):
            return bool(self.get_target_type_set(key))
        else:
            raise TypeError(key)

    def __getitem__(self, name: QualifiedName) -> Target:
        return self._targets_by_name[check.isinstance(name, QualifiedName)]
