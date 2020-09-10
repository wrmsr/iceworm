import typing as ta

from omnibus import docker
from omnibus import lifecycles as lc
from omnibus import properties

from . import harness as har


@har.bind(har.Session, eager=True)
class DockerManager(lc.ContextManageableLifecycle):

    def __init__(self) -> None:
        super().__init__()

        self._client = None

    @properties.stateful_cached
    def client(self):
        return self._lifecycle_exit_stack.enter_context(docker.client_context())

    def get_container_tcp_endpoints(
            self,
            name_port_pairs: ta.Iterable[ta.Tuple[str, int]],
    ) -> ta.Dict[ta.Tuple[str, int], ta.Tuple[str, int]]:
        return docker.get_container_tcp_endpoints(self.client, name_port_pairs)
