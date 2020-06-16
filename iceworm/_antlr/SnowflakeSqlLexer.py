# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\13")
        buf.write("I\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\3\2\3\3")
        buf.write("\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\b\6\b/\n\b\r\b\16\b\60\3\t\3\t\5\t\65")
        buf.write("\n\t\3\t\3\t\3\t\7\t:\n\t\f\t\16\t=\13\t\3\n\3\n\3\13")
        buf.write("\3\13\3\f\6\fD\n\f\r\f\16\fE\3\f\3\f\2\2\r\3\3\5\4\7\5")
        buf.write("\t\6\13\7\r\b\17\t\21\n\23\2\25\2\27\13\3\2\6\5\2<<BB")
        buf.write("aa\3\2\62;\4\2C\\c|\5\2\13\f\17\17\"\"\2L\2\3\3\2\2\2")
        buf.write("\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r")
        buf.write("\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\27\3\2\2\2\3\31\3")
        buf.write("\2\2\2\5\33\3\2\2\2\7\35\3\2\2\2\t\37\3\2\2\2\13!\3\2")
        buf.write("\2\2\r(\3\2\2\2\17.\3\2\2\2\21\64\3\2\2\2\23>\3\2\2\2")
        buf.write("\25@\3\2\2\2\27C\3\2\2\2\31\32\7=\2\2\32\4\3\2\2\2\33")
        buf.write("\34\7.\2\2\34\6\3\2\2\2\35\36\7*\2\2\36\b\3\2\2\2\37 ")
        buf.write("\7+\2\2 \n\3\2\2\2!\"\7u\2\2\"#\7g\2\2#$\7n\2\2$%\7g\2")
        buf.write("\2%&\7e\2\2&\'\7v\2\2\'\f\3\2\2\2()\7h\2\2)*\7t\2\2*+")
        buf.write("\7q\2\2+,\7o\2\2,\16\3\2\2\2-/\5\23\n\2.-\3\2\2\2/\60")
        buf.write("\3\2\2\2\60.\3\2\2\2\60\61\3\2\2\2\61\20\3\2\2\2\62\65")
        buf.write("\5\25\13\2\63\65\7a\2\2\64\62\3\2\2\2\64\63\3\2\2\2\65")
        buf.write(";\3\2\2\2\66:\5\25\13\2\67:\5\23\n\28:\t\2\2\29\66\3\2")
        buf.write("\2\29\67\3\2\2\298\3\2\2\2:=\3\2\2\2;9\3\2\2\2;<\3\2\2")
        buf.write("\2<\22\3\2\2\2=;\3\2\2\2>?\t\3\2\2?\24\3\2\2\2@A\t\4\2")
        buf.write("\2A\26\3\2\2\2BD\t\5\2\2CB\3\2\2\2DE\3\2\2\2EC\3\2\2\2")
        buf.write("EF\3\2\2\2FG\3\2\2\2GH\b\f\2\2H\30\3\2\2\2\b\2\60\649")
        buf.write(";E\3\b\2\2")
        return buf.getvalue()


class SnowflakeSqlLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    SELECT = 5
    FROM = 6
    INTEGER_VALUE = 7
    IDENTIFIER = 8
    WS = 9

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "','", "'('", "')'", "'select'", "'from'" ]

    symbolicNames = [ "<INVALID>",
            "SELECT", "FROM", "INTEGER_VALUE", "IDENTIFIER", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "SELECT", "FROM", "INTEGER_VALUE", 
                  "IDENTIFIER", "DIGIT", "LETTER", "WS" ]

    grammarFileName = "SnowflakeSql.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
