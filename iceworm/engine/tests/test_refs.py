import typing as ta
import weakref

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang
import pytest


T = ta.TypeVar('T')
Self = ta.TypeVar('Self"')


_REF_CLS_CACHE: ta.MutableMapping[type, ta.Type['Ref']] = weakref.WeakKeyDictionary()


class Ref(dc.Frozen, ta.Generic[T]):
    name: str = dc.field(check=lambda o: isinstance(o, str) and o)

    ref_cls: ta.ClassVar[type]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        check.isinstance(cls.ref_cls, type)
        check.state(lang.Final in cls.__bases__)
        rc = cls.ref_cls
        check.not_in(rc, _REF_CLS_CACHE)
        _REF_CLS_CACHE[rc] = cls

    def __class_getitem__(cls, arg: type) -> type:
        check.isinstance(arg, type)
        try:
            ret = _REF_CLS_CACHE[arg]
        except KeyError:
            bc = super().__class_getitem__(arg)
            ns = {
                '__module__': __package__ + '.' + __name__,
                'ref_cls': arg,
                '__class_getitem__': ta.Generic.__class_getitem__,
            }
            ret = lang.new_type(
                f'{cls.__name__}[{arg.__name__}]',
                (bc, lang.Final),
                ns,
            )
        check.state(_REF_CLS_CACHE[arg] is ret)
        return ret

    @classmethod
    def cls(cls, arg: type) -> type:
        return cls[arg]

    @classmethod
    def of(cls: ta.Type[Self], arg: ta.Union['Ref', str]) -> Self:
        if isinstance(arg, str):
            return cls(arg)
        elif type(arg) is cls:
            return arg
        else:
            raise TypeError(arg)


class Thing(dc.Pure):
    ref: Ref[int] = dc.field(coerce=Ref[int].of)


def test_ref():
    thing = Thing(Ref[int]('hi'))
    assert thing.ref.name == 'hi'

    thing = Thing('hi')
    assert thing.ref.name == 'hi'

    with pytest.raises(TypeError):
        thing = Thing(Ref[str]('hi'))  # noqa
