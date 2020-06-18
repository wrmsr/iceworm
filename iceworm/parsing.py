from omnibus import antlr
from omnibus import check
from omnibus._vendor import antlr4

from . import nodes as no
from ._antlr.SnowflakeSqlLexer import SnowflakeSqlLexer
from ._antlr.SnowflakeSqlParser import SnowflakeSqlParser
from ._antlr.SnowflakeSqlVisitor import SnowflakeSqlVisitor
from .quoting import unquote


class _ParseVisitor(SnowflakeSqlVisitor):

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is not None:
            check.none(nextResult)
            return aggregate
        else:
            check.none(aggregate)
            return nextResult

    def visitAllSelectItem(self, ctx: SnowflakeSqlParser.AllSelectItemContext):
        return no.AllSelectItem()

    def visitArithValueExpression(self, ctx: SnowflakeSqlParser.ArithValueExpressionContext):
        left, right = [self.visit(e) for e in ctx.valueExpression()]
        op = no.BINARY_OP_MAP[ctx.op.getText().lower()]
        return no.BinaryExpr(left, op, right)

    def visitBinaryBooleanExpression(self, ctx: SnowflakeSqlParser.BinaryBooleanExpressionContext):
        left, right = [self.visit(e) for e in ctx.booleanExpression()]
        op = no.BINARY_OP_MAP[ctx.op.text.lower()]
        return no.BinaryExpr(left, op, right)

    def visitExpressionSelectItem(self, ctx: SnowflakeSqlParser.ExpressionSelectItemContext):
        expr = self.visit(ctx.expression())
        label = self.visit(ctx.identifier()) if ctx.identifier() is not None else None
        return no.ExprSelectItem(expr, label)

    def visitFunctionCallPrimaryExpression(self, ctx:SnowflakeSqlParser.FunctionCallPrimaryExpressionContext):
        name = self.visit(ctx.identifier())
        args = [self.visit(a) for a in ctx.expression()]
        return no.FunctionCall(name, args)

    def visitGroupBy(self, ctx: SnowflakeSqlParser.GroupByContext):
        exprs = [self.visit(e) for e in ctx.expression()]
        return no.GroupBy(exprs)

    def visitIntegerNumber(self, ctx: SnowflakeSqlParser.IntegerNumberContext):
        return no.Integer(int(ctx.INTEGER_VALUE().getText()))

    def visitJoinRelation(self, ctx: SnowflakeSqlParser.JoinRelationContext):
        left = self.visit(ctx.left)
        ty = no.JOIN_TYPE_MAP[' '.join(c.getText().lower() for c in ctx.joinType().children)] \
            if ctx.joinType() is not None else no.JoinType.DEFAULT
        right = self.visit(ctx.right)
        condition = self.visit(ctx.condition) if ctx.condition is not None else None
        return no.Join(left, ty, right, condition)

    def visitNull(self, ctx: SnowflakeSqlParser.NullContext):
        return no.Null()

    def visitParenRelation(self, ctx: SnowflakeSqlParser.ParenRelationContext):
        return self.visit(ctx.relation())

    def visitQuotedIdentifier(self, ctx: SnowflakeSqlParser.QuotedIdentifierContext):
        name = unquote(ctx.QUOTED_IDENTIFIER().getText(), '"')
        return no.Identifier(name)

    def visitSelectStatement(self, ctx: SnowflakeSqlParser.SelectStatementContext):
        items = [self.visit(i) for i in ctx.selectItem()]
        relations = [self.visit(r) for r in ctx.relation()]
        where = self.visit(ctx.where) if ctx.where is not None else None
        group_by = self.visit(ctx.groupBy()) if ctx.groupBy() else None
        return no.Select(items, relations, where, group_by)

    def visitString(self, ctx: SnowflakeSqlParser.StringContext):
        value = unquote(ctx.STRING().getText(), "'")
        return no.String(value)

    def visitTableRelation(self, ctx: SnowflakeSqlParser.TableRelationContext):
        return no.Table(self.visit(ctx.identifier()))

    def visitUnaryValueExpression(self, ctx: SnowflakeSqlParser.UnaryValueExpressionContext):
        op = no.UNARY_OP_MAP[ctx.op.getText().lower()]
        value = self.visit(ctx.valueExpression())
        return no.UnaryExpr(op, value)

    def visitUnaryBooleanExpression(self, ctx: SnowflakeSqlParser.UnaryBooleanExpressionContext):
        op = no.UNARY_OP_MAP[ctx.op.text.lower()]
        value = self.visit(ctx.booleanExpression())
        return no.UnaryExpr(op, value)

    def visitUnquotedIdentifier(self, ctx: SnowflakeSqlParser.UnquotedIdentifierContext):
        return no.Identifier(ctx.IDENTIFIER().getText())


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
