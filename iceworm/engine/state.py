"""
TODO:
 - just gen from dc's
  - data is serde'd json, marked fields are cols, indexes added from class metadata
 - refs table?
  - want gc
   - no constraints but offline?
 - composite pk, world_id (just world?), auto-added when querying, prefixed in indices
 - _meta: revision, host, pid - same as query tags, likely more - world info
 - dc anns like nodal/serde, ignored for heap

tables:
 - worlds
 - targets
  - one per type?
  - invalidations?
   - ranges?
   - historical invalidations? pending? handled? cleared at max interval according to scheds?
"""
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
