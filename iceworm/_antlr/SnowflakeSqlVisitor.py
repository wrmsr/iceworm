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


    # Visit a parse tree produced by SnowflakeSqlParser#selectItem.
    def visitSelectItem(self, ctx:SnowflakeSqlParser.SelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#expression.
    def visitExpression(self, ctx:SnowflakeSqlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#primaryBooleanExpression.
    def visitPrimaryBooleanExpression(self, ctx:SnowflakeSqlParser.PrimaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#binaryBooleanExpression.
    def visitBinaryBooleanExpression(self, ctx:SnowflakeSqlParser.BinaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#unaryBooleanExpression.
    def visitUnaryBooleanExpression(self, ctx:SnowflakeSqlParser.UnaryBooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:SnowflakeSqlParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#functionCall.
    def visitFunctionCall(self, ctx:SnowflakeSqlParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#joinRelation.
    def visitJoinRelation(self, ctx:SnowflakeSqlParser.JoinRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#tableRelation.
    def visitTableRelation(self, ctx:SnowflakeSqlParser.TableRelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#groupBy.
    def visitGroupBy(self, ctx:SnowflakeSqlParser.GroupByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#identifier.
    def visitIdentifier(self, ctx:SnowflakeSqlParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#integerNumber.
    def visitIntegerNumber(self, ctx:SnowflakeSqlParser.IntegerNumberContext):
        return self.visitChildren(ctx)



del SnowflakeSqlParser
