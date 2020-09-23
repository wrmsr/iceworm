"""
TODO:
 - deeper ref checking lol
"""
import abc

from omnibus import check
from omnibus import dataclasses as dc
from omnibus import lang

from .collections import Analysis
from .refs import Ref


class Validation(Analysis, lang.Abstract):

    def __post_init__(self, *args, **kwargs) -> None:
        super().__post_init__(*args, **kwargs)
        self.validate()

    @abc.abstractmethod
    def validate(self) -> None:
        raise NotImplementedError


class RefValidation(Validation):

    def validate(self) -> None:
        for e in self.elements:
            for f in dc.fields(e):
                if isinstance(f.type, type) and issubclass(f.type, Ref):
                    ref = getattr(e, f.name)
                    check.in_(ref, self.elements)
