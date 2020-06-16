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


    # Visit a parse tree produced by SnowflakeSqlParser#statement.
    def visitStatement(self, ctx:SnowflakeSqlParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#selectItem.
    def visitSelectItem(self, ctx:SnowflakeSqlParser.SelectItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#tableClause.
    def visitTableClause(self, ctx:SnowflakeSqlParser.TableClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#identifier.
    def visitIdentifier(self, ctx:SnowflakeSqlParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SnowflakeSqlParser#integer.
    def visitInteger(self, ctx:SnowflakeSqlParser.IntegerContext):
        return self.visitChildren(ctx)



del SnowflakeSqlParser
