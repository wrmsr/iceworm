from omnibus.inject.dev.pytest import harness as har

from .. import objman
from ..postgres import PostgresAdapter
from .helpers import DbManager


def test_objman(harness: har.Harness):
    om = objman.ObjectManager(harness[DbManager].pg_engine, PostgresAdapter())
    assert om
