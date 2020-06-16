import glob
import os.path

from omnibus import antlr
from omnibus._vendor import antlr4

from .._antlr.SnowflakeSqlLexer import SnowflakeSqlLexer
from .._antlr.SnowflakeSqlParser import SnowflakeSqlParser
from .._antlr.SnowflakeSqlVisitor import SnowflakeSqlVisitor


def test_iceworm():
    class _ParseVisitor(SnowflakeSqlVisitor):

        def visitStatement(self, ctx: SnowflakeSqlParser.StatementContext):
            return super().visitStatement(ctx)

    for file_path in glob.glob(os.path.join(os.path.dirname(__file__), 'sql', '*.sql'), recursive=True):
        print(file_path)
        with open(file_path, 'r') as f:
            lines = f.read()
        print(lines)

        for line in lines.splitlines():
            lexer = SnowflakeSqlLexer(antlr4.InputStream(line))
            lexer.removeErrorListeners()
            lexer.addErrorListener(antlr.SilentRaisingErrorListener())

            stream = antlr4.CommonTokenStream(lexer)
            stream.fill()

            parser = SnowflakeSqlParser(stream)
            parser.removeErrorListeners()
            parser.addErrorListener(antlr.SilentRaisingErrorListener())

            visitor = _ParseVisitor()
            node = visitor.visit(parser.singleStatement())
            print(node)
