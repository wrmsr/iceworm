# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
# encoding: utf-8
from omnibus._vendor.antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\t")
        buf.write(".\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\7\3\31\n\3\f\3\16")
        buf.write("\3\34\13\3\3\3\3\3\5\3 \n\3\3\4\3\4\3\5\3\5\5\5&\n\5\3")
        buf.write("\6\3\6\3\7\3\7\3\b\3\b\3\b\2\2\t\2\4\6\b\n\f\16\2\2\2")
        buf.write(")\2\20\3\2\2\2\4\24\3\2\2\2\6!\3\2\2\2\b%\3\2\2\2\n\'")
        buf.write("\3\2\2\2\f)\3\2\2\2\16+\3\2\2\2\20\21\5\4\3\2\21\22\7")
        buf.write("\3\2\2\22\23\7\2\2\3\23\3\3\2\2\2\24\25\7\5\2\2\25\32")
        buf.write("\5\6\4\2\26\27\7\4\2\2\27\31\5\6\4\2\30\26\3\2\2\2\31")
        buf.write("\34\3\2\2\2\32\30\3\2\2\2\32\33\3\2\2\2\33\37\3\2\2\2")
        buf.write("\34\32\3\2\2\2\35\36\7\6\2\2\36 \5\n\6\2\37\35\3\2\2\2")
        buf.write("\37 \3\2\2\2 \5\3\2\2\2!\"\5\b\5\2\"\7\3\2\2\2#&\5\f\7")
        buf.write("\2$&\5\16\b\2%#\3\2\2\2%$\3\2\2\2&\t\3\2\2\2\'(\5\f\7")
        buf.write("\2(\13\3\2\2\2)*\7\7\2\2*\r\3\2\2\2+,\7\b\2\2,\17\3\2")
        buf.write("\2\2\5\32\37%")
        return buf.getvalue()


class SnowflakeSqlParser ( Parser ):

    grammarFileName = "SnowflakeSql.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "','", "'select'", "'from'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "SELECT", "FROM", 
                      "IDENTIFIER", "INTEGER", "WS" ]

    RULE_singleStatement = 0
    RULE_selectStatement = 1
    RULE_selectItem = 2
    RULE_expression = 3
    RULE_tableClause = 4
    RULE_identifier = 5
    RULE_integer = 6

    ruleNames =  [ "singleStatement", "selectStatement", "selectItem", "expression", 
                   "tableClause", "identifier", "integer" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    SELECT=3
    FROM=4
    IDENTIFIER=5
    INTEGER=6
    WS=7

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class SingleStatementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def selectStatement(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.SelectStatementContext,0)


        def EOF(self):
            return self.getToken(SnowflakeSqlParser.EOF, 0)

        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_singleStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleStatement" ):
                listener.enterSingleStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleStatement" ):
                listener.exitSingleStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingleStatement" ):
                return visitor.visitSingleStatement(self)
            else:
                return visitor.visitChildren(self)




    def singleStatement(self):

        localctx = SnowflakeSqlParser.SingleStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_singleStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.selectStatement()
            self.state = 15
            self.match(SnowflakeSqlParser.T__0)
            self.state = 16
            self.match(SnowflakeSqlParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectStatementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SELECT(self):
            return self.getToken(SnowflakeSqlParser.SELECT, 0)

        def selectItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SnowflakeSqlParser.SelectItemContext)
            else:
                return self.getTypedRuleContext(SnowflakeSqlParser.SelectItemContext,i)


        def FROM(self):
            return self.getToken(SnowflakeSqlParser.FROM, 0)

        def tableClause(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.TableClauseContext,0)


        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_selectStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectStatement" ):
                listener.enterSelectStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectStatement" ):
                listener.exitSelectStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectStatement" ):
                return visitor.visitSelectStatement(self)
            else:
                return visitor.visitChildren(self)




    def selectStatement(self):

        localctx = SnowflakeSqlParser.SelectStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_selectStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 18
            self.match(SnowflakeSqlParser.SELECT)
            self.state = 19
            self.selectItem()
            self.state = 24
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SnowflakeSqlParser.T__1:
                self.state = 20
                self.match(SnowflakeSqlParser.T__1)
                self.state = 21
                self.selectItem()
                self.state = 26
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SnowflakeSqlParser.FROM:
                self.state = 27
                self.match(SnowflakeSqlParser.FROM)
                self.state = 28
                self.tableClause()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectItemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.ExpressionContext,0)


        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_selectItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectItem" ):
                listener.enterSelectItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectItem" ):
                listener.exitSelectItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectItem" ):
                return visitor.visitSelectItem(self)
            else:
                return visitor.visitChildren(self)




    def selectItem(self):

        localctx = SnowflakeSqlParser.SelectItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_selectItem)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.IdentifierContext,0)


        def integer(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.IntegerContext,0)


        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = SnowflakeSqlParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_expression)
        try:
            self.state = 35
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [SnowflakeSqlParser.IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 33
                self.identifier()
                pass
            elif token in [SnowflakeSqlParser.INTEGER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 34
                self.integer()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TableClauseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.IdentifierContext,0)


        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_tableClause

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTableClause" ):
                listener.enterTableClause(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTableClause" ):
                listener.exitTableClause(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTableClause" ):
                return visitor.visitTableClause(self)
            else:
                return visitor.visitChildren(self)




    def tableClause(self):

        localctx = SnowflakeSqlParser.TableClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_tableClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.identifier()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifierContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(SnowflakeSqlParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_identifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier" ):
                listener.enterIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier" ):
                listener.exitIdentifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifier" ):
                return visitor.visitIdentifier(self)
            else:
                return visitor.visitChildren(self)




    def identifier(self):

        localctx = SnowflakeSqlParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.match(SnowflakeSqlParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntegerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(SnowflakeSqlParser.INTEGER, 0)

        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_integer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInteger" ):
                listener.enterInteger(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInteger" ):
                listener.exitInteger(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInteger" ):
                return visitor.visitInteger(self)
            else:
                return visitor.visitChildren(self)




    def integer(self):

        localctx = SnowflakeSqlParser.IntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_integer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(SnowflakeSqlParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
