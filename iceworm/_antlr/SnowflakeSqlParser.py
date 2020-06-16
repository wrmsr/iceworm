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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\13")
        buf.write("F\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\7\3\33\n")
        buf.write("\3\f\3\16\3\36\13\3\3\3\3\3\3\3\3\3\7\3$\n\3\f\3\16\3")
        buf.write("\'\13\3\5\3)\n\3\3\4\3\4\3\5\3\5\3\5\5\5\60\n\5\3\6\3")
        buf.write("\6\3\6\3\6\3\6\7\6\67\n\6\f\6\16\6:\13\6\5\6<\n\6\3\6")
        buf.write("\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\2\2\n\2\4\6\b\n\f\16")
        buf.write("\20\2\2\2D\2\22\3\2\2\2\4\26\3\2\2\2\6*\3\2\2\2\b/\3\2")
        buf.write("\2\2\n\61\3\2\2\2\f?\3\2\2\2\16A\3\2\2\2\20C\3\2\2\2\22")
        buf.write("\23\5\4\3\2\23\24\7\3\2\2\24\25\7\2\2\3\25\3\3\2\2\2\26")
        buf.write("\27\7\7\2\2\27\34\5\6\4\2\30\31\7\4\2\2\31\33\5\6\4\2")
        buf.write("\32\30\3\2\2\2\33\36\3\2\2\2\34\32\3\2\2\2\34\35\3\2\2")
        buf.write("\2\35(\3\2\2\2\36\34\3\2\2\2\37 \7\b\2\2 %\5\f\7\2!\"")
        buf.write("\7\4\2\2\"$\5\f\7\2#!\3\2\2\2$\'\3\2\2\2%#\3\2\2\2%&\3")
        buf.write("\2\2\2&)\3\2\2\2\'%\3\2\2\2(\37\3\2\2\2()\3\2\2\2)\5\3")
        buf.write("\2\2\2*+\5\b\5\2+\7\3\2\2\2,\60\5\16\b\2-\60\5\20\t\2")
        buf.write(".\60\5\n\6\2/,\3\2\2\2/-\3\2\2\2/.\3\2\2\2\60\t\3\2\2")
        buf.write("\2\61\62\5\16\b\2\62;\7\5\2\2\63\64\5\b\5\2\648\7\4\2")
        buf.write("\2\65\67\5\b\5\2\66\65\3\2\2\2\67:\3\2\2\28\66\3\2\2\2")
        buf.write("89\3\2\2\29<\3\2\2\2:8\3\2\2\2;\63\3\2\2\2;<\3\2\2\2<")
        buf.write("=\3\2\2\2=>\7\6\2\2>\13\3\2\2\2?@\5\16\b\2@\r\3\2\2\2")
        buf.write("AB\7\n\2\2B\17\3\2\2\2CD\7\t\2\2D\21\3\2\2\2\b\34%(/8")
        buf.write(";")
        return buf.getvalue()


class SnowflakeSqlParser ( Parser ):

    grammarFileName = "SnowflakeSql.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "','", "'('", "')'", "'select'", 
                     "'from'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "SELECT", "FROM", "INTEGER_VALUE", "IDENTIFIER", 
                      "WS" ]

    RULE_singleStatement = 0
    RULE_selectStatement = 1
    RULE_selectItem = 2
    RULE_expression = 3
    RULE_functionCall = 4
    RULE_relation = 5
    RULE_identifier = 6
    RULE_number = 7

    ruleNames =  [ "singleStatement", "selectStatement", "selectItem", "expression", 
                   "functionCall", "relation", "identifier", "number" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    SELECT=5
    FROM=6
    INTEGER_VALUE=7
    IDENTIFIER=8
    WS=9

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
            self.state = 16
            self.selectStatement()
            self.state = 17
            self.match(SnowflakeSqlParser.T__0)
            self.state = 18
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

        def relation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SnowflakeSqlParser.RelationContext)
            else:
                return self.getTypedRuleContext(SnowflakeSqlParser.RelationContext,i)


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
            self.state = 20
            self.match(SnowflakeSqlParser.SELECT)
            self.state = 21
            self.selectItem()
            self.state = 26
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SnowflakeSqlParser.T__1:
                self.state = 22
                self.match(SnowflakeSqlParser.T__1)
                self.state = 23
                self.selectItem()
                self.state = 28
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 38
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SnowflakeSqlParser.FROM:
                self.state = 29
                self.match(SnowflakeSqlParser.FROM)
                self.state = 30
                self.relation()
                self.state = 35
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==SnowflakeSqlParser.T__1:
                    self.state = 31
                    self.match(SnowflakeSqlParser.T__1)
                    self.state = 32
                    self.relation()
                    self.state = 37
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



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
            self.state = 40
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


        def number(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.NumberContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.FunctionCallContext,0)


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
            self.state = 45
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 42
                self.identifier()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 43
                self.number()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 44
                self.functionCall()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.IdentifierContext,0)


        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SnowflakeSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(SnowflakeSqlParser.ExpressionContext,i)


        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_functionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def functionCall(self):

        localctx = SnowflakeSqlParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.identifier()
            self.state = 48
            self.match(SnowflakeSqlParser.T__2)
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SnowflakeSqlParser.INTEGER_VALUE or _la==SnowflakeSqlParser.IDENTIFIER:
                self.state = 49
                self.expression()

                self.state = 50
                self.match(SnowflakeSqlParser.T__1)
                self.state = 54
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==SnowflakeSqlParser.INTEGER_VALUE or _la==SnowflakeSqlParser.IDENTIFIER:
                    self.state = 51
                    self.expression()
                    self.state = 56
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 59
            self.match(SnowflakeSqlParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.IdentifierContext,0)


        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_relation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelation" ):
                listener.enterRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelation" ):
                listener.exitRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelation" ):
                return visitor.visitRelation(self)
            else:
                return visitor.visitChildren(self)




    def relation(self):

        localctx = SnowflakeSqlParser.RelationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_relation)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
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
        self.enterRule(localctx, 12, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(SnowflakeSqlParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER_VALUE(self):
            return self.getToken(SnowflakeSqlParser.INTEGER_VALUE, 0)

        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)




    def number(self):

        localctx = SnowflakeSqlParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self.match(SnowflakeSqlParser.INTEGER_VALUE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
