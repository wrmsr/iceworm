"""
TODO:
 - scoping?
 - ** config field inspection like w/ eles... **
  - config field names get injected with their injected impls
  - just make configs nodal?
"""
import typing as ta
import weakref

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import inject as inj
from omnibus import lang


ConfigableT = ta.TypeVar('ConfigableT', bound='Configable')
ConfigableConfigT = ta.TypeVar('ConfigableConfigT', bound='Configable.Config')


_CFG_CLS_MAP: ta.Mapping[ta.Type['Configable.Config'], ta.Type['Configable']] = weakref.WeakValueDictionary()


class Configable(ta.Generic[ConfigableConfigT], lang.Abstract):

    class Config(lang.Abstract):
        def __init_subclass__(cls, **kwargs) -> None:
            super().__init_subclass__(**kwargs)
            check.state(cls.__name__ == 'Config')

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        cfg_cls = check.issubclass(cls.__dict__['Config'], Configable.Config)
        check.not_in(cfg_cls, _CFG_CLS_MAP)
        _CFG_CLS_MAP[cfg_cls] = cls

    def __init__(self, config: ConfigableConfigT) -> None:
        super().__init__()

        self._config: ConfigableConfigT = check.isinstance(config, self.Config)


def get_impl(cfg: ta.Union[ta.Type[Configable.Config], Configable.Config]) -> ta.Type[Configable]:
    if isinstance(cfg, type):
        cfg_cls = check.issubclass(cfg, Configable.Config)
    elif isinstance(cfg, Configable.Config):
        cfg_cls = type(cfg)
    else:
        raise TypeError(cfg)
    return _CFG_CLS_MAP[cfg_cls]


class _UNDERLYING(lang.Marker):
    pass


def bind_impl(binder: inj.Binder, cls: ta.Type[Configable], impl_cls: ta.Type[Configable]) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, Configable)
    check.issubclass(impl_cls, cls)

    impl_assists = {'config'}
    provider_kwargs = {
        '__factory': inj.Key(ta.Callable[..., impl_cls], _UNDERLYING),
    }

    if dc.is_dataclass(impl_cls.Config):
        for f in dc.fields(impl_cls.Config):
            if isinstance(f.type, type) and issubclass(f.type, Configable.Config):
                check.not_in(f.name, impl_assists)
                check.not_in(f.name, provider_kwargs)
                impl_assists.add(f.name)
                # FIXME: forward anns
                provider_kwargs[f.name] = inj.Key(ta.Callable[..., get_impl(f.type)])

    @inj.annotate(factory=_UNDERLYING)
    def provide(config, __factory, **kwargs) -> impl_cls:
        return __factory(config=config)

    binder.bind_class(impl_cls, key=inj.Key(impl_cls, _UNDERLYING), assists=impl_assists)
    binder.bind_callable(provide, assists={'config'}, kwargs=provider_kwargs)

    binder.new_dict_binder(ta.Type[cls.Config], ta.Callable[..., cls]).bind(impl_cls.Config, to_provider=ta.Callable[..., impl_cls])  # noqa


def bind_dict(binder: inj.Binder, cls: ta.Type[Configable]) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, Configable)

    binder.new_dict_binder(ta.Type[cls.Config], ta.Callable[..., cls])


def bind_factory(binder: inj.Binder, cls: ta.Type[Configable]) -> None:
    check.isinstance(binder, inj.Binder)
    check.issubclass(cls, Configable)

    bind_dict(binder, cls)

    def provide(
            config: cls.Config,
            facs: ta.Mapping[ta.Type[cls.Config], ta.Callable[..., cls]],
    ) -> cls:
        fac = facs[type(config)]
        return fac(config=config)

    binder.bind_callable(provide, assists={'config'})
