from omnibus.inject.dev import pytest as ptinj

from .. import objman
from ..postgres import PostgresAdapter
from .helpers import DbManager


def test_objman(harness: ptinj.Harness):
    om = objman.ObjectManager(harness[DbManager].pg_engine, PostgresAdapter())
    assert om
