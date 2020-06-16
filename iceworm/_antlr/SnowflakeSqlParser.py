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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\20")
        buf.write("h\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\2\3\2\3\3\3\3")
        buf.write("\3\3\3\3\7\3\37\n\3\f\3\16\3\"\13\3\3\3\3\3\3\3\3\3\7")
        buf.write("\3(\n\3\f\3\16\3+\13\3\5\3-\n\3\3\4\3\4\5\4\61\n\4\3\4")
        buf.write("\5\4\64\n\4\3\5\3\5\3\6\3\6\3\6\3\6\5\6<\n\6\3\6\3\6\3")
        buf.write("\6\7\6A\n\6\f\6\16\6D\13\6\3\7\3\7\3\7\5\7I\n\7\3\b\3")
        buf.write("\b\3\b\3\b\3\b\7\bP\n\b\f\b\16\bS\13\b\5\bU\n\b\3\b\3")
        buf.write("\b\3\t\3\t\3\t\3\t\3\t\3\t\7\t_\n\t\f\t\16\tb\13\t\3\n")
        buf.write("\3\n\3\13\3\13\3\13\2\4\n\20\f\2\4\6\b\n\f\16\20\22\24")
        buf.write("\2\3\4\2\7\7\f\f\2i\2\26\3\2\2\2\4\32\3\2\2\2\6.\3\2\2")
        buf.write("\2\b\65\3\2\2\2\n;\3\2\2\2\fH\3\2\2\2\16J\3\2\2\2\20X")
        buf.write("\3\2\2\2\22c\3\2\2\2\24e\3\2\2\2\26\27\5\4\3\2\27\30\7")
        buf.write("\3\2\2\30\31\7\2\2\3\31\3\3\2\2\2\32\33\7\r\2\2\33 \5")
        buf.write("\6\4\2\34\35\7\4\2\2\35\37\5\6\4\2\36\34\3\2\2\2\37\"")
        buf.write("\3\2\2\2 \36\3\2\2\2 !\3\2\2\2!,\3\2\2\2\" \3\2\2\2#$")
        buf.write("\7\t\2\2$)\5\20\t\2%&\7\4\2\2&(\5\20\t\2\'%\3\2\2\2(+")
        buf.write("\3\2\2\2)\'\3\2\2\2)*\3\2\2\2*-\3\2\2\2+)\3\2\2\2,#\3")
        buf.write("\2\2\2,-\3\2\2\2-\5\3\2\2\2.\63\5\b\5\2/\61\7\b\2\2\60")
        buf.write("/\3\2\2\2\60\61\3\2\2\2\61\62\3\2\2\2\62\64\5\22\n\2\63")
        buf.write("\60\3\2\2\2\63\64\3\2\2\2\64\7\3\2\2\2\65\66\5\n\6\2\66")
        buf.write("\t\3\2\2\2\678\b\6\1\28<\5\f\7\29:\7\13\2\2:<\5\n\6\4")
        buf.write(";\67\3\2\2\2;9\3\2\2\2<B\3\2\2\2=>\f\3\2\2>?\t\2\2\2?")
        buf.write("A\5\n\6\4@=\3\2\2\2AD\3\2\2\2B@\3\2\2\2BC\3\2\2\2C\13")
        buf.write("\3\2\2\2DB\3\2\2\2EI\5\22\n\2FI\5\24\13\2GI\5\16\b\2H")
        buf.write("E\3\2\2\2HF\3\2\2\2HG\3\2\2\2I\r\3\2\2\2JK\5\22\n\2KT")
        buf.write("\7\5\2\2LM\5\b\5\2MQ\7\4\2\2NP\5\b\5\2ON\3\2\2\2PS\3\2")
        buf.write("\2\2QO\3\2\2\2QR\3\2\2\2RU\3\2\2\2SQ\3\2\2\2TL\3\2\2\2")
        buf.write("TU\3\2\2\2UV\3\2\2\2VW\7\6\2\2W\17\3\2\2\2XY\b\t\1\2Y")
        buf.write("Z\5\22\n\2Z`\3\2\2\2[\\\f\4\2\2\\]\7\n\2\2]_\5\20\t\5")
        buf.write("^[\3\2\2\2_b\3\2\2\2`^\3\2\2\2`a\3\2\2\2a\21\3\2\2\2b")
        buf.write("`\3\2\2\2cd\7\17\2\2d\23\3\2\2\2ef\7\16\2\2f\25\3\2\2")
        buf.write("\2\r ),\60\63;BHQT`")
        return buf.getvalue()


class SnowflakeSqlParser ( Parser ):

    grammarFileName = "SnowflakeSql.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "','", "'('", "')'", "'and'", "'as'", 
                     "'from'", "'join'", "'not'", "'or'", "'select'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "AND", "AS", "FROM", "JOIN", "NOT", "OR", 
                      "SELECT", "INTEGER_VALUE", "IDENTIFIER", "WS" ]

    RULE_singleStatement = 0
    RULE_selectStatement = 1
    RULE_selectItem = 2
    RULE_expression = 3
    RULE_booleanExpression = 4
    RULE_primaryExpression = 5
    RULE_functionCall = 6
    RULE_relation = 7
    RULE_identifier = 8
    RULE_number = 9

    ruleNames =  [ "singleStatement", "selectStatement", "selectItem", "expression", 
                   "booleanExpression", "primaryExpression", "functionCall", 
                   "relation", "identifier", "number" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    AND=5
    AS=6
    FROM=7
    JOIN=8
    NOT=9
    OR=10
    SELECT=11
    INTEGER_VALUE=12
    IDENTIFIER=13
    WS=14

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
            self.state = 20
            self.selectStatement()
            self.state = 21
            self.match(SnowflakeSqlParser.T__0)
            self.state = 22
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
            self.state = 24
            self.match(SnowflakeSqlParser.SELECT)
            self.state = 25
            self.selectItem()
            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SnowflakeSqlParser.T__1:
                self.state = 26
                self.match(SnowflakeSqlParser.T__1)
                self.state = 27
                self.selectItem()
                self.state = 32
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SnowflakeSqlParser.FROM:
                self.state = 33
                self.match(SnowflakeSqlParser.FROM)
                self.state = 34
                self.relation(0)
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==SnowflakeSqlParser.T__1:
                    self.state = 35
                    self.match(SnowflakeSqlParser.T__1)
                    self.state = 36
                    self.relation(0)
                    self.state = 41
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


        def identifier(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.IdentifierContext,0)


        def AS(self):
            return self.getToken(SnowflakeSqlParser.AS, 0)

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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.expression()
            self.state = 49
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SnowflakeSqlParser.AS or _la==SnowflakeSqlParser.IDENTIFIER:
                self.state = 46
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==SnowflakeSqlParser.AS:
                    self.state = 45
                    self.match(SnowflakeSqlParser.AS)


                self.state = 48
                self.identifier()


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

        def booleanExpression(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.BooleanExpressionContext,0)


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
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.booleanExpression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_booleanExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class PrimaryBooleanExpressionContext(BooleanExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SnowflakeSqlParser.BooleanExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def primaryExpression(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.PrimaryExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimaryBooleanExpression" ):
                listener.enterPrimaryBooleanExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimaryBooleanExpression" ):
                listener.exitPrimaryBooleanExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryBooleanExpression" ):
                return visitor.visitPrimaryBooleanExpression(self)
            else:
                return visitor.visitChildren(self)


    class BinaryBooleanExpressionContext(BooleanExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SnowflakeSqlParser.BooleanExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def booleanExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SnowflakeSqlParser.BooleanExpressionContext)
            else:
                return self.getTypedRuleContext(SnowflakeSqlParser.BooleanExpressionContext,i)

        def AND(self):
            return self.getToken(SnowflakeSqlParser.AND, 0)
        def OR(self):
            return self.getToken(SnowflakeSqlParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinaryBooleanExpression" ):
                listener.enterBinaryBooleanExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinaryBooleanExpression" ):
                listener.exitBinaryBooleanExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinaryBooleanExpression" ):
                return visitor.visitBinaryBooleanExpression(self)
            else:
                return visitor.visitChildren(self)


    class UnaryBooleanExpressionContext(BooleanExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SnowflakeSqlParser.BooleanExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def booleanExpression(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.BooleanExpressionContext,0)

        def NOT(self):
            return self.getToken(SnowflakeSqlParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryBooleanExpression" ):
                listener.enterUnaryBooleanExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryBooleanExpression" ):
                listener.exitUnaryBooleanExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryBooleanExpression" ):
                return visitor.visitUnaryBooleanExpression(self)
            else:
                return visitor.visitChildren(self)



    def booleanExpression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = SnowflakeSqlParser.BooleanExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_booleanExpression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [SnowflakeSqlParser.INTEGER_VALUE, SnowflakeSqlParser.IDENTIFIER]:
                localctx = SnowflakeSqlParser.PrimaryBooleanExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 54
                self.primaryExpression()
                pass
            elif token in [SnowflakeSqlParser.NOT]:
                localctx = SnowflakeSqlParser.UnaryBooleanExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 55
                localctx.op = self.match(SnowflakeSqlParser.NOT)
                self.state = 56
                self.booleanExpression(2)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 64
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = SnowflakeSqlParser.BinaryBooleanExpressionContext(self, SnowflakeSqlParser.BooleanExpressionContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_booleanExpression)
                    self.state = 59
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 60
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==SnowflakeSqlParser.AND or _la==SnowflakeSqlParser.OR):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 61
                    self.booleanExpression(2) 
                self.state = 66
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PrimaryExpressionContext(ParserRuleContext):

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
            return SnowflakeSqlParser.RULE_primaryExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimaryExpression" ):
                listener.enterPrimaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimaryExpression" ):
                listener.exitPrimaryExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryExpression" ):
                return visitor.visitPrimaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def primaryExpression(self):

        localctx = SnowflakeSqlParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_primaryExpression)
        try:
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 67
                self.identifier()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 68
                self.number()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 69
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
        self.enterRule(localctx, 12, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.identifier()
            self.state = 73
            self.match(SnowflakeSqlParser.T__2)
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SnowflakeSqlParser.NOT) | (1 << SnowflakeSqlParser.INTEGER_VALUE) | (1 << SnowflakeSqlParser.IDENTIFIER))) != 0):
                self.state = 74
                self.expression()

                self.state = 75
                self.match(SnowflakeSqlParser.T__1)
                self.state = 79
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SnowflakeSqlParser.NOT) | (1 << SnowflakeSqlParser.INTEGER_VALUE) | (1 << SnowflakeSqlParser.IDENTIFIER))) != 0):
                    self.state = 76
                    self.expression()
                    self.state = 81
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 84
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


        def getRuleIndex(self):
            return SnowflakeSqlParser.RULE_relation

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class JoinRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SnowflakeSqlParser.RelationContext
            super().__init__(parser)
            self.left = None # RelationContext
            self.right = None # RelationContext
            self.copyFrom(ctx)

        def JOIN(self):
            return self.getToken(SnowflakeSqlParser.JOIN, 0)
        def relation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SnowflakeSqlParser.RelationContext)
            else:
                return self.getTypedRuleContext(SnowflakeSqlParser.RelationContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJoinRelation" ):
                listener.enterJoinRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJoinRelation" ):
                listener.exitJoinRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJoinRelation" ):
                return visitor.visitJoinRelation(self)
            else:
                return visitor.visitChildren(self)


    class TableRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SnowflakeSqlParser.RelationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def identifier(self):
            return self.getTypedRuleContext(SnowflakeSqlParser.IdentifierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTableRelation" ):
                listener.enterTableRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTableRelation" ):
                listener.exitTableRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTableRelation" ):
                return visitor.visitTableRelation(self)
            else:
                return visitor.visitChildren(self)



    def relation(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = SnowflakeSqlParser.RelationContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 14
        self.enterRecursionRule(localctx, 14, self.RULE_relation, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = SnowflakeSqlParser.TableRelationContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 87
            self.identifier()
            self._ctx.stop = self._input.LT(-1)
            self.state = 94
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = SnowflakeSqlParser.JoinRelationContext(self, SnowflakeSqlParser.RelationContext(self, _parentctx, _parentState))
                    localctx.left = _prevctx
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_relation)
                    self.state = 89
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 90
                    self.match(SnowflakeSqlParser.JOIN)
                    self.state = 91
                    localctx.right = self.relation(3) 
                self.state = 96
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
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
        self.enterRule(localctx, 16, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
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
        self.enterRule(localctx, 18, self.RULE_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.match(SnowflakeSqlParser.INTEGER_VALUE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[4] = self.booleanExpression_sempred
        self._predicates[7] = self.relation_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def booleanExpression_sempred(self, localctx:BooleanExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def relation_sempred(self, localctx:RelationContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         
