"""
TODO:
 - slack, irc
 - omni's iface?
 - schema: 2-deep max from sqla
  - channels table, messages table
"""
import typing as ta

from omnibus import check

from ... import metadata as md
from ...types import QualifiedName
from .connectors import Connection
from .connectors import Connector
from .connectors import RowSink
from .connectors import RowSource


class ChatConnector(Connector['ChatConnector', 'ChatConnector.Config']):

    class Config(Connector.Config):
        pass

    def __init__(self, config: Config) -> None:
        super().__init__(check.isinstance(config, ChatConnector.Config))

    def connect(self) -> 'ChatConnection':
        return ChatConnection(self)


class ChatConnection(Connection[ChatConnector]):

    def __init__(self, connector: ChatConnector) -> None:
        super().__init__(connector)

    def create_row_source(self, query: str) -> RowSource:
        raise TypeError

    def create_row_sink(self, table: QualifiedName) -> RowSink:
        raise TypeError

    def _reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        return {}
