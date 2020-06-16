# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\t")
        buf.write("\64\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t")
        buf.write("\7\4\b\t\b\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\5\3\5\3\5\3\5\3\5\3\6\3\6\7\6$\n\6\f\6\16\6\'\13\6")
        buf.write("\3\7\6\7*\n\7\r\7\16\7+\3\b\6\b/\n\b\r\b\16\b\60\3\b\3")
        buf.write("\b\2\2\t\3\3\5\4\7\5\t\6\13\7\r\b\17\t\3\2\6\5\2C\\aa")
        buf.write("c|\6\2\62;C\\aac|\3\2\62;\5\2\13\f\17\17\"\"\2\66\2\3")
        buf.write("\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2")
        buf.write("\2\2\2\r\3\2\2\2\2\17\3\2\2\2\3\21\3\2\2\2\5\23\3\2\2")
        buf.write("\2\7\25\3\2\2\2\t\34\3\2\2\2\13!\3\2\2\2\r)\3\2\2\2\17")
        buf.write(".\3\2\2\2\21\22\7=\2\2\22\4\3\2\2\2\23\24\7.\2\2\24\6")
        buf.write("\3\2\2\2\25\26\7u\2\2\26\27\7g\2\2\27\30\7n\2\2\30\31")
        buf.write("\7g\2\2\31\32\7e\2\2\32\33\7v\2\2\33\b\3\2\2\2\34\35\7")
        buf.write("h\2\2\35\36\7t\2\2\36\37\7q\2\2\37 \7o\2\2 \n\3\2\2\2")
        buf.write("!%\t\2\2\2\"$\t\3\2\2#\"\3\2\2\2$\'\3\2\2\2%#\3\2\2\2")
        buf.write("%&\3\2\2\2&\f\3\2\2\2\'%\3\2\2\2(*\t\4\2\2)(\3\2\2\2*")
        buf.write("+\3\2\2\2+)\3\2\2\2+,\3\2\2\2,\16\3\2\2\2-/\t\5\2\2.-")
        buf.write("\3\2\2\2/\60\3\2\2\2\60.\3\2\2\2\60\61\3\2\2\2\61\62\3")
        buf.write("\2\2\2\62\63\b\b\2\2\63\20\3\2\2\2\6\2%+\60\3\b\2\2")
        return buf.getvalue()


class SnowflakeSqlLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    SELECT = 3
    FROM = 4
    IDENTIFIER = 5
    INTEGER = 6
    WS = 7

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "','", "'select'", "'from'" ]

    symbolicNames = [ "<INVALID>",
            "SELECT", "FROM", "IDENTIFIER", "INTEGER", "WS" ]

    ruleNames = [ "T__0", "T__1", "SELECT", "FROM", "IDENTIFIER", "INTEGER", 
                  "WS" ]

    grammarFileName = "SnowflakeSql.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
