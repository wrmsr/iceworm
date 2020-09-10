"""
TODO:
 - read docker-compose.yml
 - abstract project name
"""
import typing as ta

from omnibus import docker
from omnibus import lifecycles as lc
from omnibus import properties

from . import harness as har


@har.bind(har.Session, eager=True)
class DockerManager(lc.ContextManageableLifecycle):

    @properties.stateful_cached
    def client(self):
        return self._lifecycle_exit_stack.enter_context(docker.client_context())

    _container_tcp_endpoints = properties.cached(lambda self: {})

    def get_container_tcp_endpoints(
            self,
            name_port_pairs: ta.Iterable[ta.Tuple[str, int]],
    ) -> ta.Dict[ta.Tuple[str, int], ta.Tuple[str, int]]:
        if docker.is_in_docker():
            return {t: t for t in name_port_pairs}
        ret = {}
        lut = {}
        for h, p in name_port_pairs:
            try:
                ret[(h, p)] = self._container_tcp_endpoints[(h, p)]
            except KeyError:
                lut[(f'docker_{h}_1', p)] = (h, p)
        if lut:
            dct = docker.get_container_tcp_endpoints(self.client, lut)
            res = {lut[k]: v for k, v in dct.items()}
            ret.update(res)
            self._container_tcp_endpoints.update(res)
        return ret
