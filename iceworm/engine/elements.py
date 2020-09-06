"""
TODO:
 - ** s/name/id/? **
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
import functools
import operator
import typing as ta
import weakref

from omnibus import check
from omnibus import collections as ocol
from omnibus import dataclasses as dc
from omnibus import lang

from ..utils.nodal import NodalDataclass
from ..utils import annotations as anns
from ..utils import serde


T = ta.TypeVar('T"')
ElementT = ta.TypeVar('ElementT', bound='Element')
Self = ta.TypeVar('Self"')
Name = str


def name_check(obj: ta.Any) -> bool:
    return isinstance(obj, str) and obj


def optional_name_check(obj: ta.Any) -> bool:
    return obj is None or (isinstance(obj, str) and obj)


class Annotation(anns.Annotation, abstract=True):
    pass


class Annotations(anns.Annotations[Annotation]):

    @classmethod
    def _ann_cls(cls) -> ta.Type[Annotation]:
        return Annotation


class Element(dc.Enum, NodalDataclass['Element'], reorder=True):

    @classmethod
    def _nodal_cls(cls) -> ta.Type['Element']:
        return Element

    anns: Annotations = dc.field(
        (),
        kwonly=True,
        repr=False,
        hash=False,
        compare=False,
        coerce=Annotations,
        metadata={serde.Ignore: operator.not_},
    )

    name: ta.Optional[str] = dc.field(None, check=optional_name_check, kwonly=True)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        nf = dc.fields_dict(cls)['name']
        check.state(nf.type in (str, ta.Optional[str]))


_REF_CLS_CACHE: ta.MutableMapping[type, ta.Type['Ref']] = weakref.WeakKeyDictionary()


@functools.total_ordering
class Ref(dc.Frozen, ta.Generic[ElementT], repr=False, eq=False, order=False):
    name: Name = dc.field(check=name_check)

    ele_cls: ta.ClassVar[type]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name!r})'

    __str__ = __repr__

    def __eq__(self, other: ta.Any) -> bool:
        if type(other) is not type(self):
            raise TypeError(other)
        return self.name == other.name

    def __lt__(self, other: ta.Any) -> bool:
        if type(other) is not type(self):
            raise TypeError(other)
        return self.name < other.name

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()

        check.isinstance(cls.ele_cls, type)
        check.issubclass(cls.ele_cls, Element)
        check.state(lang.Final in cls.__bases__)
        rc = cls.ele_cls
        check.not_in(rc, _REF_CLS_CACHE)
        _REF_CLS_CACHE[rc] = cls

        class _RefSerde(serde.AutoSerde[cls]):  # noqa
            _bind = cls

            def serialize(self, obj: Ref) -> ta.Any:
                return check.isinstance(obj, cls).name

            def deserialize(self, ser: ta.Any) -> Ref:
                return cls(check.isinstance(ser, Name))

    def __class_getitem__(cls, arg: type) -> type:
        check.isinstance(arg, type)
        try:
            ret = _REF_CLS_CACHE[arg]
        except KeyError:
            bc = super().__class_getitem__(arg)
            ns = {
                'ele_cls': arg,
                '__class_getitem__': ta.Generic.__class_getitem__,
            }
            ret = lang.new_type(
                f'{cls.__name__}[{arg.__name__}]',
                (bc, lang.Final),
                ns,
                repr=False,
                eq=False,
                order=False,
            )
        check.state(_REF_CLS_CACHE[arg] is ret)
        return ret

    @classmethod
    def cls(cls: ta.Type[Self], arg: type) -> ta.Type[Self]:
        return cls[arg]

    @classmethod
    def of(cls: ta.Type[Self], obj: ta.Union['Ref', Name]) -> Self:
        if type(obj) is cls:
            return obj
        elif isinstance(obj, Name):
            return cls(obj)
        else:
            raise TypeError(obj)


class Origin(Annotation):
    element: Element


class ElementSet:

    def __init__(self, elements: ta.Iterable[Element]) -> None:
        super().__init__()

        self._elements = [check.isinstance(e, Element) for e in elements]

        self._element_set = ocol.IdentitySet(self._elements)
        by_name: ta.Dict[Name, Element] = {}
        for element in self._elements:
            if element.name is not None:
                check.not_in(element.name, by_name)
                by_name[element.name] = element
        self._elements_by_name: ta.Mapping[Name, Element] = by_name
        self._element_sets_by_type: ta.Dict[type, ta.AbstractSet[Element]] = {}

    @classmethod
    def of(cls, it: ta.Iterable[Element]) -> 'ElementSet':
        if isinstance(it, cls):
            return it
        else:
            return cls(it)

    def get_element_type_set(self, ty: ta.Type[T]) -> ta.AbstractSet[T]:
        try:
            return self._element_sets_by_type[ty]
        except KeyError:
            ret = self._element_sets_by_type[ty] = ocol.IdentitySet(n for n in self._elements if isinstance(n, ty))
            return ret

    def __iter__(self) -> ta.Iterator[Element]:
        return iter(self._elements)

    def __contains__(self, key: ta.Union[Name, Element, type]) -> bool:
        if isinstance(key, Name):
            return key in self._elements_by_name
        elif isinstance(key, Element):
            return key in self._element_set
        elif isinstance(key, type):
            return bool(self.get_element_type_set(key))
        else:
            raise TypeError(key)

    def __getitem__(self, name: Name) -> Element:
        return self._elements_by_name[check.isinstance(name, Name)]


class ElementProcessor(lang.Abstract):

    @abc.abstractmethod
    def matches(self, elements: ElementSet) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def process(self, elements: ElementSet) -> ElementSet:
        raise NotImplementedError
