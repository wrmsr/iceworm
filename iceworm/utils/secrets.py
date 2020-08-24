import abc
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from .utils import unique_dict


class SecretKey(dc.Pure):
    key: str


class Secret(dc.Enum):

    @abc.abstractproperty
    def value(self) -> str:
        raise NotImplementedError

    def __call__(self) -> str:
        return self.value


class KeyedSecret(Secret):
    key: str = dc.field(check=lambda o: isinstance(o, str))
    value: str = dc.field(repr=False, check=lambda o: isinstance(o, str))


class ProvidedSecret(Secret):
    value: str = dc.field(repr=False, check=lambda o: isinstance(o, str))
    src: ta.Any = dc.field(None)


class ComputedSecret(Secret):
    fn: ta.Callable[[], str] = dc.field(check=callable)

    @property
    def value(self) -> str:
        return self.fn()


class Secrets:

    def __init__(self, dct: ta.Mapping[str, str]) -> None:
        super().__init__()

        self._dct = unique_dict((check.isinstance(k, str), check.isinstance(v, str)) for k, v in dct.items())

    def __getitem__(self, key: ta.Union[Secret, SecretKey, str]) -> Secret:
        if isinstance(key, Secret):
            return key
        elif isinstance(key, SecretKey):
            try:
                value = self._dct[key.key]
            except KeyError:
                raise
            else:
                return KeyedSecret(key.key, value)
        elif isinstance(key, str):
            return ProvidedSecret(key)
        else:
            raise TypeError(key)
