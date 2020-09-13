"""
TODO:
 - ensure nodal interop
 - injection helper
"""
import typing as ta
import weakref

from omnibus import check
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

        if lang.Abstract not in cls.__bases__:
            cfg_cls = check.issubclass(cls.__dict__['Config'], Configable.Config)
            check.not_in(cfg_cls, _CFG_CLS_MAP)
            _CFG_CLS_MAP[cfg_cls] = cls

    def __init__(self, config: ConfigableConfigT) -> None:
        super().__init__()

        self._config: ConfigableConfigT = check.isinstance(config, self.Config)
