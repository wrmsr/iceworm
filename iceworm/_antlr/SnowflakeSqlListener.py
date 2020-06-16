# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .SnowflakeSqlParser import SnowflakeSqlParser
else:
    from SnowflakeSqlParser import SnowflakeSqlParser

# This class defines a complete listener for a parse tree produced by SnowflakeSqlParser.
class SnowflakeSqlListener(ParseTreeListener):

    # Enter a parse tree produced by SnowflakeSqlParser#singleStatement.
    def enterSingleStatement(self, ctx:SnowflakeSqlParser.SingleStatementContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#singleStatement.
    def exitSingleStatement(self, ctx:SnowflakeSqlParser.SingleStatementContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#selectStatement.
    def enterSelectStatement(self, ctx:SnowflakeSqlParser.SelectStatementContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#selectStatement.
    def exitSelectStatement(self, ctx:SnowflakeSqlParser.SelectStatementContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#selectItem.
    def enterSelectItem(self, ctx:SnowflakeSqlParser.SelectItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#selectItem.
    def exitSelectItem(self, ctx:SnowflakeSqlParser.SelectItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#expression.
    def enterExpression(self, ctx:SnowflakeSqlParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#expression.
    def exitExpression(self, ctx:SnowflakeSqlParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#primaryBooleanExpression.
    def enterPrimaryBooleanExpression(self, ctx:SnowflakeSqlParser.PrimaryBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#primaryBooleanExpression.
    def exitPrimaryBooleanExpression(self, ctx:SnowflakeSqlParser.PrimaryBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#binaryBooleanExpression.
    def enterBinaryBooleanExpression(self, ctx:SnowflakeSqlParser.BinaryBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#binaryBooleanExpression.
    def exitBinaryBooleanExpression(self, ctx:SnowflakeSqlParser.BinaryBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unaryBooleanExpression.
    def enterUnaryBooleanExpression(self, ctx:SnowflakeSqlParser.UnaryBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unaryBooleanExpression.
    def exitUnaryBooleanExpression(self, ctx:SnowflakeSqlParser.UnaryBooleanExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:SnowflakeSqlParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:SnowflakeSqlParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#functionCall.
    def enterFunctionCall(self, ctx:SnowflakeSqlParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#functionCall.
    def exitFunctionCall(self, ctx:SnowflakeSqlParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#joinRelation.
    def enterJoinRelation(self, ctx:SnowflakeSqlParser.JoinRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#joinRelation.
    def exitJoinRelation(self, ctx:SnowflakeSqlParser.JoinRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#tableRelation.
    def enterTableRelation(self, ctx:SnowflakeSqlParser.TableRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#tableRelation.
    def exitTableRelation(self, ctx:SnowflakeSqlParser.TableRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#identifier.
    def enterIdentifier(self, ctx:SnowflakeSqlParser.IdentifierContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#identifier.
    def exitIdentifier(self, ctx:SnowflakeSqlParser.IdentifierContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#integerNumber.
    def enterIntegerNumber(self, ctx:SnowflakeSqlParser.IntegerNumberContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#integerNumber.
    def exitIntegerNumber(self, ctx:SnowflakeSqlParser.IntegerNumberContext):
        pass



del SnowflakeSqlParser
