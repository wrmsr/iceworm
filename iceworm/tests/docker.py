"""
TODO:
 - abstract project name
"""
import os.path
import typing as ta

from omnibus import check
from omnibus import docker
from omnibus import lifecycles as lc
from omnibus import properties
import yaml

from . import harness as har


@har.bind(har.Session)
class DockerManager(lc.ContextManageableLifecycle):

    def __init__(self, *, request: ta.Optional[har.FixtureRequest] = None) -> None:
        super().__init__()

        self._request = check.isinstance(request, (har.FixtureRequest, None))

    PREFIX = 'iceworm-'

    @properties.stateful_cached
    def client(self):
        return self._lifecycle_exit_stack.enter_context(docker.client_context())

    _container_tcp_endpoints = properties.cached(lambda self: {})

    def get_container_tcp_endpoints(
            self,
            name_port_pairs: ta.Iterable[ta.Tuple[str, int]],
    ) -> ta.Dict[ta.Tuple[str, int], ta.Tuple[str, int]]:
        if docker.is_in_docker():
            return {(h, p): (self.PREFIX + h, p) for h, p in name_port_pairs}
        ret = {}
        lut = {}
        for h, p in name_port_pairs:
            try:
                ret[(h, p)] = self._container_tcp_endpoints[(h, p)]
            except KeyError:
                lut[(f'docker_{self.PREFIX}{h}_1', p)] = (h, p)
        if lut:
            dct = docker.get_container_tcp_endpoints(self.client, lut)
            res = {lut[k]: v for k, v in dct.items()}
            ret.update(res)
            self._container_tcp_endpoints.update(res)
        return ret

    @properties.cached
    @property
    def compose_config(self) -> ta.Mapping[str, ta.Any]:
        with open(os.path.join(os.path.dirname(__file__), '../../docker/docker-compose.yml'), 'r') as f:
            buf = f.read()
        dct = yaml.safe_load(buf)
        ret = {}
        for n, c in dct['services'].items():
            check.state(n.startswith(self.PREFIX))
            ret[n[len(self.PREFIX):]] = c
        return ret
