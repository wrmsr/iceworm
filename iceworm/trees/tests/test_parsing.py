import glob
import json  # noqa
import os.path
import typing as ta

from omnibus.antlr import ParseException
from omnibus import check
import pytest

from .. import nodes as no
from .. import parsing
from .. import rendering
from ...utils import serde
from .._antlr.IceSqlParser import IceSqlParserConfig


def _assert_query(query: str, *, config: ta.Optional[IceSqlParserConfig] = None) -> ta.Optional[no.Node]:
    query = query.strip(' \r\n;')
    if not query:
        return None

    print(query)

    node = parsing.parse_statement(query + ';', config=config)
    print(node)

    hash(node)

    ser = serde.serialize(node)  # noqa
    print(json.dumps(ser))
    des = serde.deserialize(ser, no.Node)  # noqa
    # assert des == node

    rendered = rendering.render(node)
    print(rendered)

    reparsed = parsing.parse_statement(rendered + ';', config=config)
    try:
        assert reparsed == node
    except Exception:
        raise

    assert hash(reparsed) == hash(node)

    # parts = rendering.Renderer().render(node)
    # parts_ser = serde.serialize(parts)
    # print(json.dumps(parts_ser, indent=4))

    print()

    return node


def test_parsing():
    file_paths = sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'sql', '*.sql'), recursive=True))

    for file_path in file_paths:
        print(file_path)

        with open(file_path, 'r') as f:
            lines = f.read()

        for line in lines.split(';'):
            line = line.strip()
            if not line or line.startswith('--'):
                continue

            _assert_query(line)


def test_minor():
    print(parsing.parse_expr('1'))
    print(parsing.parse_expr('2 * f(a + b.c)'))

    print(parsing.parse_col_spec('id integer'))
    print(parsing.parse_col_spec('name varchar(420)'))

    print(parsing.parse_type_spec('integer'))
    print(parsing.parse_type_spec('varchar(420)'))


def test_interval_units():
    for iv in [False, True]:
        cfg = IceSqlParserConfig(interval_units=iv)

        if not iv:
            _assert_query("select interval '3 day'", config=cfg)
        else:
            with pytest.raises(ParseException):
                _assert_query("select interval '3 day'", config=cfg)

        _assert_query("select interval 3 day", config=cfg)

        n = check.isinstance(_assert_query("select interval '3' day", config=cfg), no.Select)
        it = check.isinstance(check.isinstance(n, no.Select).items[0], no.ExprSelectItem)
        ie = check.isinstance(it.value, no.Interval)
        if not iv:
            assert check.isinstance(it.label, no.Identifier).name == 'day'
            assert ie.unit is None
        else:
            assert it.label is None
            assert ie.unit == no.IntervalUnit.DAY
