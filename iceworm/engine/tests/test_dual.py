import typing as ta

from omnibus import check
import yaml

from .. import connectors as ctrs
from .. import elements as els
from ...utils import serde


ELEMENTS_YML = """

- dual_connector: {}

"""

ELEMENTS_SER = yaml.safe_load(ELEMENTS_YML)


def test_dual():
    elements = els.ElementSet.of(serde.deserialize(ELEMENTS_SER, ta.Sequence[els.Element]))

    connectors = ctrs.ConnectorSet.of(elements.get_type_set(ctrs.Connector.Config))

    conn = check.isinstance(connectors['dual'], ctrs.dual.DualConnector).connect()
    rows = list(conn.create_row_source('select * from dual').produce_rows())
    assert rows == [{'dummy': 'x'}]
