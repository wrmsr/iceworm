import abc

from omnibus import check
from omnibus import lang


class State(lang.Abstract):

    @abc.abstractmethod
    def get_object(self):
        raise NotImplementedError


class HeapState(State):

    def get_object(self):
        raise NotImplementedError


class SqlState(State):

    class Backend(lang.Abstract):
        pass

    class PostgresBackend(Backend):
        pass

    def __init__(self, backend: Backend) -> None:
        super().__init__()

        self._backend = check.isinstance(backend, SqlState.Backend)

    def get_object(self):
        raise NotImplementedError
