import typing as ta

from omnibus import dataclasses as dc

from ...utils import seq
from .base import Identifier
from .base import Node
from .base import QualifiedNameNode
from .base import Stmt
from .base import TypeSpec


class ColSpec(Node):
    name: Identifier
    type: TypeSpec


class CreateTable(Stmt):
    name: QualifiedNameNode
    cols: ta.Sequence[ColSpec] = dc.field(coerce=seq)


class Insert(Stmt):
    name: QualifiedNameNode
