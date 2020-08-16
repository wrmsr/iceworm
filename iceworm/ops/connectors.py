"""
TODO:
 - virtual vs physical tables
 - physical tables requiring refresh
 - incremental vs total physical tables
 - materialized vs unmaterialized virtuals

Def conns:
 - kafka
 - dynamo
 - system

Alt conns:
 - salesforce
 - pagerduty
 - jira
"""
import typing as ta

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import defs
from omnibus import lang
import sqlalchemy as sa

from ..utils import unique_dict


class Connector(lang.Abstract):

    def __init__(self, name: str) -> None:
        super().__init__()

        self._name = check.not_empty(check.isinstance(name, str))

    defs.repr('name')

    @property
    def name(self) -> str:
        return self._name


class SqlConnector(Connector):
    """
    postgres/mysql/snowflake
    """

    class Config(dc.Frozen):
        url: str

    def __init__(self, name: str, config: Config) -> None:
        super().__init__(name)

        self._config = check.isinstance(config, SqlConnector.Config)

    def create_engine(self, **kwargs) -> sa.engine.Engine:
        return sa.create_engine(self._config.url, **kwargs)


class FileConnector(Connector):
    """
    local/s3/url/sftp?
    csv/json/yaml/parquet
    """

    def __init__(self, name: str, file_path: str) -> None:
        super().__init__(name)

        self._file_path = file_path

    @property
    def file_path(self) -> str:
        return self._file_path


class MongoConnector(Connector):
    pass


class ConnectorSet(ta.Iterable[Connector]):

    def __init__(self, connectors: ta.Iterable[Connector]) -> None:
        super().__init__()

        self._connectors = list(connectors)
        self._connectors_by_name = unique_dict((c.name, c) for c in self._connectors)

    def __iter__(self) -> ta.Iterator[Connector]:
        return iter(self._connectors)

    def __getitem__(self, name: str) -> Connector:
        return self._connectors_by_name[name]
