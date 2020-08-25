import textwrap

from .. import nodes as no
from .. import parsing
from .. import rendering
from .. import tokens as toks
from ...utils import serde


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
