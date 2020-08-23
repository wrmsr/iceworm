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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\21")
        buf.write("_\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2\3\2")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3%\n\3\3\4\3\4\3\4")
        buf.write("\3\4\7\4+\n\4\f\4\16\4.\13\4\3\4\5\4\61\n\4\3\4\3\4\3")
        buf.write("\4\3\4\5\4\67\n\4\3\5\3\5\3\5\3\5\3\6\3\6\5\6?\n\6\3\7")
        buf.write("\3\7\3\7\3\7\7\7E\n\7\f\7\16\7H\13\7\3\7\5\7K\n\7\3\7")
        buf.write("\3\7\3\7\3\7\5\7Q\n\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13")
        buf.write("\3\f\3\f\3\r\3\r\3\r\2\2\16\2\4\6\b\n\f\16\20\22\24\26")
        buf.write("\30\2\3\3\2\f\r\2`\2\32\3\2\2\2\4$\3\2\2\2\6\66\3\2\2")
        buf.write("\2\b8\3\2\2\2\n>\3\2\2\2\fP\3\2\2\2\16R\3\2\2\2\20T\3")
        buf.write("\2\2\2\22V\3\2\2\2\24X\3\2\2\2\26Z\3\2\2\2\30\\\3\2\2")
        buf.write("\2\32\33\5\4\3\2\33\3\3\2\2\2\34%\5\6\4\2\35%\5\f\7\2")
        buf.write("\36%\5\16\b\2\37%\5\20\t\2 %\5\22\n\2!%\5\24\13\2\"%\5")
        buf.write("\26\f\2#%\5\30\r\2$\34\3\2\2\2$\35\3\2\2\2$\36\3\2\2\2")
        buf.write("$\37\3\2\2\2$ \3\2\2\2$!\3\2\2\2$\"\3\2\2\2$#\3\2\2\2")
        buf.write("%\5\3\2\2\2&\'\7\3\2\2\',\5\b\5\2()\7\4\2\2)+\5\b\5\2")
        buf.write("*(\3\2\2\2+.\3\2\2\2,*\3\2\2\2,-\3\2\2\2-\60\3\2\2\2.")
        buf.write(",\3\2\2\2/\61\7\4\2\2\60/\3\2\2\2\60\61\3\2\2\2\61\62")
        buf.write("\3\2\2\2\62\63\7\5\2\2\63\67\3\2\2\2\64\65\7\3\2\2\65")
        buf.write("\67\7\5\2\2\66&\3\2\2\2\66\64\3\2\2\2\67\7\3\2\2\289\5")
        buf.write("\n\6\29:\7\6\2\2:;\5\4\3\2;\t\3\2\2\2<?\5\16\b\2=?\5\20")
        buf.write("\t\2><\3\2\2\2>=\3\2\2\2?\13\3\2\2\2@A\7\7\2\2AF\5\4\3")
        buf.write("\2BC\7\4\2\2CE\5\4\3\2DB\3\2\2\2EH\3\2\2\2FD\3\2\2\2F")
        buf.write("G\3\2\2\2GJ\3\2\2\2HF\3\2\2\2IK\7\4\2\2JI\3\2\2\2JK\3")
        buf.write("\2\2\2KL\3\2\2\2LM\7\b\2\2MQ\3\2\2\2NO\7\7\2\2OQ\7\b\2")
        buf.write("\2P@\3\2\2\2PN\3\2\2\2Q\r\3\2\2\2RS\7\16\2\2S\17\3\2\2")
        buf.write("\2TU\t\2\2\2U\21\3\2\2\2VW\7\17\2\2W\23\3\2\2\2XY\7\13")
        buf.write("\2\2Y\25\3\2\2\2Z[\7\t\2\2[\27\3\2\2\2\\]\7\n\2\2]\31")
        buf.write("\3\2\2\2\n$,\60\66>FJP")
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
                      "TRUE", "DQ_STRING", "SQ_STRING", "IDENTIFIER", "NUMBER", 
                      "COMMENT", "WS" ]

    RULE_root = 0
    RULE_value = 1
    RULE_obj = 2
    RULE_pair = 3
    RULE_key = 4
    RULE_array = 5
    RULE_identifier = 6
    RULE_string = 7
    RULE_number = 8
    RULE_true = 9
    RULE_false = 10
    RULE_null = 11

    ruleNames =  [ "root", "value", "obj", "pair", "key", "array", "identifier", 
                   "string", "number", "true", "false", "null" ]

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
    DQ_STRING=10
    SQ_STRING=11
    IDENTIFIER=12
    NUMBER=13
    COMMENT=14
    WS=15

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
            self.state = 24
            self.value()
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


        def identifier(self):
            return self.getTypedRuleContext(MinmlParser.IdentifierContext,0)


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
        self.enterRule(localctx, 2, self.RULE_value)
        try:
            self.state = 34
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [MinmlParser.T__0]:
                self.enterOuterAlt(localctx, 1)
                self.state = 26
                self.obj()
                pass
            elif token in [MinmlParser.T__4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 27
                self.array()
                pass
            elif token in [MinmlParser.IDENTIFIER]:
                self.enterOuterAlt(localctx, 3)
                self.state = 28
                self.identifier()
                pass
            elif token in [MinmlParser.DQ_STRING, MinmlParser.SQ_STRING]:
                self.enterOuterAlt(localctx, 4)
                self.state = 29
                self.string()
                pass
            elif token in [MinmlParser.NUMBER]:
                self.enterOuterAlt(localctx, 5)
                self.state = 30
                self.number()
                pass
            elif token in [MinmlParser.TRUE]:
                self.enterOuterAlt(localctx, 6)
                self.state = 31
                self.true()
                pass
            elif token in [MinmlParser.FALSE]:
                self.enterOuterAlt(localctx, 7)
                self.state = 32
                self.false()
                pass
            elif token in [MinmlParser.NULL]:
                self.enterOuterAlt(localctx, 8)
                self.state = 33
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
        self.enterRule(localctx, 4, self.RULE_obj)
        self._la = 0 # Token type
        try:
            self.state = 52
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 36
                self.match(MinmlParser.T__0)
                self.state = 37
                self.pair()
                self.state = 42
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 38
                        self.match(MinmlParser.T__1)
                        self.state = 39
                        self.pair() 
                    self.state = 44
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

                self.state = 46
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==MinmlParser.T__1:
                    self.state = 45
                    self.match(MinmlParser.T__1)


                self.state = 48
                self.match(MinmlParser.T__2)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 50
                self.match(MinmlParser.T__0)
                self.state = 51
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

        def key(self):
            return self.getTypedRuleContext(MinmlParser.KeyContext,0)


        def value(self):
            return self.getTypedRuleContext(MinmlParser.ValueContext,0)


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
        self.enterRule(localctx, 6, self.RULE_pair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.key()
            self.state = 55
            self.match(MinmlParser.T__3)
            self.state = 56
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(MinmlParser.IdentifierContext,0)


        def string(self):
            return self.getTypedRuleContext(MinmlParser.StringContext,0)


        def getRuleIndex(self):
            return MinmlParser.RULE_key

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKey" ):
                listener.enterKey(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKey" ):
                listener.exitKey(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKey" ):
                return visitor.visitKey(self)
            else:
                return visitor.visitChildren(self)




    def key(self):

        localctx = MinmlParser.KeyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_key)
        try:
            self.state = 60
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [MinmlParser.IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 58
                self.identifier()
                pass
            elif token in [MinmlParser.DQ_STRING, MinmlParser.SQ_STRING]:
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.string()
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
        self.enterRule(localctx, 10, self.RULE_array)
        self._la = 0 # Token type
        try:
            self.state = 78
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 62
                self.match(MinmlParser.T__4)
                self.state = 63
                self.value()
                self.state = 68
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 64
                        self.match(MinmlParser.T__1)
                        self.state = 65
                        self.value() 
                    self.state = 70
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

                self.state = 72
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==MinmlParser.T__1:
                    self.state = 71
                    self.match(MinmlParser.T__1)


                self.state = 74
                self.match(MinmlParser.T__5)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 76
                self.match(MinmlParser.T__4)
                self.state = 77
                self.match(MinmlParser.T__5)
                pass


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
            return self.getToken(MinmlParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return MinmlParser.RULE_identifier

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

        localctx = MinmlParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(MinmlParser.IDENTIFIER)
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

        def DQ_STRING(self):
            return self.getToken(MinmlParser.DQ_STRING, 0)

        def SQ_STRING(self):
            return self.getToken(MinmlParser.SQ_STRING, 0)

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
        self.enterRule(localctx, 14, self.RULE_string)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            _la = self._input.LA(1)
            if not(_la==MinmlParser.DQ_STRING or _la==MinmlParser.SQ_STRING):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
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
        self.enterRule(localctx, 16, self.RULE_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
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
        self.enterRule(localctx, 18, self.RULE_true)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
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
        self.enterRule(localctx, 20, self.RULE_false)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
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
        self.enterRule(localctx, 22, self.RULE_null)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.match(MinmlParser.NULL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
