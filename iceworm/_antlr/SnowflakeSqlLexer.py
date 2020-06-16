# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\f")
        buf.write("N\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2")
        buf.write("\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\t\6\t\64\n\t\r\t")
        buf.write("\16\t\65\3\n\3\n\5\n:\n\n\3\n\3\n\3\n\7\n?\n\n\f\n\16")
        buf.write("\nB\13\n\3\13\3\13\3\f\3\f\3\r\6\rI\n\r\r\r\16\rJ\3\r")
        buf.write("\3\r\2\2\16\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25")
        buf.write("\2\27\2\31\f\3\2\6\5\2<<BBaa\3\2\62;\4\2C\\c|\5\2\13\f")
        buf.write("\17\17\"\"\2Q\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t")
        buf.write("\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3")
        buf.write("\2\2\2\2\23\3\2\2\2\2\31\3\2\2\2\3\33\3\2\2\2\5\35\3\2")
        buf.write("\2\2\7\37\3\2\2\2\t!\3\2\2\2\13#\3\2\2\2\r&\3\2\2\2\17")
        buf.write("-\3\2\2\2\21\63\3\2\2\2\239\3\2\2\2\25C\3\2\2\2\27E\3")
        buf.write("\2\2\2\31H\3\2\2\2\33\34\7=\2\2\34\4\3\2\2\2\35\36\7.")
        buf.write("\2\2\36\6\3\2\2\2\37 \7*\2\2 \b\3\2\2\2!\"\7+\2\2\"\n")
        buf.write("\3\2\2\2#$\7c\2\2$%\7u\2\2%\f\3\2\2\2&\'\7u\2\2\'(\7g")
        buf.write("\2\2()\7n\2\2)*\7g\2\2*+\7e\2\2+,\7v\2\2,\16\3\2\2\2-")
        buf.write(".\7h\2\2./\7t\2\2/\60\7q\2\2\60\61\7o\2\2\61\20\3\2\2")
        buf.write("\2\62\64\5\25\13\2\63\62\3\2\2\2\64\65\3\2\2\2\65\63\3")
        buf.write("\2\2\2\65\66\3\2\2\2\66\22\3\2\2\2\67:\5\27\f\28:\7a\2")
        buf.write("\29\67\3\2\2\298\3\2\2\2:@\3\2\2\2;?\5\27\f\2<?\5\25\13")
        buf.write("\2=?\t\2\2\2>;\3\2\2\2><\3\2\2\2>=\3\2\2\2?B\3\2\2\2@")
        buf.write(">\3\2\2\2@A\3\2\2\2A\24\3\2\2\2B@\3\2\2\2CD\t\3\2\2D\26")
        buf.write("\3\2\2\2EF\t\4\2\2F\30\3\2\2\2GI\t\5\2\2HG\3\2\2\2IJ\3")
        buf.write("\2\2\2JH\3\2\2\2JK\3\2\2\2KL\3\2\2\2LM\b\r\2\2M\32\3\2")
        buf.write("\2\2\b\2\659>@J\3\b\2\2")
        return buf.getvalue()


class SnowflakeSqlLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    AS = 5
    SELECT = 6
    FROM = 7
    INTEGER_VALUE = 8
    IDENTIFIER = 9
    WS = 10

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "','", "'('", "')'", "'as'", "'select'", "'from'" ]

    symbolicNames = [ "<INVALID>",
            "AS", "SELECT", "FROM", "INTEGER_VALUE", "IDENTIFIER", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "AS", "SELECT", "FROM", 
                  "INTEGER_VALUE", "IDENTIFIER", "DIGIT", "LETTER", "WS" ]

    grammarFileName = "SnowflakeSql.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
