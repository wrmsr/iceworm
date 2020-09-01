"""
TODO:
 - sql files, directory structure, yamls, generators
  - datagrip as ide? .sql scripts out of order, go-to-def?
  - subdirs as schemas?
  - sql files could start with 'use <conn>'
  - * temp / scoped tables *
  - ** temp / scoped funcs - table and scalar **
  - temp targets gc'd whenever possible, code to cleanup zombies
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
   - everything between *targets*?
  - can still split, is not opaque, can analyse into
  - simplifies viz
  - does split/merge happen on the fly? reactive coalescing?
 - insert into pagerduty.alerts (to, body) select 'dp@cb.com', 'not enough things' where (
     select count(*) from (select null from things where ds = today() limit 5)) < 5
  - lol, system table of failures, insert into pagerduty.alerts select … from system.failures where table_name = ...
 - give everything a name? type:filename:line:col:seq?

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
import abc
import operator
import typing as ta

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import lang

from .. import metadata as md_
from ..types import QualifiedName
from ..utils.nodal import NodalDataclass
from ..utils import annotations as anns
from ..utils import serde


T = ta.TypeVar('T"')
RuleT = ta.TypeVar('RuleT', bound='Rule')


class Annotation(anns.Annotation, abstract=True):
    pass


class Annotations(anns.Annotations[Annotation]):

    @classmethod
    def _ann_cls(cls) -> ta.Type[Annotation]:
        return Annotation


class Target(dc.Enum, NodalDataclass['Target'], reorder=True):

    @classmethod
    def _nodal_cls(cls) -> ta.Type['Target']:
        return Target

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

    dc.check(lambda name, md: md is None or name == md.name)


class Rows(Target):
    table: QualifiedName = dc.field(coerce=QualifiedName.of)
    query: str = dc.field(check=lambda o: isinstance(o, str))

    name: ta.Optional[QualifiedName] = dc.field(None, coerce=QualifiedName.of_optional, kwonly=True)


class Function(Target):
    name: QualifiedName = dc.field(coerce=QualifiedName.of)


class Rule(Target, abstract=True):
    pass


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
        self._target_sets_by_type: ta.Dict[type, ta.AbstractSet[Target]] = {}

    @classmethod
    def of(cls, it: ta.Iterable[Target]) -> 'TargetSet':
        if isinstance(it, cls):
            return it
        else:
            return cls(it)

    def get_target_type_set(self, ty: ta.Type[T]) -> ta.AbstractSet[T]:
        try:
            return self._target_sets_by_type[ty]
        except KeyError:
            ret = self._target_sets_by_type[ty] = ocol.IdentitySet(n for n in self._targets if isinstance(n, ty))
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


class TargetProcessor(lang.Abstract):

    @abc.abstractmethod
    def matches(self, targets: TargetSet) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def process(self, targets: TargetSet) -> TargetSet:
        raise NotImplementedError


class RuleProcessor(lang.Abstract, ta.Generic[RuleT]):

    @abc.abstractproperty
    def rule_cls(self) -> ta.Type[RuleT]:
        raise NotImplementedError

    @abc.abstractmethod
    def process(self, rule: RuleT) -> ta.Iterable[Target]:
        raise NotImplementedError


class RuleTargetProcessor(TargetProcessor, ta.Generic[RuleT]):

    def __init__(self, proc: RuleProcessor[RuleT]) -> None:
        super().__init__()

        self._proc = check.isinstance(proc, RuleProcessor)

    def matches(self, targets: TargetSet) -> bool:
        return any(isinstance(t, self._proc.rule_cls) for t in targets)

    def process(self, targets: TargetSet) -> TargetSet:
        lst = []
        for tar in targets:
            if isinstance(tar, self._proc.rule_cls):
                for sub in self._proc.process(tar):
                    if Origin not in sub.anns:
                        sub = dc.replace(sub, anns={**sub.anns, Origin: Origin(tar)})
                    lst.append(sub)
            else:
                lst.append(tar)
        return TargetSet.of(lst)
