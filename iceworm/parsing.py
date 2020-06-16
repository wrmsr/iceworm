from omnibus import antlr
from omnibus import check
from omnibus import lang
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

    def visitBinaryBooleanExpression(self, ctx: SnowflakeSqlParser.BinaryBooleanExpressionContext):
        left, right = [self.visit(e) for e in ctx.booleanExpression()]
        op = lang.parse_enum(ctx.op.text.upper(), no.BinaryOp)
        return no.BinaryExpr(left, op, right)

    def visitFunctionCall(self, ctx: SnowflakeSqlParser.FunctionCallContext):
        name = self.visit(ctx.identifier())
        args = [self.visit(a) for a in ctx.expression()]
        return no.FunctionCall(name, args)

    def visitGroupBy(self, ctx: SnowflakeSqlParser.GroupByContext):
        exprs = [self.visit(e) for e in ctx.expression()]
        return no.GroupBy(exprs)

    def visitIdentifier(self, ctx: SnowflakeSqlParser.IdentifierContext):
        return no.Identifier(ctx.IDENTIFIER().getText())

    def visitIntegerNumber(self, ctx: SnowflakeSqlParser.IntegerNumberContext):
        return no.Integer(int(ctx.INTEGER_VALUE().getText()))

    def visitJoinRelation(self, ctx: SnowflakeSqlParser.JoinRelationContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        condition = self.visit(ctx.condition) if ctx.condition is not None else None
        return no.Join(left, right, condition)

    def visitNull(self, ctx: SnowflakeSqlParser.NullContext):
        return no.Null()

    def visitSelectItem(self, ctx: SnowflakeSqlParser.SelectItemContext):
        expr = self.visit(ctx.expression())
        label = self.visit(ctx.identifier()) if ctx.identifier() is not None else None
        return no.SelectItem(expr, label)

    def visitSelectStatement(self, ctx: SnowflakeSqlParser.SelectStatementContext):
        items = [self.visit(i) for i in ctx.selectItem()]
        relations = [self.visit(r) for r in ctx.relation()]
        where = self.visit(ctx.where) if ctx.where is not None else None
        group_by = self.visit(ctx.groupBy()) if ctx.groupBy() else None
        return no.Select(items, relations, where, group_by)

    def visitTableRelation(self, ctx: SnowflakeSqlParser.TableRelationContext):
        return no.Table(self.visit(ctx.identifier()))

    def visitUnaryBooleanExpression(self, ctx: SnowflakeSqlParser.UnaryBooleanExpressionContext):
        op = lang.parse_enum(ctx.op.text.upper(), no.UnaryOp)
        value = self.visit(ctx.booleanExpression())
        return no.UnaryExpr(op, value)


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
