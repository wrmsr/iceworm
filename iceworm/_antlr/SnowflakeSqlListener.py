# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from .._vendor.antlr4 import *
if __name__ is not None and "." in __name__:
    from .SnowflakeSqlParser import SnowflakeSqlParser
else:
    from SnowflakeSqlParser import SnowflakeSqlParser

# This class defines a complete listener for a parse tree produced by SnowflakeSqlParser.
class SnowflakeSqlListener(ParseTreeListener):

    # Enter a parse tree produced by SnowflakeSqlParser#parse.
    def enterParse(self, ctx:SnowflakeSqlParser.ParseContext):
        pass

    # Exit a parse tree produced by SnowflakeSqlParser#parse.
    def exitParse(self, ctx:SnowflakeSqlParser.ParseContext):
        pass



del SnowflakeSqlParser
