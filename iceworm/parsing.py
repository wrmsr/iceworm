from omnibus import antlr
from omnibus import check
from omnibus._vendor import antlr4

from . import nodes as no
from ._antlr.SnowflakeSqlLexer import SnowflakeSqlLexer
from ._antlr.SnowflakeSqlParser import SnowflakeSqlParser
from ._antlr.SnowflakeSqlVisitor import SnowflakeSqlVisitor


class _ParseVisitor(SnowflakeSqlVisitor):

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is not None:
            check.none(nextResult)
            return aggregate
        else:
            check.none(aggregate)
            return nextResult

    def visitSelectStatement(self, ctx: SnowflakeSqlParser.SelectStatementContext):
        items = [self.visit(i) for i in ctx.selectItem()]
        relations = [self.visit(r) for r in ctx.relation()]
        return no.Select(items, relations)

    def visitSelectItem(self, ctx: SnowflakeSqlParser.SelectItemContext):
        return no.SelectItem(self.visit(ctx.expression()))

    def visitRelation(self, ctx: SnowflakeSqlParser.RelationContext):
        return no.Table(ctx.identifier())

    def visitIdentifier(self, ctx: SnowflakeSqlParser.IdentifierContext):
        return no.Identifier(ctx.IDENTIFIER().getText())

    def visitNumber(self, ctx: SnowflakeSqlParser.NumberContext):
        return no.Integer(int(ctx.INTEGER_VALUE().getText()))


def parse_statement(buf: str) -> no.Node:
    lexer = SnowflakeSqlLexer(antlr4.InputStream(buf))
    lexer.removeErrorListeners()
    lexer.addErrorListener(antlr.SilentRaisingErrorListener())

    stream = antlr4.CommonTokenStream(lexer)
    stream.fill()

    parser = SnowflakeSqlParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(antlr.SilentRaisingErrorListener())

    visitor = _ParseVisitor()
    node = visitor.visit(parser.singleStatement())
    return check.isinstance(node, no.Node)
