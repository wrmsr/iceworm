import glob
import json  # noqa
import os.path
import textwrap

from .. import nodes as no
from .. import parsing
from .. import rendering
from .. import tokens as toks
from ...utils import serde


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

            hash(node)

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

            assert hash(reparsed) == hash(node)

            # parts = rendering.Renderer().render(node)
            # parts_ser = serde.serialize(parts)
            # print(json.dumps(parts_ser, indent=4))

            print()


def test_comments():
    for sql in [
        (
            '/* 0 */ select /* 1 */ a /* 2 */, /* 3 */ b '
            '/* 4 */ from /* 5 */ t '
            '/* 6 */ where /* 7 */ x /* 8 */ = /* 9 */ 1 /* 10 */'
        ),
        textwrap.dedent("""
        -- before select
        select
            a, -- this is a
            -- this is before b
            b  -- this is b
        -- before from
        from
            t -- this is t
        -- end
       """),
    ]:
        root = parsing.parse_statement(sql)
        print(root)

        ser = serde.serialize(root)  # noqa
        des = serde.deserialize(ser, no.Node)  # noqa
        # assert des == node

        rendered = rendering.render(root)
        print(rendered)

        reparsed = parsing.parse_statement(rendered + ';')
        assert reparsed == root

        tok_ana = toks.TokenAnalysis(root)
        print(tok_ana.get_node_comments(root))

        class NodePartTransform(rendering.PartTransform):

            def __call__(self, part: rendering.Node) -> rendering.Part:
                print(part)
                return super().__call__(part)

        part = rendering.Renderer()(root)
        part = NodePartTransform()(part)
        part = rendering.compact_part(part)

        import io
        buf = io.StringIO()
        rendering.render_part(part, buf)
        print(buf.getvalue())
