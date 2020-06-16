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


    # Enter a parse tree produced by SnowflakeSqlParser#statement.
    def enterStatement(self, ctx:SnowflakeSqlParser.StatementContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#statement.
    def exitStatement(self, ctx:SnowflakeSqlParser.StatementContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#selectItem.
    def enterSelectItem(self, ctx:SnowflakeSqlParser.SelectItemContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#selectItem.
    def exitSelectItem(self, ctx:SnowflakeSqlParser.SelectItemContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#tableClause.
    def enterTableClause(self, ctx:SnowflakeSqlParser.TableClauseContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#tableClause.
    def exitTableClause(self, ctx:SnowflakeSqlParser.TableClauseContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#identifier.
    def enterIdentifier(self, ctx:SnowflakeSqlParser.IdentifierContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#identifier.
    def exitIdentifier(self, ctx:SnowflakeSqlParser.IdentifierContext):
        pass


    # Enter a parse tree produced by SnowflakeSqlParser#integer.
    def enterInteger(self, ctx:SnowflakeSqlParser.IntegerContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#integer.
    def exitInteger(self, ctx:SnowflakeSqlParser.IntegerContext):
        pass



del SnowflakeSqlParser
