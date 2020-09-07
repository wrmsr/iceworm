"""
TODO:
  - quoting - of_dottable
  - disable Code unless explicitly enabled lols
"""
import abc
import collections.abc
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import properties

from .utils import seq
from .utils import serde


class QualifiedName(dc.Pure, ta.Sequence[str]):
    parts: ta.Sequence[str] = dc.field(coerce=seq)

    dc.check(lambda parts: (
            parts and
            all(parts) and
            all(isinstance(p, str) for p in parts)
    ))

    def __repr__(self) -> str:
        return 'QualifiedName([%s])' % (', '.join(map(repr, self.parts)),)

    @property
    def dotted(self) -> str:
        return '.'.join(self.parts)

    def prefixed(self, sz: int) -> ta.Sequence[ta.Optional[str]]:
        if len(self) > sz:
            raise ValueError(self)
        return ((None,) * (sz - len(self))) + tuple(self.parts)

    @property
    def pair(self) -> ta.Tuple[ta.Optional[str], str]:
        return self.prefixed(2)  # noqa

    @property
    def triple(self) -> ta.Tuple[ta.Optional[str], ta.Optional[str], str]:
        return self.prefixed(3)  # noqa

    @property
    def quad(self) -> ta.Tuple[ta.Optional[str], ta.Optional[str], ta.Optional[str], str]:
        return self.prefixed(4)  # noqa

    def __iter__(self) -> ta.Iterator[str]:
        return iter(self.parts)

    def __len__(self) -> int:
        return len(self.parts)

    def __getitem__(self, idx: int) -> str:
        return self.parts[idx]

    @classmethod
    def of_dotted(cls, dotted: str) -> 'QualifiedName':
        return cls(dotted.split('.'))

    @classmethod
    def of(cls, obj: ta.Union['QualifiedName', ta.Iterable[str]]) -> 'QualifiedName':
        if isinstance(obj, QualifiedName):
            return obj
        elif isinstance(obj, str):
            raise TypeError(obj)
        elif isinstance(obj, collections.abc.Iterable):
            return cls(list(obj))
        else:
            raise TypeError(obj)

    @classmethod
    def of_optional(cls, obj: ta.Union[None, 'QualifiedName', ta.Iterable[str]]) -> ta.Optional['QualifiedName']:
        if obj is None:
            return None
        else:
            return cls.of(obj)


class QualifiedNameSerde(serde.AutoSerde[QualifiedName]):

    def serialize(self, obj: QualifiedName) -> ta.Any:
        return check.isinstance(obj, QualifiedName).parts

    def deserialize(self, ser: ta.Any) -> QualifiedName:
        return QualifiedName.of(ser)


class Code(dc.Enum):

    @abc.abstractproperty
    def fn(self) -> ta.Callable:
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


class Lambda(Code, allow_setattr=True):
    src: str = dc.field(check=lambda s: isinstance(s, str) and ':' in s)

    @properties.cached
    def fn(self) -> ta.Callable:
        return eval('lambda ' + self.src)


class LambdaSerde(serde.AutoSerde[Lambda]):

    def serialize(self, obj: Lambda) -> ta.Any:
        return serde.serialize_dataclass_fields(obj)

    def deserialize(self, ser: ta.Any) -> Lambda:
        if isinstance(ser, str):
            return Lambda(ser)
        return serde.deserialize_dataclass_fields(ser, Lambda)
