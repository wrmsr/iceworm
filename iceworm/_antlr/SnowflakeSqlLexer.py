# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\20")
        buf.write("f\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\3\2\3\2\3\3\3\3\3")
        buf.write("\4\3\4\3\5\3\5\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3\b")
        buf.write("\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\13\3\13")
        buf.write("\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\6\rL\n\r\r\r\16")
        buf.write("\rM\3\16\3\16\5\16R\n\16\3\16\3\16\3\16\7\16W\n\16\f\16")
        buf.write("\16\16Z\13\16\3\17\3\17\3\20\3\20\3\21\6\21a\n\21\r\21")
        buf.write("\16\21b\3\21\3\21\2\2\22\3\3\5\4\7\5\t\6\13\7\r\b\17\t")
        buf.write("\21\n\23\13\25\f\27\r\31\16\33\17\35\2\37\2!\20\3\2\6")
        buf.write("\5\2<<BBaa\3\2\62;\4\2C\\c|\5\2\13\f\17\17\"\"\2i\2\3")
        buf.write("\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2")
        buf.write("\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2")
        buf.write("\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2")
        buf.write("\2!\3\2\2\2\3#\3\2\2\2\5%\3\2\2\2\7\'\3\2\2\2\t)\3\2\2")
        buf.write("\2\13+\3\2\2\2\r/\3\2\2\2\17\62\3\2\2\2\21\67\3\2\2\2")
        buf.write("\23<\3\2\2\2\25@\3\2\2\2\27C\3\2\2\2\31K\3\2\2\2\33Q\3")
        buf.write("\2\2\2\35[\3\2\2\2\37]\3\2\2\2!`\3\2\2\2#$\7=\2\2$\4\3")
        buf.write("\2\2\2%&\7.\2\2&\6\3\2\2\2\'(\7*\2\2(\b\3\2\2\2)*\7+\2")
        buf.write("\2*\n\3\2\2\2+,\7c\2\2,-\7p\2\2-.\7f\2\2.\f\3\2\2\2/\60")
        buf.write("\7c\2\2\60\61\7u\2\2\61\16\3\2\2\2\62\63\7h\2\2\63\64")
        buf.write("\7t\2\2\64\65\7q\2\2\65\66\7o\2\2\66\20\3\2\2\2\678\7")
        buf.write("l\2\289\7q\2\29:\7k\2\2:;\7p\2\2;\22\3\2\2\2<=\7p\2\2")
        buf.write("=>\7q\2\2>?\7v\2\2?\24\3\2\2\2@A\7q\2\2AB\7t\2\2B\26\3")
        buf.write("\2\2\2CD\7u\2\2DE\7g\2\2EF\7n\2\2FG\7g\2\2GH\7e\2\2HI")
        buf.write("\7v\2\2I\30\3\2\2\2JL\5\35\17\2KJ\3\2\2\2LM\3\2\2\2MK")
        buf.write("\3\2\2\2MN\3\2\2\2N\32\3\2\2\2OR\5\37\20\2PR\7a\2\2QO")
        buf.write("\3\2\2\2QP\3\2\2\2RX\3\2\2\2SW\5\37\20\2TW\5\35\17\2U")
        buf.write("W\t\2\2\2VS\3\2\2\2VT\3\2\2\2VU\3\2\2\2WZ\3\2\2\2XV\3")
        buf.write("\2\2\2XY\3\2\2\2Y\34\3\2\2\2ZX\3\2\2\2[\\\t\3\2\2\\\36")
        buf.write("\3\2\2\2]^\t\4\2\2^ \3\2\2\2_a\t\5\2\2`_\3\2\2\2ab\3\2")
        buf.write("\2\2b`\3\2\2\2bc\3\2\2\2cd\3\2\2\2de\b\21\2\2e\"\3\2\2")
        buf.write("\2\b\2MQVXb\3\b\2\2")
        return buf.getvalue()


class SnowflakeSqlLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    AND = 5
    AS = 6
    FROM = 7
    JOIN = 8
    NOT = 9
    OR = 10
    SELECT = 11
    INTEGER_VALUE = 12
    IDENTIFIER = 13
    WS = 14

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "','", "'('", "')'", "'and'", "'as'", "'from'", "'join'", 
            "'not'", "'or'", "'select'" ]

    symbolicNames = [ "<INVALID>",
            "AND", "AS", "FROM", "JOIN", "NOT", "OR", "SELECT", "INTEGER_VALUE", 
            "IDENTIFIER", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "AND", "AS", "FROM", "JOIN", 
                  "NOT", "OR", "SELECT", "INTEGER_VALUE", "IDENTIFIER", 
                  "DIGIT", "LETTER", "WS" ]

    grammarFileName = "SnowflakeSql.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
