# flake8: noqa
# Generated from SnowflakeSql.g4 by ANTLR 4.8
from omnibus._vendor.antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\t")
        buf.write("A\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\6\6\6\'\n\6\r\6\16")
        buf.write("\6(\3\7\3\7\5\7-\n\7\3\7\3\7\3\7\7\7\62\n\7\f\7\16\7\65")
        buf.write("\13\7\3\b\3\b\3\t\3\t\3\n\6\n<\n\n\r\n\16\n=\3\n\3\n\2")
        buf.write("\2\13\3\3\5\4\7\5\t\6\13\7\r\b\17\2\21\2\23\t\3\2\6\5")
        buf.write("\2<<BBaa\3\2\62;\4\2C\\c|\5\2\13\f\17\17\"\"\2D\2\3\3")
        buf.write("\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2")
        buf.write("\2\2\r\3\2\2\2\2\23\3\2\2\2\3\25\3\2\2\2\5\27\3\2\2\2")
        buf.write("\7\31\3\2\2\2\t \3\2\2\2\13&\3\2\2\2\r,\3\2\2\2\17\66")
        buf.write("\3\2\2\2\218\3\2\2\2\23;\3\2\2\2\25\26\7=\2\2\26\4\3\2")
        buf.write("\2\2\27\30\7.\2\2\30\6\3\2\2\2\31\32\7u\2\2\32\33\7g\2")
        buf.write("\2\33\34\7n\2\2\34\35\7g\2\2\35\36\7e\2\2\36\37\7v\2\2")
        buf.write("\37\b\3\2\2\2 !\7h\2\2!\"\7t\2\2\"#\7q\2\2#$\7o\2\2$\n")
        buf.write("\3\2\2\2%\'\5\17\b\2&%\3\2\2\2\'(\3\2\2\2(&\3\2\2\2()")
        buf.write("\3\2\2\2)\f\3\2\2\2*-\5\21\t\2+-\7a\2\2,*\3\2\2\2,+\3")
        buf.write("\2\2\2-\63\3\2\2\2.\62\5\21\t\2/\62\5\17\b\2\60\62\t\2")
        buf.write("\2\2\61.\3\2\2\2\61/\3\2\2\2\61\60\3\2\2\2\62\65\3\2\2")
        buf.write("\2\63\61\3\2\2\2\63\64\3\2\2\2\64\16\3\2\2\2\65\63\3\2")
        buf.write("\2\2\66\67\t\3\2\2\67\20\3\2\2\289\t\4\2\29\22\3\2\2\2")
        buf.write(":<\t\5\2\2;:\3\2\2\2<=\3\2\2\2=;\3\2\2\2=>\3\2\2\2>?\3")
        buf.write("\2\2\2?@\b\n\2\2@\24\3\2\2\2\b\2(,\61\63=\3\b\2\2")
        return buf.getvalue()


class SnowflakeSqlLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    SELECT = 3
    FROM = 4
    INTEGER_VALUE = 5
    IDENTIFIER = 6
    WS = 7

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "','", "'select'", "'from'" ]

    symbolicNames = [ "<INVALID>",
            "SELECT", "FROM", "INTEGER_VALUE", "IDENTIFIER", "WS" ]

    ruleNames = [ "T__0", "T__1", "SELECT", "FROM", "INTEGER_VALUE", "IDENTIFIER", 
                  "DIGIT", "LETTER", "WS" ]

    grammarFileName = "SnowflakeSql.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
