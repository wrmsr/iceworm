from omnibus import check

from .. import connectors as ctrs
from .. import elements as els


def test_dual():
    elements = els.ElementSet.of([
        ctrs.dual.DualConnector.Config(),
    ])

    connectors = ctrs.ConnectorSet.of(elements.get_type_set(ctrs.Connector.Config))

    conn = check.isinstance(connectors['dual'], ctrs.dual.DualConnector).connect()
    rows = list(conn.create_row_source('select * from dual').produce_rows())
    assert rows == [{'dummy': 'x'}]
