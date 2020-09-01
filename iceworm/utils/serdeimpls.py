import datetime
import typing as ta
import uuid

from .serde import AutoSerde


class BytesSerde(AutoSerde[bytes]):

    def serialize(self, obj: bytes) -> ta.Any:
        raise NotImplementedError

    def deserialize(self, ser: ta.Any) -> bytes:
        raise NotImplementedError


class DateSerde(AutoSerde[datetime.date]):

    def serialize(self, obj: datetime.date) -> ta.Any:
        raise NotImplementedError

    def deserialize(self, ser: ta.Any) -> datetime.date:
        raise NotImplementedError


class TimeSerde(AutoSerde[datetime.time]):

    def serialize(self, obj: datetime.time) -> ta.Any:
        raise NotImplementedError

    def deserialize(self, ser: ta.Any) -> datetime.time:
        raise NotImplementedError


class DatetimeSerde(AutoSerde[datetime.datetime]):

    def serialize(self, obj: datetime.datetime) -> ta.Any:
        raise NotImplementedError

    def deserialize(self, ser: ta.Any) -> datetime.datetime:
        raise NotImplementedError


class UuidSerde(AutoSerde[uuid.UUID]):

    def serialize(self, obj: uuid.UUID) -> ta.Any:
        raise NotImplementedError

    def deserialize(self, ser: ta.Any) -> uuid.UUID:
        raise NotImplementedError
