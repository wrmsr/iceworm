# flake8: noqa
# Generated from Minml.g4 by ANTLR 4.8
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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\16")
        buf.write("N\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\3\3\3\3\3\3\3")
        buf.write("\7\3\35\n\3\f\3\16\3 \13\3\3\3\3\3\3\3\3\3\5\3&\n\3\3")
        buf.write("\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\7\5\60\n\5\f\5\16\5\63")
        buf.write("\13\5\3\5\3\5\3\5\3\5\5\59\n\5\3\6\3\6\3\6\3\6\3\6\3\6")
        buf.write("\3\6\5\6B\n\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13")
        buf.write("\3\13\2\2\f\2\4\6\b\n\f\16\20\22\24\2\2\2M\2\26\3\2\2")
        buf.write("\2\4%\3\2\2\2\6\'\3\2\2\2\b8\3\2\2\2\nA\3\2\2\2\fC\3\2")
        buf.write("\2\2\16E\3\2\2\2\20G\3\2\2\2\22I\3\2\2\2\24K\3\2\2\2\26")
        buf.write("\27\5\n\6\2\27\3\3\2\2\2\30\31\7\3\2\2\31\36\5\6\4\2\32")
        buf.write("\33\7\4\2\2\33\35\5\6\4\2\34\32\3\2\2\2\35 \3\2\2\2\36")
        buf.write("\34\3\2\2\2\36\37\3\2\2\2\37!\3\2\2\2 \36\3\2\2\2!\"\7")
        buf.write("\5\2\2\"&\3\2\2\2#$\7\3\2\2$&\7\5\2\2%\30\3\2\2\2%#\3")
        buf.write("\2\2\2&\5\3\2\2\2\'(\5\f\7\2()\7\6\2\2)*\5\n\6\2*\7\3")
        buf.write("\2\2\2+,\7\7\2\2,\61\5\n\6\2-.\7\4\2\2.\60\5\n\6\2/-\3")
        buf.write("\2\2\2\60\63\3\2\2\2\61/\3\2\2\2\61\62\3\2\2\2\62\64\3")
        buf.write("\2\2\2\63\61\3\2\2\2\64\65\7\b\2\2\659\3\2\2\2\66\67\7")
        buf.write("\7\2\2\679\7\b\2\28+\3\2\2\28\66\3\2\2\29\t\3\2\2\2:B")
        buf.write("\5\4\3\2;B\5\b\5\2<B\5\f\7\2=B\5\16\b\2>B\5\20\t\2?B\5")
        buf.write("\22\n\2@B\5\24\13\2A:\3\2\2\2A;\3\2\2\2A<\3\2\2\2A=\3")
        buf.write("\2\2\2A>\3\2\2\2A?\3\2\2\2A@\3\2\2\2B\13\3\2\2\2CD\7\f")
        buf.write("\2\2D\r\3\2\2\2EF\7\r\2\2F\17\3\2\2\2GH\7\13\2\2H\21\3")
        buf.write("\2\2\2IJ\7\t\2\2J\23\3\2\2\2KL\7\n\2\2L\25\3\2\2\2\7\36")
        buf.write("%\618A")
        return buf.getvalue()


class MinmlParser ( Parser ):

    grammarFileName = "Minml.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "','", "'}'", "':'", "'['", "']'", 
                     "'false'", "'null'", "'true'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "FALSE", "NULL", 
                      "TRUE", "STRING", "NUMBER", "WS" ]

    RULE_root = 0
    RULE_obj = 1
    RULE_pair = 2
    RULE_array = 3
    RULE_value = 4
    RULE_string = 5
    RULE_number = 6
    RULE_true = 7
    RULE_false = 8
    RULE_null = 9

    ruleNames =  [ "root", "obj", "pair", "array", "value", "string", "number", 
                   "true", "false", "null" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    FALSE=7
    NULL=8
    TRUE=9
    STRING=10
    NUMBER=11
    WS=12

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self):
            return self.getTypedRuleContext(MinmlParser.ValueContext,0)


        def getRuleIndex(self):
            return MinmlParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = MinmlParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MinmlParser.PairContext)
            else:
                return self.getTypedRuleContext(MinmlParser.PairContext,i)


        def getRuleIndex(self):
            return MinmlParser.RULE_obj

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObj" ):
                listener.enterObj(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObj" ):
                listener.exitObj(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObj" ):
                return visitor.visitObj(self)
            else:
                return visitor.visitChildren(self)




    def obj(self):

        localctx = MinmlParser.ObjContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_obj)
        self._la = 0 # Token type
        try:
            self.state = 35
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 22
                self.match(MinmlParser.T__0)
                self.state = 23
                self.pair()
                self.state = 28
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==MinmlParser.T__1:
                    self.state = 24
                    self.match(MinmlParser.T__1)
                    self.state = 25
                    self.pair()
                    self.state = 30
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 31
                self.match(MinmlParser.T__2)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 33
                self.match(MinmlParser.T__0)
                self.state = 34
                self.match(MinmlParser.T__2)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PairContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.key = None # StringContext

        def value(self):
            return self.getTypedRuleContext(MinmlParser.ValueContext,0)


        def string(self):
            return self.getTypedRuleContext(MinmlParser.StringContext,0)


        def getRuleIndex(self):
            return MinmlParser.RULE_pair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPair" ):
                listener.enterPair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPair" ):
                listener.exitPair(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPair" ):
                return visitor.visitPair(self)
            else:
                return visitor.visitChildren(self)




    def pair(self):

        localctx = MinmlParser.PairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_pair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            localctx.key = self.string()
            self.state = 38
            self.match(MinmlParser.T__3)
            self.state = 39
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MinmlParser.ValueContext)
            else:
                return self.getTypedRuleContext(MinmlParser.ValueContext,i)


        def getRuleIndex(self):
            return MinmlParser.RULE_array

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArray" ):
                listener.enterArray(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArray" ):
                listener.exitArray(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArray" ):
                return visitor.visitArray(self)
            else:
                return visitor.visitChildren(self)




    def array(self):

        localctx = MinmlParser.ArrayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_array)
        self._la = 0 # Token type
        try:
            self.state = 54
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 41
                self.match(MinmlParser.T__4)
                self.state = 42
                self.value()
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==MinmlParser.T__1:
                    self.state = 43
                    self.match(MinmlParser.T__1)
                    self.state = 44
                    self.value()
                    self.state = 49
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 50
                self.match(MinmlParser.T__5)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.match(MinmlParser.T__4)
                self.state = 53
                self.match(MinmlParser.T__5)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def obj(self):
            return self.getTypedRuleContext(MinmlParser.ObjContext,0)


        def array(self):
            return self.getTypedRuleContext(MinmlParser.ArrayContext,0)


        def string(self):
            return self.getTypedRuleContext(MinmlParser.StringContext,0)


        def number(self):
            return self.getTypedRuleContext(MinmlParser.NumberContext,0)


        def true(self):
            return self.getTypedRuleContext(MinmlParser.TrueContext,0)


        def false(self):
            return self.getTypedRuleContext(MinmlParser.FalseContext,0)


        def null(self):
            return self.getTypedRuleContext(MinmlParser.NullContext,0)


        def getRuleIndex(self):
            return MinmlParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = MinmlParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_value)
        try:
            self.state = 63
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [MinmlParser.T__0]:
                self.enterOuterAlt(localctx, 1)
                self.state = 56
                self.obj()
                pass
            elif token in [MinmlParser.T__4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 57
                self.array()
                pass
            elif token in [MinmlParser.STRING]:
                self.enterOuterAlt(localctx, 3)
                self.state = 58
                self.string()
                pass
            elif token in [MinmlParser.NUMBER]:
                self.enterOuterAlt(localctx, 4)
                self.state = 59
                self.number()
                pass
            elif token in [MinmlParser.TRUE]:
                self.enterOuterAlt(localctx, 5)
                self.state = 60
                self.true()
                pass
            elif token in [MinmlParser.FALSE]:
                self.enterOuterAlt(localctx, 6)
                self.state = 61
                self.false()
                pass
            elif token in [MinmlParser.NULL]:
                self.enterOuterAlt(localctx, 7)
                self.state = 62
                self.null()
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


    class StringContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(MinmlParser.STRING, 0)

        def getRuleIndex(self):
            return MinmlParser.RULE_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)




    def string(self):

        localctx = MinmlParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self.match(MinmlParser.STRING)
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

        def NUMBER(self):
            return self.getToken(MinmlParser.NUMBER, 0)

        def getRuleIndex(self):
            return MinmlParser.RULE_number

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

        localctx = MinmlParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.match(MinmlParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TrueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(MinmlParser.TRUE, 0)

        def getRuleIndex(self):
            return MinmlParser.RULE_true

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrue" ):
                listener.enterTrue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrue" ):
                listener.exitTrue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrue" ):
                return visitor.visitTrue(self)
            else:
                return visitor.visitChildren(self)




    def true(self):

        localctx = MinmlParser.TrueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_true)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(MinmlParser.TRUE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FalseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FALSE(self):
            return self.getToken(MinmlParser.FALSE, 0)

        def getRuleIndex(self):
            return MinmlParser.RULE_false

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFalse" ):
                listener.enterFalse(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFalse" ):
                listener.exitFalse(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFalse" ):
                return visitor.visitFalse(self)
            else:
                return visitor.visitChildren(self)




    def false(self):

        localctx = MinmlParser.FalseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_false)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self.match(MinmlParser.FALSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NullContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NULL(self):
            return self.getToken(MinmlParser.NULL, 0)

        def getRuleIndex(self):
            return MinmlParser.RULE_null

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNull" ):
                listener.enterNull(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNull" ):
                listener.exitNull(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNull" ):
                return visitor.visitNull(self)
            else:
                return visitor.visitChildren(self)




    def null(self):

        localctx = MinmlParser.NullContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_null)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(MinmlParser.NULL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
