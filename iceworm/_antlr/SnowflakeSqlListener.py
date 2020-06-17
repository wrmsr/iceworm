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


    # Enter a parse tree produced by SnowflakeSqlParser#allSelectItem.
    def enterAllSelectItem(self, ctx:SnowflakeSqlParser.AllSelectItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#allSelectItem.
    def exitAllSelectItem(self, ctx:SnowflakeSqlParser.AllSelectItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#expressionSelectItem.
    def enterExpressionSelectItem(self, ctx:SnowflakeSqlParser.ExpressionSelectItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#expressionSelectItem.
    def exitExpressionSelectItem(self, ctx:SnowflakeSqlParser.ExpressionSelectItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#expression.
    def enterExpression(self, ctx:SnowflakeSqlParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#expression.
    def exitExpression(self, ctx:SnowflakeSqlParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#parenBooleanExpression.
    def enterParenBooleanExpression(self, ctx:SnowflakeSqlParser.ParenBooleanExpressionContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#parenBooleanExpression.
    def exitParenBooleanExpression(self, ctx:SnowflakeSqlParser.ParenBooleanExpressionContext):
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


    # Enter a parse tree produced by SnowflakeSqlParser#parenRelation.
    def enterParenRelation(self, ctx:SnowflakeSqlParser.ParenRelationContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#parenRelation.
    def exitParenRelation(self, ctx:SnowflakeSqlParser.ParenRelationContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#groupBy.
    def enterGroupBy(self, ctx:SnowflakeSqlParser.GroupByContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#groupBy.
    def exitGroupBy(self, ctx:SnowflakeSqlParser.GroupByContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#unquotedIdentifier.
    def enterUnquotedIdentifier(self, ctx:SnowflakeSqlParser.UnquotedIdentifierContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#unquotedIdentifier.
    def exitUnquotedIdentifier(self, ctx:SnowflakeSqlParser.UnquotedIdentifierContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#quotedIdentifier.
    def enterQuotedIdentifier(self, ctx:SnowflakeSqlParser.QuotedIdentifierContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#quotedIdentifier.
    def exitQuotedIdentifier(self, ctx:SnowflakeSqlParser.QuotedIdentifierContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#integerNumber.
    def enterIntegerNumber(self, ctx:SnowflakeSqlParser.IntegerNumberContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#integerNumber.
    def exitIntegerNumber(self, ctx:SnowflakeSqlParser.IntegerNumberContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#string.
    def enterString(self, ctx:SnowflakeSqlParser.StringContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#string.
    def exitString(self, ctx:SnowflakeSqlParser.StringContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#null.
    def enterNull(self, ctx:SnowflakeSqlParser.NullContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#null.
    def exitNull(self, ctx:SnowflakeSqlParser.NullContext):
        pass



del SnowflakeSqlParser
