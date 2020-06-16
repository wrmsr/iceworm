# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\17")
        buf.write("_\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\3\2\3\2\3\3\3\3\3\4\3\4\3\5")
        buf.write("\3\5\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3")
        buf.write("\t\3\t\3\t\3\t\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3")
        buf.write("\13\3\13\3\f\6\fE\n\f\r\f\16\fF\3\r\3\r\5\rK\n\r\3\r\3")
        buf.write("\r\3\r\7\rP\n\r\f\r\16\rS\13\r\3\16\3\16\3\17\3\17\3\20")
        buf.write("\6\20Z\n\20\r\20\16\20[\3\20\3\20\2\2\21\3\3\5\4\7\5\t")
        buf.write("\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\2\35\2")
        buf.write("\37\17\3\2\6\5\2<<BBaa\3\2\62;\4\2C\\c|\5\2\13\f\17\17")
        buf.write("\"\"\2b\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2")
        buf.write("\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2")
        buf.write("\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2")
        buf.write("\37\3\2\2\2\3!\3\2\2\2\5#\3\2\2\2\7%\3\2\2\2\t\'\3\2\2")
        buf.write("\2\13)\3\2\2\2\r-\3\2\2\2\17\60\3\2\2\2\21\65\3\2\2\2")
        buf.write("\239\3\2\2\2\25<\3\2\2\2\27D\3\2\2\2\31J\3\2\2\2\33T\3")
        buf.write("\2\2\2\35V\3\2\2\2\37Y\3\2\2\2!\"\7=\2\2\"\4\3\2\2\2#")
        buf.write("$\7.\2\2$\6\3\2\2\2%&\7*\2\2&\b\3\2\2\2\'(\7+\2\2(\n\3")
        buf.write("\2\2\2)*\7c\2\2*+\7p\2\2+,\7f\2\2,\f\3\2\2\2-.\7c\2\2")
        buf.write("./\7u\2\2/\16\3\2\2\2\60\61\7h\2\2\61\62\7t\2\2\62\63")
        buf.write("\7q\2\2\63\64\7o\2\2\64\20\3\2\2\2\65\66\7p\2\2\66\67")
        buf.write("\7q\2\2\678\7v\2\28\22\3\2\2\29:\7q\2\2:;\7t\2\2;\24\3")
        buf.write("\2\2\2<=\7u\2\2=>\7g\2\2>?\7n\2\2?@\7g\2\2@A\7e\2\2AB")
        buf.write("\7v\2\2B\26\3\2\2\2CE\5\33\16\2DC\3\2\2\2EF\3\2\2\2FD")
        buf.write("\3\2\2\2FG\3\2\2\2G\30\3\2\2\2HK\5\35\17\2IK\7a\2\2JH")
        buf.write("\3\2\2\2JI\3\2\2\2KQ\3\2\2\2LP\5\35\17\2MP\5\33\16\2N")
        buf.write("P\t\2\2\2OL\3\2\2\2OM\3\2\2\2ON\3\2\2\2PS\3\2\2\2QO\3")
        buf.write("\2\2\2QR\3\2\2\2R\32\3\2\2\2SQ\3\2\2\2TU\t\3\2\2U\34\3")
        buf.write("\2\2\2VW\t\4\2\2W\36\3\2\2\2XZ\t\5\2\2YX\3\2\2\2Z[\3\2")
        buf.write("\2\2[Y\3\2\2\2[\\\3\2\2\2\\]\3\2\2\2]^\b\20\2\2^ \3\2")
        buf.write("\2\2\b\2FJOQ[\3\b\2\2")
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
    NOT = 8
    OR = 9
    SELECT = 10
    INTEGER_VALUE = 11
    IDENTIFIER = 12
    WS = 13

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "','", "'('", "')'", "'and'", "'as'", "'from'", "'not'", 
            "'or'", "'select'" ]

    symbolicNames = [ "<INVALID>",
            "AND", "AS", "FROM", "NOT", "OR", "SELECT", "INTEGER_VALUE", 
            "IDENTIFIER", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "AND", "AS", "FROM", "NOT", 
                  "OR", "SELECT", "INTEGER_VALUE", "IDENTIFIER", "DIGIT", 
                  "LETTER", "WS" ]

    grammarFileName = "SnowflakeSql.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
