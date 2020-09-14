from .. import objman
from ...tests import harness as har
from ..postgres import PostgresAdapter
from .helpers import DbManager


def test_objman(harness: har.Harness):
    om = objman.ObjectManager(harness[DbManager].pg_engine, PostgresAdapter())
    assert om
