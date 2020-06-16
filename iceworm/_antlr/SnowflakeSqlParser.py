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
        buf.write("*\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2")
        buf.write("\3\2\3\2\3\2\3\3\3\3\3\3\3\3\7\3\27\n\3\f\3\16\3\32\13")
        buf.write("\3\3\3\3\3\5\3\36\n\3\3\4\3\4\5\4\"\n\4\3\5\3\5\3\6\3")
        buf.write("\6\3\7\3\7\3\7\2\2\b\2\4\6\b\n\f\2\2\2&\2\16\3\2\2\2\4")
        buf.write("\22\3\2\2\2\6!\3\2\2\2\b#\3\2\2\2\n%\3\2\2\2\f\'\3\2\2")
        buf.write("\2\16\17\5\4\3\2\17\20\7\3\2\2\20\21\7\2\2\3\21\3\3\2")
        buf.write("\2\2\22\23\7\5\2\2\23\30\5\6\4\2\24\25\7\4\2\2\25\27\5")
        buf.write("\6\4\2\26\24\3\2\2\2\27\32\3\2\2\2\30\26\3\2\2\2\30\31")
        buf.write("\3\2\2\2\31\35\3\2\2\2\32\30\3\2\2\2\33\34\7\6\2\2\34")
        buf.write("\36\5\b\5\2\35\33\3\2\2\2\35\36\3\2\2\2\36\5\3\2\2\2\37")
        buf.write("\"\5\n\6\2 \"\5\f\7\2!\37\3\2\2\2! \3\2\2\2\"\7\3\2\2")
        buf.write("\2#$\5\n\6\2$\t\3\2\2\2%&\7\7\2\2&\13\3\2\2\2\'(\7\b\2")
        buf.write("\2(\r\3\2\2\2\5\30\35!")
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
    RULE_statement = 1
    RULE_selectItem = 2
    RULE_tableClause = 3
    RULE_identifier = 4
    RULE_integer = 5

    ruleNames =  [ "singleStatement", "statement", "selectItem", "tableClause", 
                   "identifier", "integer" ]

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

        def statement(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.StatementContext,0)


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
            self.state = 12
            self.statement()
            self.state = 13
            self.match(SnowflakeSqlParser.T__0)
            self.state = 14
            self.match(SnowflakeSqlParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):

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
            return SnowflakeSqlParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = SnowflakeSqlParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 16
            self.match(SnowflakeSqlParser.SELECT)
            self.state = 17
            self.selectItem()
            self.state = 22
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SnowflakeSqlParser.T__1:
                self.state = 18
                self.match(SnowflakeSqlParser.T__1)
                self.state = 19
                self.selectItem()
                self.state = 24
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 27
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SnowflakeSqlParser.FROM:
                self.state = 25
                self.match(SnowflakeSqlParser.FROM)
                self.state = 26
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

        def identifier(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.IdentifierContext,0)


        def integer(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.IntegerContext,0)


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
            self.state = 31
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [SnowflakeSqlParser.IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 29
                self.identifier()
                pass
            elif token in [SnowflakeSqlParser.INTEGER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 30
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
        self.enterRule(localctx, 6, self.RULE_tableClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
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
        self.enterRule(localctx, 8, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
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
        self.enterRule(localctx, 10, self.RULE_integer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.match(SnowflakeSqlParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
