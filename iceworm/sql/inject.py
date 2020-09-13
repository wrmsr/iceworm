from omnibus import check
from omnibus import inject as inj

from .adapter import Adapter


def bind_adapter_factory(binder: inj.Binder, cls: ta.Type[Adapter]) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, Adapter)

    binder.bind_class(cls, assists={'config'})
    binder.new_dict_binder(ta.Type[Adapter.Config], ta.Callable[..., Connector]).bind(cls.Config, to_provider=ta.Callable[..., cls])  # noqa


def install(binder: inj.Binder) -> inj.Binder:
    check.isinstance(binder, inj.Binder)

    return binder
