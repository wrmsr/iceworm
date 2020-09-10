import typing as ta

from omnibus import check
from omnibus import docker
from omnibus import lifecycles as lc

from . import harness as har


@har.bind(har.Session)
class DockerManager(lc.ContextManageableLifecycle):

    def __init__(self) -> None:
        super().__init__()

        self._client = None

    @property
    def client(self):
        check.state(self.is_lifecycle_started)
        if self._client is None:
            self._client = docker.get_client()
        return self._client

    def get_container_tcp_endpoints(
            self,
            name_port_pairs: ta.Iterable[ta.Tuple[str, int]],
    ) -> ta.Dict[ta.Tuple[str, int], ta.Tuple[str, int]]:
        return docker.get_container_tcp_endpoints(self.client, name_port_pairs)

    def _do_lifecycle_stop(self) -> None:
        if self._client is not None:
            docker.close_client(self._client)
            self._client = None
