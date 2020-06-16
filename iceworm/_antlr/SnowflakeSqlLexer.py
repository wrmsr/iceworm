# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\21")
        buf.write("k\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\3\2\3\2")
        buf.write("\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3")
        buf.write("\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n")
        buf.write("\3\13\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3")
        buf.write("\r\3\16\6\16Q\n\16\r\16\16\16R\3\17\3\17\5\17W\n\17\3")
        buf.write("\17\3\17\3\17\7\17\\\n\17\f\17\16\17_\13\17\3\20\3\20")
        buf.write("\3\21\3\21\3\22\6\22f\n\22\r\22\16\22g\3\22\3\22\2\2\23")
        buf.write("\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31")
        buf.write("\16\33\17\35\20\37\2!\2#\21\3\2\6\5\2<<BBaa\3\2\62;\4")
        buf.write("\2C\\c|\5\2\13\f\17\17\"\"\2n\2\3\3\2\2\2\2\5\3\2\2\2")
        buf.write("\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17")
        buf.write("\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3")
        buf.write("\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2#\3\2\2")
        buf.write("\2\3%\3\2\2\2\5\'\3\2\2\2\7)\3\2\2\2\t+\3\2\2\2\13-\3")
        buf.write("\2\2\2\r\61\3\2\2\2\17\64\3\2\2\2\219\3\2\2\2\23>\3\2")
        buf.write("\2\2\25B\3\2\2\2\27E\3\2\2\2\31H\3\2\2\2\33P\3\2\2\2\35")
        buf.write("V\3\2\2\2\37`\3\2\2\2!b\3\2\2\2#e\3\2\2\2%&\7=\2\2&\4")
        buf.write("\3\2\2\2\'(\7.\2\2(\6\3\2\2\2)*\7*\2\2*\b\3\2\2\2+,\7")
        buf.write("+\2\2,\n\3\2\2\2-.\7c\2\2./\7p\2\2/\60\7f\2\2\60\f\3\2")
        buf.write("\2\2\61\62\7c\2\2\62\63\7u\2\2\63\16\3\2\2\2\64\65\7h")
        buf.write("\2\2\65\66\7t\2\2\66\67\7q\2\2\678\7o\2\28\20\3\2\2\2")
        buf.write("9:\7l\2\2:;\7q\2\2;<\7k\2\2<=\7p\2\2=\22\3\2\2\2>?\7p")
        buf.write("\2\2?@\7q\2\2@A\7v\2\2A\24\3\2\2\2BC\7q\2\2CD\7p\2\2D")
        buf.write("\26\3\2\2\2EF\7q\2\2FG\7t\2\2G\30\3\2\2\2HI\7u\2\2IJ\7")
        buf.write("g\2\2JK\7n\2\2KL\7g\2\2LM\7e\2\2MN\7v\2\2N\32\3\2\2\2")
        buf.write("OQ\5\37\20\2PO\3\2\2\2QR\3\2\2\2RP\3\2\2\2RS\3\2\2\2S")
        buf.write("\34\3\2\2\2TW\5!\21\2UW\7a\2\2VT\3\2\2\2VU\3\2\2\2W]\3")
        buf.write("\2\2\2X\\\5!\21\2Y\\\5\37\20\2Z\\\t\2\2\2[X\3\2\2\2[Y")
        buf.write("\3\2\2\2[Z\3\2\2\2\\_\3\2\2\2][\3\2\2\2]^\3\2\2\2^\36")
        buf.write("\3\2\2\2_]\3\2\2\2`a\t\3\2\2a \3\2\2\2bc\t\4\2\2c\"\3")
        buf.write("\2\2\2df\t\5\2\2ed\3\2\2\2fg\3\2\2\2ge\3\2\2\2gh\3\2\2")
        buf.write("\2hi\3\2\2\2ij\b\22\2\2j$\3\2\2\2\b\2RV[]g\3\b\2\2")
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
    ON = 10
    OR = 11
    SELECT = 12
    INTEGER_VALUE = 13
    IDENTIFIER = 14
    WS = 15

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "','", "'('", "')'", "'and'", "'as'", "'from'", "'join'", 
            "'not'", "'on'", "'or'", "'select'" ]

    symbolicNames = [ "<INVALID>",
            "AND", "AS", "FROM", "JOIN", "NOT", "ON", "OR", "SELECT", "INTEGER_VALUE", 
            "IDENTIFIER", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "AND", "AS", "FROM", "JOIN", 
                  "NOT", "ON", "OR", "SELECT", "INTEGER_VALUE", "IDENTIFIER", 
                  "DIGIT", "LETTER", "WS" ]

    grammarFileName = "SnowflakeSql.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
