import glob
import json  # noqa
import os.path
import textwrap

from .. import nodes as no
from .. import parsing
from .. import rendering
from .. import serde


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

            print(line)

            node = parsing.parse_statement(line + ';')
            print(node)

            ser = serde.serialize(node)  # noqa
            des = serde.deserialize(ser, no.Node)  # noqa
            # assert des == node

            rendered = rendering.render(node)
            print(rendered)

            reparsed = parsing.parse_statement(rendered + ';')
            try:
                assert reparsed == node
            except Exception:
                raise

            # parts = rendering.Renderer().render(node)
            # parts_ser = serde.serialize(parts)
            # print(json.dumps(parts_ser, indent=4))

            print()


def test_comments():
    sql = textwrap.dedent("""
    -- before select
    select
        a, -- this is a
        -- this is before b
        b  -- this is b
    -- before from
    from
        t -- this is t
    -- end
    """)

    node = parsing.parse_statement(sql)
    print(node)

    ser = serde.serialize(node)  # noqa
    des = serde.deserialize(ser, no.Node)  # noqa
    # assert des == node

    rendered = rendering.render(node)
    print(rendered)

    reparsed = parsing.parse_statement(rendered + ';')
    assert reparsed == node

    import collections.abc

    def rec(part: rendering.Part):
        if isinstance(part, str):
            return part
        elif isinstance(part, collections.abc.Sequence):
            return [rec(c) for c in part]
        elif isinstance(part, rendering.Paren):
            return rendering.Paren(rec(part.part))
        elif isinstance(part, rendering.List):
            return rendering.List([rec(c) for c in part.parts], part.delimiter)
        elif isinstance(part, rendering.Concat):
            return rendering.Concat([rec(c) for c in part.parts])
        elif isinstance(part, rendering.Node):
            return []
        else:
            raise TypeError(part)

    part = rendering.compact_part(rendering.Renderer()(node))
    rpart = rec(part)

    import io
    buf = io.StringIO()
    rendering.render_part(rpart, buf)
    print(buf.getvalue())
