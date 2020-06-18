# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .SnowflakeSqlParser import SnowflakeSqlParser
else:
    from SnowflakeSqlParser import SnowflakeSqlParser

# This class defines a complete generic visitor for a parse tree produced by SnowflakeSqlParser.

class SnowflakeSqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SnowflakeSqlParser#singleStatement.
    def visitSingleStatement(self, ctx:SnowflakeSqlParser.SingleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#selectStatement.
    def visitSelectStatement(self, ctx:SnowflakeSqlParser.SelectStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#allSelectItem.
    def visitAllSelectItem(self, ctx:SnowflakeSqlParser.AllSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#expressionSelectItem.
    def visitExpressionSelectItem(self, ctx:SnowflakeSqlParser.ExpressionSelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#expression.
    def visitExpression(self, ctx:SnowflakeSqlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#binaryBooleanExpression.
    def visitBinaryBooleanExpression(self, ctx:SnowflakeSqlParser.BinaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#predicatedBooleanExpression.
    def visitPredicatedBooleanExpression(self, ctx:SnowflakeSqlParser.PredicatedBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unaryBooleanExpression.
    def visitUnaryBooleanExpression(self, ctx:SnowflakeSqlParser.UnaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#cmpPredicate.
    def visitCmpPredicate(self, ctx:SnowflakeSqlParser.CmpPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#inListPredicate.
    def visitInListPredicate(self, ctx:SnowflakeSqlParser.InListPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#isNullPredicate.
    def visitIsNullPredicate(self, ctx:SnowflakeSqlParser.IsNullPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#primaryValueExpression.
    def visitPrimaryValueExpression(self, ctx:SnowflakeSqlParser.PrimaryValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unaryValueExpression.
    def visitUnaryValueExpression(self, ctx:SnowflakeSqlParser.UnaryValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#arithValueExpression.
    def visitArithValueExpression(self, ctx:SnowflakeSqlParser.ArithValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#functionCallPrimaryExpression.
    def visitFunctionCallPrimaryExpression(self, ctx:SnowflakeSqlParser.FunctionCallPrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#simplePrimaryExpression.
    def visitSimplePrimaryExpression(self, ctx:SnowflakeSqlParser.SimplePrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#simpleExpression.
    def visitSimpleExpression(self, ctx:SnowflakeSqlParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#joinRelation.
    def visitJoinRelation(self, ctx:SnowflakeSqlParser.JoinRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#tableRelation.
    def visitTableRelation(self, ctx:SnowflakeSqlParser.TableRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#parenRelation.
    def visitParenRelation(self, ctx:SnowflakeSqlParser.ParenRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#groupBy.
    def visitGroupBy(self, ctx:SnowflakeSqlParser.GroupByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unquotedIdentifier.
    def visitUnquotedIdentifier(self, ctx:SnowflakeSqlParser.UnquotedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#quotedIdentifier.
    def visitQuotedIdentifier(self, ctx:SnowflakeSqlParser.QuotedIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#integerNumber.
    def visitIntegerNumber(self, ctx:SnowflakeSqlParser.IntegerNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#string.
    def visitString(self, ctx:SnowflakeSqlParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#null.
    def visitNull(self, ctx:SnowflakeSqlParser.NullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#joinType.
    def visitJoinType(self, ctx:SnowflakeSqlParser.JoinTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#cmpOp.
    def visitCmpOp(self, ctx:SnowflakeSqlParser.CmpOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#arithOp.
    def visitArithOp(self, ctx:SnowflakeSqlParser.ArithOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unaryOp.
    def visitUnaryOp(self, ctx:SnowflakeSqlParser.UnaryOpContext):
        return self.visitChildren(ctx)



del SnowflakeSqlParser
