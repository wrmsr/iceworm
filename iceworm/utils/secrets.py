import abc
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc

from .utils import unique_dict


class SecretKey(dc.Pure):
    key: str


class SecretValue(dc.Enum):

    @abc.abstractproperty
    def value(self) -> str:
        raise NotImplementedError


class KeyedSecretValue(SecretValue):
    key: str
    value: str = dc.field(repr=False)


class ProvidedSecretValue(SecretValue):
    value: str = dc.field(repr=False)
    src: ta.Any = dc.field(None)


class Secrets:

    def __init__(self, dct: ta.Mapping[str, str]) -> None:
        super().__init__()

        self._dct = unique_dict((check.isinstance(k, str), check.isinstance(v, str)) for k, v in dct.items())

    def __getitem__(self, key: ta.Union[SecretValue, SecretKey, str]) -> SecretValue:
        if isinstance(key, SecretValue):
            return key
        elif isinstance(key, SecretKey):
            try:
                value = self._dct[key.key]
            except KeyError:
                raise
            else:
                return KeyedSecretValue(key.key, value)
        elif isinstance(key, str):
            return ProvidedSecretValue(key)
        else:
            raise TypeError(key)
