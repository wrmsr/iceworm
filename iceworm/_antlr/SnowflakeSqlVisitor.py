# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from .._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .SnowflakeSqlParser import SnowflakeSqlParser
else:
    from SnowflakeSqlParser import SnowflakeSqlParser

# This class defines a complete generic visitor for a parse tree produced by SnowflakeSqlParser.

class SnowflakeSqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SnowflakeSqlParser#parse.
    def visitParse(self, ctx:SnowflakeSqlParser.ParseContext):
        return self.visitChildren(ctx)



del SnowflakeSqlParser
