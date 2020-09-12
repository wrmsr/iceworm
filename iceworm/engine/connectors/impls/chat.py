"""
TODO:
 - slack, irc
 - omni's iface?
 - schema: 2-deep max from sqla
  - channels table, messages table
 - send only on commit
  - could update/del then lol
   - how to combine with reads?
  - provided by a buffering conn wrapper (heap?)
"""
import typing as ta

from omnibus import check

from .... import metadata as md
from ....types import QualifiedName
from ..base import Connection as _Connection
from ..base import Connector as _Connector
from ..base import RowSink
from ..base import RowSource


class ChatConnector(_Connector['ChatConnector', 'ChatConnector.Config']):

    class Config(_Connector.Config):
        pass

    def __init__(self, config: Config) -> None:
        super().__init__(check.isinstance(config, ChatConnector.Config))

    def connect(self) -> 'ChatConnection':
        return ChatConnection(self)


class ChatConnection(_Connection[ChatConnector]):

    def __init__(self, connector: ChatConnector) -> None:
        super().__init__(connector)

    def create_row_source(self, query: str) -> RowSource:
        raise TypeError

    def create_row_sink(self, table: QualifiedName) -> RowSink:
        raise TypeError

    def _reflect(self, names: ta.Optional[ta.Iterable[QualifiedName]] = None) -> ta.Mapping[QualifiedName, md.Object]:
        return {}
