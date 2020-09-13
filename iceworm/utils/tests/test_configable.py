import typing as ta

from .. import configable as cfgabl


ThingConfigT = ta.TypeVar('ThingConfigT', bound='Thing.Config')


class Thing(cfgabl.Configable[ThingConfigT]):
    class Config(cfgabl.Configable.Config):
        pass


class AThing(Thing['AThing.Config']):
    class Config(Thing.Config):
        pass


class BThing(Thing['BThing.Config']):
    class Config(Thing.Config):
        pass


def test_configable():
    pass
