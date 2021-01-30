# flake8: noqa
# type: ignore
# Generated from IceSql.g4 by ANTLR 4.8
# encoding: utf-8
from omnibus._vendor.antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


import dataclasses


@dataclasses.dataclass(frozen=True)
class IceSqlParserConfig:
    interval_units: bool = False


DEFAULT_ICE_SQL_PARSER_CONFIG = IceSqlParserConfig()


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3~")
        buf.write("\u0367\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t")
        buf.write("&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.\t.\4")
        buf.write("/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64\t\64")
        buf.write("\4\65\t\65\4\66\t\66\3\2\3\2\3\2\3\3\3\3\3\3\3\3\5\3t")
        buf.write("\n\3\3\4\3\4\3\4\5\4y\n\4\3\4\3\4\3\4\3\4\3\4\3\4\7\4")
        buf.write("\u0081\n\4\f\4\16\4\u0084\13\4\3\4\3\4\5\4\u0088\n\4\3")
        buf.write("\4\3\4\5\4\u008c\n\4\3\5\3\5\5\5\u0090\n\5\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\7\3\7\3\7\3\7\3\7\5\7\u009c\n\7\3\b\3\b\3\t")
        buf.write("\3\t\3\t\3\t\7\t\u00a4\n\t\f\t\16\t\u00a7\13\t\5\t\u00a9")
        buf.write("\n\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13\7\13\u00b5")
        buf.write("\n\13\f\13\16\13\u00b8\13\13\3\f\3\f\5\f\u00bc\n\f\3\f")
        buf.write("\3\f\3\r\3\r\3\r\3\r\3\r\5\r\u00c5\n\r\5\r\u00c7\n\r\3")
        buf.write("\16\3\16\3\16\3\16\3\16\5\16\u00ce\n\16\3\17\3\17\5\17")
        buf.write("\u00d2\n\17\3\17\5\17\u00d5\n\17\3\17\3\17\3\17\7\17\u00da")
        buf.write("\n\17\f\17\16\17\u00dd\13\17\3\17\3\17\3\17\3\17\7\17")
        buf.write("\u00e3\n\17\f\17\16\17\u00e6\13\17\5\17\u00e8\n\17\3\17")
        buf.write("\3\17\5\17\u00ec\n\17\3\17\3\17\3\17\5\17\u00f1\n\17\3")
        buf.write("\17\3\17\5\17\u00f5\n\17\3\17\3\17\5\17\u00f9\n\17\3\17")
        buf.write("\3\17\3\17\3\17\3\17\7\17\u0100\n\17\f\17\16\17\u0103")
        buf.write("\13\17\5\17\u0105\n\17\3\17\3\17\5\17\u0109\n\17\3\20")
        buf.write("\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3\21\5\21\u0115")
        buf.write("\n\21\3\21\5\21\u0118\n\21\5\21\u011a\n\21\3\22\3\22\3")
        buf.write("\23\3\23\3\23\5\23\u0121\n\23\3\23\3\23\5\23\u0125\n\23")
        buf.write("\3\23\3\23\3\23\7\23\u012a\n\23\f\23\16\23\u012d\13\23")
        buf.write("\3\24\3\24\3\24\3\24\3\24\5\24\u0134\n\24\3\24\3\24\5")
        buf.write("\24\u0138\n\24\3\24\3\24\3\24\3\24\3\24\3\24\5\24\u0140")
        buf.write("\n\24\3\24\3\24\3\24\3\24\3\24\7\24\u0147\n\24\f\24\16")
        buf.write("\24\u014a\13\24\3\24\3\24\3\24\5\24\u014f\n\24\3\24\3")
        buf.write("\24\3\24\3\24\3\24\3\24\5\24\u0157\n\24\3\24\3\24\3\24")
        buf.write("\5\24\u015c\n\24\3\24\3\24\5\24\u0160\n\24\3\24\3\24\3")
        buf.write("\24\3\24\3\24\7\24\u0167\n\24\f\24\16\24\u016a\13\24\3")
        buf.write("\24\3\24\5\24\u016e\n\24\3\24\3\24\5\24\u0172\n\24\5\24")
        buf.write("\u0174\n\24\3\25\3\25\3\25\3\25\3\25\5\25\u017b\n\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u0185\n\25")
        buf.write("\3\25\3\25\3\25\3\25\5\25\u018b\n\25\3\25\3\25\3\25\3")
        buf.write("\25\3\25\3\25\7\25\u0193\n\25\f\25\16\25\u0196\13\25\3")
        buf.write("\25\3\25\3\25\7\25\u019b\n\25\f\25\16\25\u019e\13\25\3")
        buf.write("\26\3\26\3\26\5\26\u01a3\n\26\3\27\3\27\3\27\5\27\u01a8")
        buf.write("\n\27\3\27\7\27\u01ab\n\27\f\27\16\27\u01ae\13\27\3\27")
        buf.write("\3\27\5\27\u01b2\n\27\3\27\3\27\3\27\3\27\3\27\3\27\3")
        buf.write("\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27")
        buf.write("\5\27\u01db\n\27\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3")
        buf.write("\30\5\30\u01e5\n\30\3\31\3\31\3\31\3\31\3\31\7\31\u01ec")
        buf.write("\n\31\f\31\16\31\u01ef\13\31\5\31\u01f1\n\31\3\31\5\31")
        buf.write("\u01f4\n\31\3\32\3\32\3\32\5\32\u01f9\n\32\3\32\3\32\3")
        buf.write("\32\7\32\u01fe\n\32\f\32\16\32\u0201\13\32\5\32\u0203")
        buf.write("\n\32\3\32\3\32\3\32\5\32\u0208\n\32\3\32\3\32\3\32\3")
        buf.write("\32\3\32\3\32\3\32\3\32\7\32\u0212\n\32\f\32\16\32\u0215")
        buf.write("\13\32\3\32\3\32\5\32\u0219\n\32\3\32\5\32\u021c\n\32")
        buf.write("\3\32\3\32\3\32\3\32\3\32\7\32\u0223\n\32\f\32\16\32\u0226")
        buf.write("\13\32\3\32\3\32\3\32\5\32\u022b\n\32\3\32\3\32\3\32\3")
        buf.write("\32\3\32\3\32\3\32\3\32\7\32\u0235\n\32\f\32\16\32\u0238")
        buf.write("\13\32\3\32\3\32\5\32\u023c\n\32\3\32\5\32\u023f\n\32")
        buf.write("\3\32\3\32\3\32\5\32\u0244\n\32\3\32\3\32\3\32\3\32\3")
        buf.write("\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\7\32\u0252\n\32")
        buf.write("\f\32\16\32\u0255\13\32\3\32\3\32\5\32\u0259\n\32\3\32")
        buf.write("\5\32\u025c\n\32\3\32\3\32\3\32\3\32\3\32\5\32\u0263\n")
        buf.write("\32\5\32\u0265\n\32\3\33\3\33\3\33\3\33\3\34\3\34\3\34")
        buf.write("\3\34\3\34\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\36")
        buf.write("\7\36\u0279\n\36\f\36\16\36\u027c\13\36\5\36\u027e\n\36")
        buf.write("\3\36\3\36\3\36\3\36\3\36\7\36\u0285\n\36\f\36\16\36\u0288")
        buf.write("\13\36\5\36\u028a\n\36\3\36\5\36\u028d\n\36\3\36\3\36")
        buf.write("\3\37\3\37\3\37\3\37\3\37\3\37\5\37\u0297\n\37\3 \3 \3")
        buf.write(" \3 \3 \3 \3 \3 \5 \u02a1\n \3!\3!\5!\u02a5\n!\3!\3!\5")
        buf.write("!\u02a9\n!\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"")
        buf.write("\3\"\3\"\3\"\5\"\u02b9\n\"\3\"\3\"\5\"\u02bd\n\"\3\"\3")
        buf.write("\"\3\"\3\"\5\"\u02c3\n\"\3\"\3\"\3\"\3\"\3\"\5\"\u02ca")
        buf.write("\n\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3")
        buf.write("\"\3\"\7\"\u02da\n\"\f\"\16\"\u02dd\13\"\5\"\u02df\n\"")
        buf.write("\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3\"\5\"\u02ed")
        buf.write("\n\"\3\"\3\"\3\"\3\"\3\"\5\"\u02f4\n\"\3\"\3\"\3\"\3\"")
        buf.write("\3\"\5\"\u02fb\n\"\7\"\u02fd\n\"\f\"\16\"\u0300\13\"\3")
        buf.write("#\3#\3#\7#\u0305\n#\f#\16#\u0308\13#\3#\3#\3#\3#\3#\3")
        buf.write("#\7#\u0310\n#\f#\16#\u0313\13#\3#\3#\5#\u0317\n#\3$\3")
        buf.write("$\3$\3$\7$\u031d\n$\f$\16$\u0320\13$\3$\3$\3%\3%\3%\7")
        buf.write("%\u0327\n%\f%\16%\u032a\13%\3&\3&\3&\7&\u032f\n&\f&\16")
        buf.write("&\u0332\13&\3\'\3\'\5\'\u0336\n\'\3(\3(\3)\3)\3)\3*\3")
        buf.write("*\3*\3+\3+\3+\5+\u0343\n+\3,\3,\3-\3-\3.\3.\3/\3/\3\60")
        buf.write("\3\60\3\61\3\61\3\62\3\62\3\62\3\62\3\62\3\62\3\62\3\62")
        buf.write("\3\62\3\62\3\62\3\62\5\62\u035d\n\62\3\63\3\63\3\64\3")
        buf.write("\64\3\65\3\65\3\66\3\66\3\66\2\5$(B\67\2\4\6\b\n\f\16")
        buf.write("\20\22\24\26\30\32\34\36 \"$&(*,.\60\62\64\668:<>@BDF")
        buf.write("HJLNPRTVXZ\\^`bdfhj\2\17\4\2\33\33SS\5\2==II__\4\2<<]")
        buf.write("]\7\2\'\';;LMbbqq\4\2\63\63YY\4\2[[aa\4\2\36\36))\4\2")
        buf.write("\62\62FF\4\2\32\32**\3\2\16\24\4\2\6\6\25\31\3\2\25\26")
        buf.write("\22\2!!&\'\60\60\62\6299;;==FFHILMUU[\\^_bbqqvv\2\u03c9")
        buf.write("\2l\3\2\2\2\4s\3\2\2\2\6u\3\2\2\2\b\u008d\3\2\2\2\n\u0091")
        buf.write("\3\2\2\2\f\u0096\3\2\2\2\16\u009d\3\2\2\2\20\u00a8\3\2")
        buf.write("\2\2\22\u00ac\3\2\2\2\24\u00b2\3\2\2\2\26\u00b9\3\2\2")
        buf.write("\2\30\u00c6\3\2\2\2\32\u00cd\3\2\2\2\34\u00cf\3\2\2\2")
        buf.write("\36\u010a\3\2\2\2 \u0119\3\2\2\2\"\u011b\3\2\2\2$\u0124")
        buf.write("\3\2\2\2&\u0173\3\2\2\2(\u017a\3\2\2\2*\u01a2\3\2\2\2")
        buf.write(",\u01da\3\2\2\2.\u01e4\3\2\2\2\60\u01e6\3\2\2\2\62\u0264")
        buf.write("\3\2\2\2\64\u0266\3\2\2\2\66\u026a\3\2\2\28\u026f\3\2")
        buf.write("\2\2:\u0271\3\2\2\2<\u0296\3\2\2\2>\u02a0\3\2\2\2@\u02a2")
        buf.write("\3\2\2\2B\u02b8\3\2\2\2D\u0316\3\2\2\2F\u0318\3\2\2\2")
        buf.write("H\u0323\3\2\2\2J\u032b\3\2\2\2L\u0335\3\2\2\2N\u0337\3")
        buf.write("\2\2\2P\u0339\3\2\2\2R\u033c\3\2\2\2T\u0342\3\2\2\2V\u0344")
        buf.write("\3\2\2\2X\u0346\3\2\2\2Z\u0348\3\2\2\2\\\u034a\3\2\2\2")
        buf.write("^\u034c\3\2\2\2`\u034e\3\2\2\2b\u035c\3\2\2\2d\u035e\3")
        buf.write("\2\2\2f\u0360\3\2\2\2h\u0362\3\2\2\2j\u0364\3\2\2\2lm")
        buf.write("\5\4\3\2mn\7\2\2\3n\3\3\2\2\2ot\5\16\b\2pt\5\6\4\2qt\5")
        buf.write("\n\6\2rt\5\f\7\2so\3\2\2\2sp\3\2\2\2sq\3\2\2\2sr\3\2\2")
        buf.write("\2t\5\3\2\2\2ux\7#\2\2vw\7S\2\2wy\7\\\2\2xv\3\2\2\2xy")
        buf.write("\3\2\2\2yz\3\2\2\2z{\7e\2\2{\u0087\5H%\2|}\7\3\2\2}\u0082")
        buf.write("\5\b\5\2~\177\7\4\2\2\177\u0081\5\b\5\2\u0080~\3\2\2\2")
        buf.write("\u0081\u0084\3\2\2\2\u0082\u0080\3\2\2\2\u0082\u0083\3")
        buf.write("\2\2\2\u0083\u0085\3\2\2\2\u0084\u0082\3\2\2\2\u0085\u0086")
        buf.write("\7\5\2\2\u0086\u0088\3\2\2\2\u0087|\3\2\2\2\u0087\u0088")
        buf.write("\3\2\2\2\u0088\u008b\3\2\2\2\u0089\u008a\7\35\2\2\u008a")
        buf.write("\u008c\5\16\b\2\u008b\u0089\3\2\2\2\u008b\u008c\3\2\2")
        buf.write("\2\u008c\7\3\2\2\2\u008d\u008f\5L\'\2\u008e\u0090\5\60")
        buf.write("\31\2\u008f\u008e\3\2\2\2\u008f\u0090\3\2\2\2\u0090\t")
        buf.write("\3\2\2\2\u0091\u0092\7@\2\2\u0092\u0093\7C\2\2\u0093\u0094")
        buf.write("\5H%\2\u0094\u0095\5\16\b\2\u0095\13\3\2\2\2\u0096\u0097")
        buf.write("\7(\2\2\u0097\u0098\7\65\2\2\u0098\u009b\5H%\2\u0099\u009a")
        buf.write("\7n\2\2\u009a\u009c\5$\23\2\u009b\u0099\3\2\2\2\u009b")
        buf.write("\u009c\3\2\2\2\u009c\r\3\2\2\2\u009d\u009e\5\20\t\2\u009e")
        buf.write("\17\3\2\2\2\u009f\u00a0\7o\2\2\u00a0\u00a5\5\22\n\2\u00a1")
        buf.write("\u00a2\7\4\2\2\u00a2\u00a4\5\22\n\2\u00a3\u00a1\3\2\2")
        buf.write("\2\u00a4\u00a7\3\2\2\2\u00a5\u00a3\3\2\2\2\u00a5\u00a6")
        buf.write("\3\2\2\2\u00a6\u00a9\3\2\2\2\u00a7\u00a5\3\2\2\2\u00a8")
        buf.write("\u009f\3\2\2\2\u00a8\u00a9\3\2\2\2\u00a9\u00aa\3\2\2\2")
        buf.write("\u00aa\u00ab\5\24\13\2\u00ab\21\3\2\2\2\u00ac\u00ad\5")
        buf.write("L\'\2\u00ad\u00ae\7\35\2\2\u00ae\u00af\7\3\2\2\u00af\u00b0")
        buf.write("\5\16\b\2\u00b0\u00b1\7\5\2\2\u00b1\23\3\2\2\2\u00b2\u00b6")
        buf.write("\5\32\16\2\u00b3\u00b5\5\26\f\2\u00b4\u00b3\3\2\2\2\u00b5")
        buf.write("\u00b8\3\2\2\2\u00b6\u00b4\3\2\2\2\u00b6\u00b7\3\2\2\2")
        buf.write("\u00b7\25\3\2\2\2\u00b8\u00b6\3\2\2\2\u00b9\u00bb\5\30")
        buf.write("\r\2\u00ba\u00bc\5`\61\2\u00bb\u00ba\3\2\2\2\u00bb\u00bc")
        buf.write("\3\2\2\2\u00bc\u00bd\3\2\2\2\u00bd\u00be\5\32\16\2\u00be")
        buf.write("\27\3\2\2\2\u00bf\u00c7\7A\2\2\u00c0\u00c7\7K\2\2\u00c1")
        buf.write("\u00c7\7/\2\2\u00c2\u00c4\7j\2\2\u00c3\u00c5\7\32\2\2")
        buf.write("\u00c4\u00c3\3\2\2\2\u00c4\u00c5\3\2\2\2\u00c5\u00c7\3")
        buf.write("\2\2\2\u00c6\u00bf\3\2\2\2\u00c6\u00c0\3\2\2\2\u00c6\u00c1")
        buf.write("\3\2\2\2\u00c6\u00c2\3\2\2\2\u00c7\31\3\2\2\2\u00c8\u00c9")
        buf.write("\7\3\2\2\u00c9\u00ca\5\32\16\2\u00ca\u00cb\7\5\2\2\u00cb")
        buf.write("\u00ce\3\2\2\2\u00cc\u00ce\5\34\17\2\u00cd\u00c8\3\2\2")
        buf.write("\2\u00cd\u00cc\3\2\2\2\u00ce\33\3\2\2\2\u00cf\u00d1\7")
        buf.write("c\2\2\u00d0\u00d2\5\36\20\2\u00d1\u00d0\3\2\2\2\u00d1")
        buf.write("\u00d2\3\2\2\2\u00d2\u00d4\3\2\2\2\u00d3\u00d5\5`\61\2")
        buf.write("\u00d4\u00d3\3\2\2\2\u00d4\u00d5\3\2\2\2\u00d5\u00d6\3")
        buf.write("\2\2\2\u00d6\u00db\5 \21\2\u00d7\u00d8\7\4\2\2\u00d8\u00da")
        buf.write("\5 \21\2\u00d9\u00d7\3\2\2\2\u00da\u00dd\3\2\2\2\u00db")
        buf.write("\u00d9\3\2\2\2\u00db\u00dc\3\2\2\2\u00dc\u00e7\3\2\2\2")
        buf.write("\u00dd\u00db\3\2\2\2\u00de\u00df\7\65\2\2\u00df\u00e4")
        buf.write("\5B\"\2\u00e0\u00e1\7\4\2\2\u00e1\u00e3\5B\"\2\u00e2\u00e0")
        buf.write("\3\2\2\2\u00e3\u00e6\3\2\2\2\u00e4\u00e2\3\2\2\2\u00e4")
        buf.write("\u00e5\3\2\2\2\u00e5\u00e8\3\2\2\2\u00e6\u00e4\3\2\2\2")
        buf.write("\u00e7\u00de\3\2\2\2\u00e7\u00e8\3\2\2\2\u00e8\u00eb\3")
        buf.write("\2\2\2\u00e9\u00ea\7n\2\2\u00ea\u00ec\5$\23\2\u00eb\u00e9")
        buf.write("\3\2\2\2\u00eb\u00ec\3\2\2\2\u00ec\u00f0\3\2\2\2\u00ed")
        buf.write("\u00ee\78\2\2\u00ee\u00ef\7 \2\2\u00ef\u00f1\5D#\2\u00f0")
        buf.write("\u00ed\3\2\2\2\u00f0\u00f1\3\2\2\2\u00f1\u00f4\3\2\2\2")
        buf.write("\u00f2\u00f3\7:\2\2\u00f3\u00f5\5$\23\2\u00f4\u00f2\3")
        buf.write("\2\2\2\u00f4\u00f5\3\2\2\2\u00f5\u00f8\3\2\2\2\u00f6\u00f7")
        buf.write("\7Z\2\2\u00f7\u00f9\5$\23\2\u00f8\u00f6\3\2\2\2\u00f8")
        buf.write("\u00f9\3\2\2\2\u00f9\u0104\3\2\2\2\u00fa\u00fb\7T\2\2")
        buf.write("\u00fb\u00fc\7 \2\2\u00fc\u0101\5@!\2\u00fd\u00fe\7\4")
        buf.write("\2\2\u00fe\u0100\5@!\2\u00ff\u00fd\3\2\2\2\u0100\u0103")
        buf.write("\3\2\2\2\u0101\u00ff\3\2\2\2\u0101\u0102\3\2\2\2\u0102")
        buf.write("\u0105\3\2\2\2\u0103\u0101\3\2\2\2\u0104\u00fa\3\2\2\2")
        buf.write("\u0104\u0105\3\2\2\2\u0105\u0108\3\2\2\2\u0106\u0107\7")
        buf.write("J\2\2\u0107\u0109\7s\2\2\u0108\u0106\3\2\2\2\u0108\u0109")
        buf.write("\3\2\2\2\u0109\35\3\2\2\2\u010a\u010b\7g\2\2\u010b\u010c")
        buf.write("\5T+\2\u010c\37\3\2\2\2\u010d\u011a\7\6\2\2\u010e\u010f")
        buf.write("\5L\'\2\u010f\u0110\7\7\2\2\u0110\u0111\7\6\2\2\u0111")
        buf.write("\u011a\3\2\2\2\u0112\u0117\5\"\22\2\u0113\u0115\7\35\2")
        buf.write("\2\u0114\u0113\3\2\2\2\u0114\u0115\3\2\2\2\u0115\u0116")
        buf.write("\3\2\2\2\u0116\u0118\5L\'\2\u0117\u0114\3\2\2\2\u0117")
        buf.write("\u0118\3\2\2\2\u0118\u011a\3\2\2\2\u0119\u010d\3\2\2\2")
        buf.write("\u0119\u010e\3\2\2\2\u0119\u0112\3\2\2\2\u011a!\3\2\2")
        buf.write("\2\u011b\u011c\5$\23\2\u011c#\3\2\2\2\u011d\u011e\b\23")
        buf.write("\1\2\u011e\u0120\5(\25\2\u011f\u0121\5&\24\2\u0120\u011f")
        buf.write("\3\2\2\2\u0120\u0121\3\2\2\2\u0121\u0125\3\2\2\2\u0122")
        buf.write("\u0123\7O\2\2\u0123\u0125\5$\23\4\u0124\u011d\3\2\2\2")
        buf.write("\u0124\u0122\3\2\2\2\u0125\u012b\3\2\2\2\u0126\u0127\f")
        buf.write("\3\2\2\u0127\u0128\t\2\2\2\u0128\u012a\5$\23\4\u0129\u0126")
        buf.write("\3\2\2\2\u012a\u012d\3\2\2\2\u012b\u0129\3\2\2\2\u012b")
        buf.write("\u012c\3\2\2\2\u012c%\3\2\2\2\u012d\u012b\3\2\2\2\u012e")
        buf.write("\u012f\5d\63\2\u012f\u0130\5(\25\2\u0130\u0174\3\2\2\2")
        buf.write("\u0131\u0133\7D\2\2\u0132\u0134\7O\2\2\u0133\u0132\3\2")
        buf.write("\2\2\u0133\u0134\3\2\2\2\u0134\u0135\3\2\2\2\u0135\u0174")
        buf.write("\7P\2\2\u0136\u0138\7O\2\2\u0137\u0136\3\2\2\2\u0137\u0138")
        buf.write("\3\2\2\2\u0138\u0139\3\2\2\2\u0139\u013a\7\37\2\2\u013a")
        buf.write("\u013b\5(\25\2\u013b\u013c\7\33\2\2\u013c\u013d\5(\25")
        buf.write("\2\u013d\u0174\3\2\2\2\u013e\u0140\7O\2\2\u013f\u013e")
        buf.write("\3\2\2\2\u013f\u0140\3\2\2\2\u0140\u0141\3\2\2\2\u0141")
        buf.write("\u0142\7>\2\2\u0142\u0143\7\3\2\2\u0143\u0148\5\"\22\2")
        buf.write("\u0144\u0145\7\4\2\2\u0145\u0147\5\"\22\2\u0146\u0144")
        buf.write("\3\2\2\2\u0147\u014a\3\2\2\2\u0148\u0146\3\2\2\2\u0148")
        buf.write("\u0149\3\2\2\2\u0149\u014b\3\2\2\2\u014a\u0148\3\2\2\2")
        buf.write("\u014b\u014c\7\5\2\2\u014c\u0174\3\2\2\2\u014d\u014f\7")
        buf.write("O\2\2\u014e\u014d\3\2\2\2\u014e\u014f\3\2\2\2\u014f\u0150")
        buf.write("\3\2\2\2\u0150\u0151\7>\2\2\u0151\u0152\7\3\2\2\u0152")
        buf.write("\u0153\5\16\b\2\u0153\u0154\7\5\2\2\u0154\u0174\3\2\2")
        buf.write("\2\u0155\u0157\7O\2\2\u0156\u0155\3\2\2\2\u0156\u0157")
        buf.write("\3\2\2\2\u0157\u0158\3\2\2\2\u0158\u0159\7>\2\2\u0159")
        buf.write("\u0174\7x\2\2\u015a\u015c\7O\2\2\u015b\u015a\3\2\2\2\u015b")
        buf.write("\u015c\3\2\2\2\u015c\u015d\3\2\2\2\u015d\u015f\t\3\2\2")
        buf.write("\u015e\u0160\7\34\2\2\u015f\u015e\3\2\2\2\u015f\u0160")
        buf.write("\3\2\2\2\u0160\u016d\3\2\2\2\u0161\u016e\5\"\22\2\u0162")
        buf.write("\u0163\7\3\2\2\u0163\u0168\5\"\22\2\u0164\u0165\7\4\2")
        buf.write("\2\u0165\u0167\5\"\22\2\u0166\u0164\3\2\2\2\u0167\u016a")
        buf.write("\3\2\2\2\u0168\u0166\3\2\2\2\u0168\u0169\3\2\2\2\u0169")
        buf.write("\u016b\3\2\2\2\u016a\u0168\3\2\2\2\u016b\u016c\7\5\2\2")
        buf.write("\u016c\u016e\3\2\2\2\u016d\u0161\3\2\2\2\u016d\u0162\3")
        buf.write("\2\2\2\u016e\u0171\3\2\2\2\u016f\u0170\7.\2\2\u0170\u0172")
        buf.write("\5X-\2\u0171\u016f\3\2\2\2\u0171\u0172\3\2\2\2\u0172\u0174")
        buf.write("\3\2\2\2\u0173\u012e\3\2\2\2\u0173\u0131\3\2\2\2\u0173")
        buf.write("\u0137\3\2\2\2\u0173\u013f\3\2\2\2\u0173\u014e\3\2\2\2")
        buf.write("\u0173\u0156\3\2\2\2\u0173\u015b\3\2\2\2\u0174\'\3\2\2")
        buf.write("\2\u0175\u0176\b\25\1\2\u0176\u017b\5,\27\2\u0177\u0178")
        buf.write("\5h\65\2\u0178\u0179\5(\25\6\u0179\u017b\3\2\2\2\u017a")
        buf.write("\u0175\3\2\2\2\u017a\u0177\3\2\2\2\u017b\u019c\3\2\2\2")
        buf.write("\u017c\u017d\f\5\2\2\u017d\u017e\5f\64\2\u017e\u017f\5")
        buf.write("(\25\6\u017f\u019b\3\2\2\2\u0180\u018a\f\4\2\2\u0181\u0182")
        buf.write("\7\b\2\2\u0182\u018b\5*\26\2\u0183\u0185\7\b\2\2\u0184")
        buf.write("\u0183\3\2\2\2\u0184\u0185\3\2\2\2\u0185\u0186\3\2\2\2")
        buf.write("\u0186\u0187\7\t\2\2\u0187\u0188\5*\26\2\u0188\u0189\7")
        buf.write("\n\2\2\u0189\u018b\3\2\2\2\u018a\u0181\3\2\2\2\u018a\u0184")
        buf.write("\3\2\2\2\u018b\u0194\3\2\2\2\u018c\u018d\7\7\2\2\u018d")
        buf.write("\u0193\5*\26\2\u018e\u018f\7\t\2\2\u018f\u0190\5*\26\2")
        buf.write("\u0190\u0191\7\n\2\2\u0191\u0193\3\2\2\2\u0192\u018c\3")
        buf.write("\2\2\2\u0192\u018e\3\2\2\2\u0193\u0196\3\2\2\2\u0194\u0192")
        buf.write("\3\2\2\2\u0194\u0195\3\2\2\2\u0195\u019b\3\2\2\2\u0196")
        buf.write("\u0194\3\2\2\2\u0197\u0198\f\3\2\2\u0198\u0199\7\13\2")
        buf.write("\2\u0199\u019b\5\60\31\2\u019a\u017c\3\2\2\2\u019a\u0180")
        buf.write("\3\2\2\2\u019a\u0197\3\2\2\2\u019b\u019e\3\2\2\2\u019c")
        buf.write("\u019a\3\2\2\2\u019c\u019d\3\2\2\2\u019d)\3\2\2\2\u019e")
        buf.write("\u019c\3\2\2\2\u019f\u01a3\5L\'\2\u01a0\u01a3\5X-\2\u01a1")
        buf.write("\u01a3\5V,\2\u01a2\u019f\3\2\2\2\u01a2\u01a0\3\2\2\2\u01a2")
        buf.write("\u01a1\3\2\2\2\u01a3+\3\2\2\2\u01a4\u01db\5\62\32\2\u01a5")
        buf.write("\u01a7\7!\2\2\u01a6\u01a8\5\"\22\2\u01a7\u01a6\3\2\2\2")
        buf.write("\u01a7\u01a8\3\2\2\2\u01a8\u01ac\3\2\2\2\u01a9\u01ab\5")
        buf.write("\66\34\2\u01aa\u01a9\3\2\2\2\u01ab\u01ae\3\2\2\2\u01ac")
        buf.write("\u01aa\3\2\2\2\u01ac\u01ad\3\2\2\2\u01ad\u01b1\3\2\2\2")
        buf.write("\u01ae\u01ac\3\2\2\2\u01af\u01b0\7,\2\2\u01b0\u01b2\5")
        buf.write("\"\22\2\u01b1\u01af\3\2\2\2\u01b1\u01b2\3\2\2\2\u01b2")
        buf.write("\u01b3\3\2\2\2\u01b3\u01db\7-\2\2\u01b4\u01b5\6\27\6\2")
        buf.write("\u01b5\u01b6\7B\2\2\u01b6\u01db\5\"\22\2\u01b7\u01b8\6")
        buf.write("\27\7\2\u01b8\u01b9\7B\2\2\u01b9\u01ba\5\"\22\2\u01ba")
        buf.write("\u01bb\58\35\2\u01bb\u01db\3\2\2\2\u01bc\u01bd\7B\2\2")
        buf.write("\u01bd\u01be\5\"\22\2\u01be\u01bf\58\35\2\u01bf\u01db")
        buf.write("\3\2\2\2\u01c0\u01c1\7\3\2\2\u01c1\u01c2\5\16\b\2\u01c2")
        buf.write("\u01c3\7\5\2\2\u01c3\u01db\3\2\2\2\u01c4\u01c5\7\3\2\2")
        buf.write("\u01c5\u01c6\5\"\22\2\u01c6\u01c7\7\5\2\2\u01c7\u01db")
        buf.write("\3\2\2\2\u01c8\u01c9\7\"\2\2\u01c9\u01ca\7\3\2\2\u01ca")
        buf.write("\u01cb\5\"\22\2\u01cb\u01cc\7\35\2\2\u01cc\u01cd\5\60")
        buf.write("\31\2\u01cd\u01ce\7\5\2\2\u01ce\u01db\3\2\2\2\u01cf\u01d0")
        buf.write("\7&\2\2\u01d0\u01db\5X-\2\u01d1\u01d2\7\60\2\2\u01d2\u01d3")
        buf.write("\7\3\2\2\u01d3\u01d4\5L\'\2\u01d4\u01d5\7\65\2\2\u01d5")
        buf.write("\u01d6\5\"\22\2\u01d6\u01d7\7\5\2\2\u01d7\u01db\3\2\2")
        buf.write("\2\u01d8\u01db\7x\2\2\u01d9\u01db\5.\30\2\u01da\u01a4")
        buf.write("\3\2\2\2\u01da\u01a5\3\2\2\2\u01da\u01b4\3\2\2\2\u01da")
        buf.write("\u01b7\3\2\2\2\u01da\u01bc\3\2\2\2\u01da\u01c0\3\2\2\2")
        buf.write("\u01da\u01c4\3\2\2\2\u01da\u01c8\3\2\2\2\u01da\u01cf\3")
        buf.write("\2\2\2\u01da\u01d1\3\2\2\2\u01da\u01d8\3\2\2\2\u01da\u01d9")
        buf.write("\3\2\2\2\u01db-\3\2\2\2\u01dc\u01e5\5P)\2\u01dd\u01e5")
        buf.write("\5R*\2\u01de\u01e5\5H%\2\u01df\u01e5\5T+\2\u01e0\u01e5")
        buf.write("\5X-\2\u01e1\u01e5\5Z.\2\u01e2\u01e5\5\\/\2\u01e3\u01e5")
        buf.write("\5^\60\2\u01e4\u01dc\3\2\2\2\u01e4\u01dd\3\2\2\2\u01e4")
        buf.write("\u01de\3\2\2\2\u01e4\u01df\3\2\2\2\u01e4\u01e0\3\2\2\2")
        buf.write("\u01e4\u01e1\3\2\2\2\u01e4\u01e2\3\2\2\2\u01e4\u01e3\3")
        buf.write("\2\2\2\u01e5/\3\2\2\2\u01e6\u01f3\5L\'\2\u01e7\u01f0\7")
        buf.write("\3\2\2\u01e8\u01ed\5.\30\2\u01e9\u01ea\7\4\2\2\u01ea\u01ec")
        buf.write("\5.\30\2\u01eb\u01e9\3\2\2\2\u01ec\u01ef\3\2\2\2\u01ed")
        buf.write("\u01eb\3\2\2\2\u01ed\u01ee\3\2\2\2\u01ee\u01f1\3\2\2\2")
        buf.write("\u01ef\u01ed\3\2\2\2\u01f0\u01e8\3\2\2\2\u01f0\u01f1\3")
        buf.write("\2\2\2\u01f1\u01f2\3\2\2\2\u01f2\u01f4\7\5\2\2\u01f3\u01e7")
        buf.write("\3\2\2\2\u01f3\u01f4\3\2\2\2\u01f4\61\3\2\2\2\u01f5\u01f6")
        buf.write("\5H%\2\u01f6\u01f8\7\3\2\2\u01f7\u01f9\5`\61\2\u01f8\u01f7")
        buf.write("\3\2\2\2\u01f8\u01f9\3\2\2\2\u01f9\u0202\3\2\2\2\u01fa")
        buf.write("\u01ff\5\"\22\2\u01fb\u01fc\7\4\2\2\u01fc\u01fe\5\"\22")
        buf.write("\2\u01fd\u01fb\3\2\2\2\u01fe\u0201\3\2\2\2\u01ff\u01fd")
        buf.write("\3\2\2\2\u01ff\u0200\3\2\2\2\u0200\u0203\3\2\2\2\u0201")
        buf.write("\u01ff\3\2\2\2\u0202\u01fa\3\2\2\2\u0202\u0203\3\2\2\2")
        buf.write("\u0203\u0204\3\2\2\2\u0204\u0207\7\5\2\2\u0205\u0206\t")
        buf.write("\4\2\2\u0206\u0208\7Q\2\2\u0207\u0205\3\2\2\2\u0207\u0208")
        buf.write("\3\2\2\2\u0208\u0218\3\2\2\2\u0209\u020a\7p\2\2\u020a")
        buf.write("\u020b\78\2\2\u020b\u020c\7\3\2\2\u020c\u020d\7T\2\2\u020d")
        buf.write("\u020e\7 \2\2\u020e\u0213\5@!\2\u020f\u0210\7\4\2\2\u0210")
        buf.write("\u0212\5@!\2\u0211\u020f\3\2\2\2\u0212\u0215\3\2\2\2\u0213")
        buf.write("\u0211\3\2\2\2\u0213\u0214\3\2\2\2\u0214\u0216\3\2\2\2")
        buf.write("\u0215\u0213\3\2\2\2\u0216\u0217\7\5\2\2\u0217\u0219\3")
        buf.write("\2\2\2\u0218\u0209\3\2\2\2\u0218\u0219\3\2\2\2\u0219\u021b")
        buf.write("\3\2\2\2\u021a\u021c\5:\36\2\u021b\u021a\3\2\2\2\u021b")
        buf.write("\u021c\3\2\2\2\u021c\u0265\3\2\2\2\u021d\u021e\5H%\2\u021e")
        buf.write("\u021f\7\3\2\2\u021f\u0224\5\64\33\2\u0220\u0221\7\4\2")
        buf.write("\2\u0221\u0223\5\64\33\2\u0222\u0220\3\2\2\2\u0223\u0226")
        buf.write("\3\2\2\2\u0224\u0222\3\2\2\2\u0224\u0225\3\2\2\2\u0225")
        buf.write("\u0227\3\2\2\2\u0226\u0224\3\2\2\2\u0227\u022a\7\5\2\2")
        buf.write("\u0228\u0229\t\4\2\2\u0229\u022b\7Q\2\2\u022a\u0228\3")
        buf.write("\2\2\2\u022a\u022b\3\2\2\2\u022b\u023b\3\2\2\2\u022c\u022d")
        buf.write("\7p\2\2\u022d\u022e\78\2\2\u022e\u022f\7\3\2\2\u022f\u0230")
        buf.write("\7T\2\2\u0230\u0231\7 \2\2\u0231\u0236\5@!\2\u0232\u0233")
        buf.write("\7\4\2\2\u0233\u0235\5@!\2\u0234\u0232\3\2\2\2\u0235\u0238")
        buf.write("\3\2\2\2\u0236\u0234\3\2\2\2\u0236\u0237\3\2\2\2\u0237")
        buf.write("\u0239\3\2\2\2\u0238\u0236\3\2\2\2\u0239\u023a\7\5\2\2")
        buf.write("\u023a\u023c\3\2\2\2\u023b\u022c\3\2\2\2\u023b\u023c\3")
        buf.write("\2\2\2\u023c\u023e\3\2\2\2\u023d\u023f\5:\36\2\u023e\u023d")
        buf.write("\3\2\2\2\u023e\u023f\3\2\2\2\u023f\u0265\3\2\2\2\u0240")
        buf.write("\u0241\5H%\2\u0241\u0243\7\3\2\2\u0242\u0244\5`\61\2\u0243")
        buf.write("\u0242\3\2\2\2\u0243\u0244\3\2\2\2\u0244\u0245\3\2\2\2")
        buf.write("\u0245\u0246\5\"\22\2\u0246\u0247\t\4\2\2\u0247\u0248")
        buf.write("\7Q\2\2\u0248\u0258\7\5\2\2\u0249\u024a\7p\2\2\u024a\u024b")
        buf.write("\78\2\2\u024b\u024c\7\3\2\2\u024c\u024d\7T\2\2\u024d\u024e")
        buf.write("\7 \2\2\u024e\u0253\5@!\2\u024f\u0250\7\4\2\2\u0250\u0252")
        buf.write("\5@!\2\u0251\u024f\3\2\2\2\u0252\u0255\3\2\2\2\u0253\u0251")
        buf.write("\3\2\2\2\u0253\u0254\3\2\2\2\u0254\u0256\3\2\2\2\u0255")
        buf.write("\u0253\3\2\2\2\u0256\u0257\7\5\2\2\u0257\u0259\3\2\2\2")
        buf.write("\u0258\u0249\3\2\2\2\u0258\u0259\3\2\2\2\u0259\u025b\3")
        buf.write("\2\2\2\u025a\u025c\5:\36\2\u025b\u025a\3\2\2\2\u025b\u025c")
        buf.write("\3\2\2\2\u025c\u0265\3\2\2\2\u025d\u025e\5H%\2\u025e\u025f")
        buf.write("\7\3\2\2\u025f\u0260\7\6\2\2\u0260\u0262\7\5\2\2\u0261")
        buf.write("\u0263\5:\36\2\u0262\u0261\3\2\2\2\u0262\u0263\3\2\2\2")
        buf.write("\u0263\u0265\3\2\2\2\u0264\u01f5\3\2\2\2\u0264\u021d\3")
        buf.write("\2\2\2\u0264\u0240\3\2\2\2\u0264\u025d\3\2\2\2\u0265\63")
        buf.write("\3\2\2\2\u0266\u0267\5L\'\2\u0267\u0268\7\f\2\2\u0268")
        buf.write("\u0269\5\"\22\2\u0269\65\3\2\2\2\u026a\u026b\7m\2\2\u026b")
        buf.write("\u026c\5\"\22\2\u026c\u026d\7f\2\2\u026d\u026e\5\"\22")
        buf.write("\2\u026e\67\3\2\2\2\u026f\u0270\t\5\2\2\u02709\3\2\2\2")
        buf.write("\u0271\u0272\7V\2\2\u0272\u027d\7\3\2\2\u0273\u0274\7")
        buf.write("W\2\2\u0274\u0275\7 \2\2\u0275\u027a\5\"\22\2\u0276\u0277")
        buf.write("\7\4\2\2\u0277\u0279\5\"\22\2\u0278\u0276\3\2\2\2\u0279")
        buf.write("\u027c\3\2\2\2\u027a\u0278\3\2\2\2\u027a\u027b\3\2\2\2")
        buf.write("\u027b\u027e\3\2\2\2\u027c\u027a\3\2\2\2\u027d\u0273\3")
        buf.write("\2\2\2\u027d\u027e\3\2\2\2\u027e\u0289\3\2\2\2\u027f\u0280")
        buf.write("\7T\2\2\u0280\u0281\7 \2\2\u0281\u0286\5@!\2\u0282\u0283")
        buf.write("\7\4\2\2\u0283\u0285\5@!\2\u0284\u0282\3\2\2\2\u0285\u0288")
        buf.write("\3\2\2\2\u0286\u0284\3\2\2\2\u0286\u0287\3\2\2\2\u0287")
        buf.write("\u028a\3\2\2\2\u0288\u0286\3\2\2\2\u0289\u027f\3\2\2\2")
        buf.write("\u0289\u028a\3\2\2\2\u028a\u028c\3\2\2\2\u028b\u028d\5")
        buf.write("> \2\u028c\u028b\3\2\2\2\u028c\u028d\3\2\2\2\u028d\u028e")
        buf.write("\3\2\2\2\u028e\u028f\7\5\2\2\u028f;\3\2\2\2\u0290\u0291")
        buf.write("\7s\2\2\u0291\u0297\t\6\2\2\u0292\u0293\7i\2\2\u0293\u0297")
        buf.write("\t\6\2\2\u0294\u0295\7%\2\2\u0295\u0297\7`\2\2\u0296\u0290")
        buf.write("\3\2\2\2\u0296\u0292\3\2\2\2\u0296\u0294\3\2\2\2\u0297")
        buf.write("=\3\2\2\2\u0298\u0299\t\7\2\2\u0299\u02a1\5<\37\2\u029a")
        buf.write("\u029b\t\7\2\2\u029b\u029c\7\37\2\2\u029c\u029d\5<\37")
        buf.write("\2\u029d\u029e\7\33\2\2\u029e\u029f\5<\37\2\u029f\u02a1")
        buf.write("\3\2\2\2\u02a0\u0298\3\2\2\2\u02a0\u029a\3\2\2\2\u02a1")
        buf.write("?\3\2\2\2\u02a2\u02a4\5\"\22\2\u02a3\u02a5\t\b\2\2\u02a4")
        buf.write("\u02a3\3\2\2\2\u02a4\u02a5\3\2\2\2\u02a5\u02a8\3\2\2\2")
        buf.write("\u02a6\u02a7\7Q\2\2\u02a7\u02a9\t\t\2\2\u02a8\u02a6\3")
        buf.write("\2\2\2\u02a8\u02a9\3\2\2\2\u02a9A\3\2\2\2\u02aa\u02ab")
        buf.write("\b\"\1\2\u02ab\u02ac\7G\2\2\u02ac\u02b9\5B\"\t\u02ad\u02b9")
        buf.write("\5\62\32\2\u02ae\u02af\7\3\2\2\u02af\u02b0\5\16\b\2\u02b0")
        buf.write("\u02b1\7\5\2\2\u02b1\u02b9\3\2\2\2\u02b2\u02b3\7\3\2\2")
        buf.write("\u02b3\u02b4\5B\"\2\u02b4\u02b5\7\5\2\2\u02b5\u02b9\3")
        buf.write("\2\2\2\u02b6\u02b9\7x\2\2\u02b7\u02b9\5H%\2\u02b8\u02aa")
        buf.write("\3\2\2\2\u02b8\u02ad\3\2\2\2\u02b8\u02ae\3\2\2\2\u02b8")
        buf.write("\u02b2\3\2\2\2\u02b8\u02b6\3\2\2\2\u02b8\u02b7\3\2\2\2")
        buf.write("\u02b9\u02fe\3\2\2\2\u02ba\u02bc\f\f\2\2\u02bb\u02bd\5")
        buf.write("b\62\2\u02bc\u02bb\3\2\2\2\u02bc\u02bd\3\2\2\2\u02bd\u02be")
        buf.write("\3\2\2\2\u02be\u02bf\7E\2\2\u02bf\u02c2\5B\"\2\u02c0\u02c1")
        buf.write("\7R\2\2\u02c1\u02c3\5$\23\2\u02c2\u02c0\3\2\2\2\u02c2")
        buf.write("\u02c3\3\2\2\2\u02c3\u02c9\3\2\2\2\u02c4\u02c5\7l\2\2")
        buf.write("\u02c5\u02c6\7\3\2\2\u02c6\u02c7\5J&\2\u02c7\u02c8\7\5")
        buf.write("\2\2\u02c8\u02ca\3\2\2\2\u02c9\u02c4\3\2\2\2\u02c9\u02ca")
        buf.write("\3\2\2\2\u02ca\u02fd\3\2\2\2\u02cb\u02cc\f\13\2\2\u02cc")
        buf.write("\u02cd\7X\2\2\u02cd\u02ce\7\3\2\2\u02ce\u02cf\5H%\2\u02cf")
        buf.write("\u02d0\7\3\2\2\u02d0\u02d1\5L\'\2\u02d1\u02d2\7\5\2\2")
        buf.write("\u02d2\u02d3\7\64\2\2\u02d3\u02d4\5L\'\2\u02d4\u02d5\7")
        buf.write(">\2\2\u02d5\u02de\7\3\2\2\u02d6\u02db\5\"\22\2\u02d7\u02d8")
        buf.write("\7\4\2\2\u02d8\u02da\5\"\22\2\u02d9\u02d7\3\2\2\2\u02da")
        buf.write("\u02dd\3\2\2\2\u02db\u02d9\3\2\2\2\u02db\u02dc\3\2\2\2")
        buf.write("\u02dc\u02df\3\2\2\2\u02dd\u02db\3\2\2\2\u02de\u02d6\3")
        buf.write("\2\2\2\u02de\u02df\3\2\2\2\u02df\u02e0\3\2\2\2\u02e0\u02e1")
        buf.write("\7\5\2\2\u02e1\u02e2\7\5\2\2\u02e2\u02fd\3\2\2\2\u02e3")
        buf.write("\u02e4\f\n\2\2\u02e4\u02e5\7k\2\2\u02e5\u02e6\7\3\2\2")
        buf.write("\u02e6\u02e7\5L\'\2\u02e7\u02e8\7\64\2\2\u02e8\u02e9\5")
        buf.write("L\'\2\u02e9\u02ea\7>\2\2\u02ea\u02ec\7\3\2\2\u02eb\u02ed")
        buf.write("\5J&\2\u02ec\u02eb\3\2\2\2\u02ec\u02ed\3\2\2\2\u02ed\u02ee")
        buf.write("\3\2\2\2\u02ee\u02ef\7\5\2\2\u02ef\u02f0\7\5\2\2\u02f0")
        buf.write("\u02fd\3\2\2\2\u02f1\u02f3\f\4\2\2\u02f2\u02f4\7\35\2")
        buf.write("\2\u02f3\u02f2\3\2\2\2\u02f3\u02f4\3\2\2\2\u02f4\u02f5")
        buf.write("\3\2\2\2\u02f5\u02fa\5L\'\2\u02f6\u02f7\7\3\2\2\u02f7")
        buf.write("\u02f8\5J&\2\u02f8\u02f9\7\5\2\2\u02f9\u02fb\3\2\2\2\u02fa")
        buf.write("\u02f6\3\2\2\2\u02fa\u02fb\3\2\2\2\u02fb\u02fd\3\2\2\2")
        buf.write("\u02fc\u02ba\3\2\2\2\u02fc\u02cb\3\2\2\2\u02fc\u02e3\3")
        buf.write("\2\2\2\u02fc\u02f1\3\2\2\2\u02fd\u0300\3\2\2\2\u02fe\u02fc")
        buf.write("\3\2\2\2\u02fe\u02ff\3\2\2\2\u02ffC\3\2\2\2\u0300\u02fe")
        buf.write("\3\2\2\2\u0301\u0306\5\"\22\2\u0302\u0303\7\4\2\2\u0303")
        buf.write("\u0305\5\"\22\2\u0304\u0302\3\2\2\2\u0305\u0308\3\2\2")
        buf.write("\2\u0306\u0304\3\2\2\2\u0306\u0307\3\2\2\2\u0307\u0317")
        buf.write("\3\2\2\2\u0308\u0306\3\2\2\2\u0309\u030a\79\2\2\u030a")
        buf.write("\u030b\7d\2\2\u030b\u030c\7\3\2\2\u030c\u0311\5F$\2\u030d")
        buf.write("\u030e\7\4\2\2\u030e\u0310\5F$\2\u030f\u030d\3\2\2\2\u0310")
        buf.write("\u0313\3\2\2\2\u0311\u030f\3\2\2\2\u0311\u0312\3\2\2\2")
        buf.write("\u0312\u0314\3\2\2\2\u0313\u0311\3\2\2\2\u0314\u0315\7")
        buf.write("\5\2\2\u0315\u0317\3\2\2\2\u0316\u0301\3\2\2\2\u0316\u0309")
        buf.write("\3\2\2\2\u0317E\3\2\2\2\u0318\u0319\7\3\2\2\u0319\u031e")
        buf.write("\5\"\22\2\u031a\u031b\7\4\2\2\u031b\u031d\5\"\22\2\u031c")
        buf.write("\u031a\3\2\2\2\u031d\u0320\3\2\2\2\u031e\u031c\3\2\2\2")
        buf.write("\u031e\u031f\3\2\2\2\u031f\u0321\3\2\2\2\u0320\u031e\3")
        buf.write("\2\2\2\u0321\u0322\7\5\2\2\u0322G\3\2\2\2\u0323\u0328")
        buf.write("\5L\'\2\u0324\u0325\7\7\2\2\u0325\u0327\5L\'\2\u0326\u0324")
        buf.write("\3\2\2\2\u0327\u032a\3\2\2\2\u0328\u0326\3\2\2\2\u0328")
        buf.write("\u0329\3\2\2\2\u0329I\3\2\2\2\u032a\u0328\3\2\2\2\u032b")
        buf.write("\u0330\5L\'\2\u032c\u032d\7\4\2\2\u032d\u032f\5L\'\2\u032e")
        buf.write("\u032c\3\2\2\2\u032f\u0332\3\2\2\2\u0330\u032e\3\2\2\2")
        buf.write("\u0330\u0331\3\2\2\2\u0331K\3\2\2\2\u0332\u0330\3\2\2")
        buf.write("\2\u0333\u0336\5j\66\2\u0334\u0336\5N(\2\u0335\u0333\3")
        buf.write("\2\2\2\u0335\u0334\3\2\2\2\u0336M\3\2\2\2\u0337\u0338")
        buf.write("\7w\2\2\u0338O\3\2\2\2\u0339\u033a\7\r\2\2\u033a\u033b")
        buf.write("\7v\2\2\u033bQ\3\2\2\2\u033c\u033d\7\b\2\2\u033d\u033e")
        buf.write("\7v\2\2\u033eS\3\2\2\2\u033f\u0343\5V,\2\u0340\u0343\7")
        buf.write("t\2\2\u0341\u0343\7u\2\2\u0342\u033f\3\2\2\2\u0342\u0340")
        buf.write("\3\2\2\2\u0342\u0341\3\2\2\2\u0343U\3\2\2\2\u0344\u0345")
        buf.write("\7s\2\2\u0345W\3\2\2\2\u0346\u0347\7r\2\2\u0347Y\3\2\2")
        buf.write("\2\u0348\u0349\7P\2\2\u0349[\3\2\2\2\u034a\u034b\7h\2")
        buf.write("\2\u034b]\3\2\2\2\u034c\u034d\7\61\2\2\u034d_\3\2\2\2")
        buf.write("\u034e\u034f\t\n\2\2\u034fa\3\2\2\2\u0350\u035d\7?\2\2")
        buf.write("\u0351\u035d\7H\2\2\u0352\u0353\7H\2\2\u0353\u035d\7U")
        buf.write("\2\2\u0354\u035d\7^\2\2\u0355\u0356\7^\2\2\u0356\u035d")
        buf.write("\7U\2\2\u0357\u035d\7\66\2\2\u0358\u0359\7\66\2\2\u0359")
        buf.write("\u035d\7U\2\2\u035a\u035d\7$\2\2\u035b\u035d\7N\2\2\u035c")
        buf.write("\u0350\3\2\2\2\u035c\u0351\3\2\2\2\u035c\u0352\3\2\2\2")
        buf.write("\u035c\u0354\3\2\2\2\u035c\u0355\3\2\2\2\u035c\u0357\3")
        buf.write("\2\2\2\u035c\u0358\3\2\2\2\u035c\u035a\3\2\2\2\u035c\u035b")
        buf.write("\3\2\2\2\u035dc\3\2\2\2\u035e\u035f\t\13\2\2\u035fe\3")
        buf.write("\2\2\2\u0360\u0361\t\f\2\2\u0361g\3\2\2\2\u0362\u0363")
        buf.write("\t\r\2\2\u0363i\3\2\2\2\u0364\u0365\t\16\2\2\u0365k\3")
        buf.write("\2\2\2msx\u0082\u0087\u008b\u008f\u009b\u00a5\u00a8\u00b6")
        buf.write("\u00bb\u00c4\u00c6\u00cd\u00d1\u00d4\u00db\u00e4\u00e7")
        buf.write("\u00eb\u00f0\u00f4\u00f8\u0101\u0104\u0108\u0114\u0117")
        buf.write("\u0119\u0120\u0124\u012b\u0133\u0137\u013f\u0148\u014e")
        buf.write("\u0156\u015b\u015f\u0168\u016d\u0171\u0173\u017a\u0184")
        buf.write("\u018a\u0192\u0194\u019a\u019c\u01a2\u01a7\u01ac\u01b1")
        buf.write("\u01da\u01e4\u01ed\u01f0\u01f3\u01f8\u01ff\u0202\u0207")
        buf.write("\u0213\u0218\u021b\u0224\u022a\u0236\u023b\u023e\u0243")
        buf.write("\u0253\u0258\u025b\u0262\u0264\u027a\u027d\u0286\u0289")
        buf.write("\u028c\u0296\u02a0\u02a4\u02a8\u02b8\u02bc\u02c2\u02c9")
        buf.write("\u02db\u02de\u02ec\u02f3\u02fa\u02fc\u02fe\u0306\u0311")
        buf.write("\u0316\u031e\u0328\u0330\u0335\u0342\u035c")
        return buf.getvalue()


class IceSqlParser ( Parser ):

    grammarFileName = "IceSql.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "','", "')'", "'*'", "'.'", "':'", 
                     "'['", "']'", "'::'", "'=>'", "'$'", "'='", "'!='", 
                     "'<>'", "'<'", "'<='", "'>'", "'>='", "'+'", "'-'", 
                     "'/'", "'%'", "'||'", "'all'", "'and'", "'any'", "'as'", 
                     "'asc'", "'between'", "'by'", "'case'", "'cast'", "'create'", 
                     "'cross'", "'current'", "'date'", "'day'", "'delete'", 
                     "'desc'", "'distinct'", "'drop'", "'else'", "'end'", 
                     "'escape'", "'except'", "'extract'", "'false'", "'first'", 
                     "'following'", "'for'", "'from'", "'full'", "'function'", 
                     "'group'", "'grouping'", "'having'", "'hour'", "'ignore'", 
                     "'ilike'", "'in'", "'inner'", "'insert'", "'intersect'", 
                     "'interval'", "'into'", "'is'", "'join'", "'last'", 
                     "'lateral'", "'left'", "'like'", "'limit'", "'minus'", 
                     "'minute'", "'month'", "'natural'", "'not'", "'null'", 
                     "'nulls'", "'on'", "'or'", "'order'", "'outer'", "'over'", 
                     "'partition'", "'pivot'", "'preceding'", "'qualify'", 
                     "'range'", "'replace'", "'respect'", "'right'", "'rlike'", 
                     "'row'", "'rows'", "'second'", "'select'", "'sets'", 
                     "'table'", "'then'", "'top'", "'true'", "'unbounded'", 
                     "'union'", "'unpivot'", "'using'", "'when'", "'where'", 
                     "'with'", "'within'", "'year'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "ALL", "AND", "ANY", "AS", "ASC", "BETWEEN", "BY", 
                      "CASE", "CAST", "CREATE", "CROSS", "CURRENT", "DATE", 
                      "DAY", "DELETE", "DESC", "DISTINCT", "DROP", "ELSE", 
                      "END", "ESCAPE", "EXCEPT", "EXTRACT", "FALSE", "FIRST", 
                      "FOLLOWING", "FOR", "FROM", "FULL", "FUNCTION", "GROUP", 
                      "GROUPING", "HAVING", "HOUR", "IGNORE", "ILIKE", "IN", 
                      "INNER", "INSERT", "INTERSECT", "INTERVAL", "INTO", 
                      "IS", "JOIN", "LAST", "LATERAL", "LEFT", "LIKE", "LIMIT", 
                      "MINUS", "MINUTE", "MONTH", "NATURAL", "NOT", "NULL", 
                      "NULLS", "ON", "OR", "ORDER", "OUTER", "OVER", "PARTITION", 
                      "PIVOT", "PRECEDING", "QUALIFY", "RANGE", "REPLACE", 
                      "RESPECT", "RIGHT", "RLIKE", "ROW", "ROWS", "SECOND", 
                      "SELECT", "SETS", "TABLE", "THEN", "TOP", "TRUE", 
                      "UNBOUNDED", "UNION", "UNPIVOT", "USING", "WHEN", 
                      "WHERE", "WITH", "WITHIN", "YEAR", "STRING", "INTEGER_VALUE", 
                      "DECIMAL_VALUE", "FLOAT_VALUE", "IDENTIFIER", "QUOTED_IDENTIFIER", 
                      "JINJA", "COMMENT", "BLOCK_COMMENT", "JINJA_STATEMENT", 
                      "JINJA_COMMENT", "WS", "DELIMITER" ]

    RULE_singleStatement = 0
    RULE_statement = 1
    RULE_createTable = 2
    RULE_colSpec = 3
    RULE_insert = 4
    RULE_delete = 5
    RULE_select = 6
    RULE_cteSelect = 7
    RULE_cte = 8
    RULE_setSelect = 9
    RULE_setSelectItem = 10
    RULE_setSelectKind = 11
    RULE_parenSelect = 12
    RULE_primarySelect = 13
    RULE_topN = 14
    RULE_selectItem = 15
    RULE_expression = 16
    RULE_booleanExpression = 17
    RULE_predicate = 18
    RULE_valueExpression = 19
    RULE_traversalKey = 20
    RULE_primaryExpression = 21
    RULE_simpleExpression = 22
    RULE_typeSpec = 23
    RULE_functionCall = 24
    RULE_kwarg = 25
    RULE_caseItem = 26
    RULE_intervalUnit = 27
    RULE_over = 28
    RULE_frameBound = 29
    RULE_frame = 30
    RULE_sortItem = 31
    RULE_relation = 32
    RULE_grouping = 33
    RULE_groupingSet = 34
    RULE_qualifiedName = 35
    RULE_identifierList = 36
    RULE_identifier = 37
    RULE_quotedIdentifier = 38
    RULE_var = 39
    RULE_param = 40
    RULE_number = 41
    RULE_integer = 42
    RULE_string = 43
    RULE_null = 44
    RULE_true = 45
    RULE_false = 46
    RULE_setQuantifier = 47
    RULE_joinType = 48
    RULE_cmpOp = 49
    RULE_arithOp = 50
    RULE_unaryOp = 51
    RULE_unquotedIdentifier = 52

    ruleNames =  [ "singleStatement", "statement", "createTable", "colSpec", 
                   "insert", "delete", "select", "cteSelect", "cte", "setSelect", 
                   "setSelectItem", "setSelectKind", "parenSelect", "primarySelect", 
                   "topN", "selectItem", "expression", "booleanExpression", 
                   "predicate", "valueExpression", "traversalKey", "primaryExpression", 
                   "simpleExpression", "typeSpec", "functionCall", "kwarg", 
                   "caseItem", "intervalUnit", "over", "frameBound", "frame", 
                   "sortItem", "relation", "grouping", "groupingSet", "qualifiedName", 
                   "identifierList", "identifier", "quotedIdentifier", "var", 
                   "param", "number", "integer", "string", "null", "true", 
                   "false", "setQuantifier", "joinType", "cmpOp", "arithOp", 
                   "unaryOp", "unquotedIdentifier" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    ALL=24
    AND=25
    ANY=26
    AS=27
    ASC=28
    BETWEEN=29
    BY=30
    CASE=31
    CAST=32
    CREATE=33
    CROSS=34
    CURRENT=35
    DATE=36
    DAY=37
    DELETE=38
    DESC=39
    DISTINCT=40
    DROP=41
    ELSE=42
    END=43
    ESCAPE=44
    EXCEPT=45
    EXTRACT=46
    FALSE=47
    FIRST=48
    FOLLOWING=49
    FOR=50
    FROM=51
    FULL=52
    FUNCTION=53
    GROUP=54
    GROUPING=55
    HAVING=56
    HOUR=57
    IGNORE=58
    ILIKE=59
    IN=60
    INNER=61
    INSERT=62
    INTERSECT=63
    INTERVAL=64
    INTO=65
    IS=66
    JOIN=67
    LAST=68
    LATERAL=69
    LEFT=70
    LIKE=71
    LIMIT=72
    MINUS=73
    MINUTE=74
    MONTH=75
    NATURAL=76
    NOT=77
    NULL=78
    NULLS=79
    ON=80
    OR=81
    ORDER=82
    OUTER=83
    OVER=84
    PARTITION=85
    PIVOT=86
    PRECEDING=87
    QUALIFY=88
    RANGE=89
    REPLACE=90
    RESPECT=91
    RIGHT=92
    RLIKE=93
    ROW=94
    ROWS=95
    SECOND=96
    SELECT=97
    SETS=98
    TABLE=99
    THEN=100
    TOP=101
    TRUE=102
    UNBOUNDED=103
    UNION=104
    UNPIVOT=105
    USING=106
    WHEN=107
    WHERE=108
    WITH=109
    WITHIN=110
    YEAR=111
    STRING=112
    INTEGER_VALUE=113
    DECIMAL_VALUE=114
    FLOAT_VALUE=115
    IDENTIFIER=116
    QUOTED_IDENTIFIER=117
    JINJA=118
    COMMENT=119
    BLOCK_COMMENT=120
    JINJA_STATEMENT=121
    JINJA_COMMENT=122
    WS=123
    DELIMITER=124

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    _config = None

    @property
    def config(self):
        return self._config or DEFAULT_ICE_SQL_PARSER_CONFIG

    @config.setter
    def config(self, config):
        if self._config is not None or not isinstance(config, IceSqlParserConfig):
            raise TypeError
        self._config = config



    class SingleStatementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self):
            return self.getTypedRuleContext(IceSqlParser.StatementContext,0)


        def EOF(self):
            return self.getToken(IceSqlParser.EOF, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_singleStatement

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

        localctx = IceSqlParser.SingleStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_singleStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 106
            self.statement()
            self.state = 107
            self.match(IceSqlParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def select(self):
            return self.getTypedRuleContext(IceSqlParser.SelectContext,0)


        def createTable(self):
            return self.getTypedRuleContext(IceSqlParser.CreateTableContext,0)


        def insert(self):
            return self.getTypedRuleContext(IceSqlParser.InsertContext,0)


        def delete(self):
            return self.getTypedRuleContext(IceSqlParser.DeleteContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = IceSqlParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 113
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [IceSqlParser.T__0, IceSqlParser.SELECT, IceSqlParser.WITH]:
                self.enterOuterAlt(localctx, 1)
                self.state = 109
                self.select()
                pass
            elif token in [IceSqlParser.CREATE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 110
                self.createTable()
                pass
            elif token in [IceSqlParser.INSERT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 111
                self.insert()
                pass
            elif token in [IceSqlParser.DELETE]:
                self.enterOuterAlt(localctx, 4)
                self.state = 112
                self.delete()
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


    class CreateTableContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CREATE(self):
            return self.getToken(IceSqlParser.CREATE, 0)

        def TABLE(self):
            return self.getToken(IceSqlParser.TABLE, 0)

        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)


        def OR(self):
            return self.getToken(IceSqlParser.OR, 0)

        def REPLACE(self):
            return self.getToken(IceSqlParser.REPLACE, 0)

        def colSpec(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ColSpecContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ColSpecContext,i)


        def AS(self):
            return self.getToken(IceSqlParser.AS, 0)

        def select(self):
            return self.getTypedRuleContext(IceSqlParser.SelectContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_createTable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCreateTable" ):
                listener.enterCreateTable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCreateTable" ):
                listener.exitCreateTable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCreateTable" ):
                return visitor.visitCreateTable(self)
            else:
                return visitor.visitChildren(self)




    def createTable(self):

        localctx = IceSqlParser.CreateTableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_createTable)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(IceSqlParser.CREATE)
            self.state = 118
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.OR:
                self.state = 116
                self.match(IceSqlParser.OR)
                self.state = 117
                self.match(IceSqlParser.REPLACE)


            self.state = 120
            self.match(IceSqlParser.TABLE)
            self.state = 121
            self.qualifiedName()
            self.state = 133
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.T__0:
                self.state = 122
                self.match(IceSqlParser.T__0)
                self.state = 123
                self.colSpec()
                self.state = 128
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 124
                    self.match(IceSqlParser.T__1)
                    self.state = 125
                    self.colSpec()
                    self.state = 130
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 131
                self.match(IceSqlParser.T__2)


            self.state = 137
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.AS:
                self.state = 135
                self.match(IceSqlParser.AS)
                self.state = 136
                self.select()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ColSpecContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierContext,0)


        def typeSpec(self):
            return self.getTypedRuleContext(IceSqlParser.TypeSpecContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_colSpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterColSpec" ):
                listener.enterColSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitColSpec" ):
                listener.exitColSpec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitColSpec" ):
                return visitor.visitColSpec(self)
            else:
                return visitor.visitChildren(self)




    def colSpec(self):

        localctx = IceSqlParser.ColSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_colSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            self.identifier()
            self.state = 141
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << IceSqlParser.CASE) | (1 << IceSqlParser.DATE) | (1 << IceSqlParser.DAY) | (1 << IceSqlParser.EXTRACT) | (1 << IceSqlParser.FIRST) | (1 << IceSqlParser.GROUPING) | (1 << IceSqlParser.HOUR) | (1 << IceSqlParser.ILIKE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (IceSqlParser.LAST - 68)) | (1 << (IceSqlParser.LEFT - 68)) | (1 << (IceSqlParser.LIKE - 68)) | (1 << (IceSqlParser.MINUTE - 68)) | (1 << (IceSqlParser.MONTH - 68)) | (1 << (IceSqlParser.OUTER - 68)) | (1 << (IceSqlParser.RANGE - 68)) | (1 << (IceSqlParser.REPLACE - 68)) | (1 << (IceSqlParser.RIGHT - 68)) | (1 << (IceSqlParser.RLIKE - 68)) | (1 << (IceSqlParser.SECOND - 68)) | (1 << (IceSqlParser.YEAR - 68)) | (1 << (IceSqlParser.IDENTIFIER - 68)) | (1 << (IceSqlParser.QUOTED_IDENTIFIER - 68)))) != 0):
                self.state = 140
                self.typeSpec()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InsertContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INSERT(self):
            return self.getToken(IceSqlParser.INSERT, 0)

        def INTO(self):
            return self.getToken(IceSqlParser.INTO, 0)

        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)


        def select(self):
            return self.getTypedRuleContext(IceSqlParser.SelectContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_insert

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInsert" ):
                listener.enterInsert(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInsert" ):
                listener.exitInsert(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInsert" ):
                return visitor.visitInsert(self)
            else:
                return visitor.visitChildren(self)




    def insert(self):

        localctx = IceSqlParser.InsertContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_insert)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            self.match(IceSqlParser.INSERT)
            self.state = 144
            self.match(IceSqlParser.INTO)
            self.state = 145
            self.qualifiedName()
            self.state = 146
            self.select()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeleteContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.where = None # BooleanExpressionContext

        def DELETE(self):
            return self.getToken(IceSqlParser.DELETE, 0)

        def FROM(self):
            return self.getToken(IceSqlParser.FROM, 0)

        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)


        def WHERE(self):
            return self.getToken(IceSqlParser.WHERE, 0)

        def booleanExpression(self):
            return self.getTypedRuleContext(IceSqlParser.BooleanExpressionContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_delete

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDelete" ):
                listener.enterDelete(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDelete" ):
                listener.exitDelete(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDelete" ):
                return visitor.visitDelete(self)
            else:
                return visitor.visitChildren(self)




    def delete(self):

        localctx = IceSqlParser.DeleteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_delete)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self.match(IceSqlParser.DELETE)
            self.state = 149
            self.match(IceSqlParser.FROM)
            self.state = 150
            self.qualifiedName()
            self.state = 153
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.WHERE:
                self.state = 151
                self.match(IceSqlParser.WHERE)
                self.state = 152
                localctx.where = self.booleanExpression(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def cteSelect(self):
            return self.getTypedRuleContext(IceSqlParser.CteSelectContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_select

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelect" ):
                listener.enterSelect(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelect" ):
                listener.exitSelect(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelect" ):
                return visitor.visitSelect(self)
            else:
                return visitor.visitChildren(self)




    def select(self):

        localctx = IceSqlParser.SelectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_select)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 155
            self.cteSelect()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CteSelectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def setSelect(self):
            return self.getTypedRuleContext(IceSqlParser.SetSelectContext,0)


        def WITH(self):
            return self.getToken(IceSqlParser.WITH, 0)

        def cte(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.CteContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.CteContext,i)


        def getRuleIndex(self):
            return IceSqlParser.RULE_cteSelect

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCteSelect" ):
                listener.enterCteSelect(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCteSelect" ):
                listener.exitCteSelect(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCteSelect" ):
                return visitor.visitCteSelect(self)
            else:
                return visitor.visitChildren(self)




    def cteSelect(self):

        localctx = IceSqlParser.CteSelectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_cteSelect)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 166
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.WITH:
                self.state = 157
                self.match(IceSqlParser.WITH)
                self.state = 158
                self.cte()
                self.state = 163
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 159
                    self.match(IceSqlParser.T__1)
                    self.state = 160
                    self.cte()
                    self.state = 165
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 168
            self.setSelect()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CteContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierContext,0)


        def AS(self):
            return self.getToken(IceSqlParser.AS, 0)

        def select(self):
            return self.getTypedRuleContext(IceSqlParser.SelectContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_cte

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCte" ):
                listener.enterCte(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCte" ):
                listener.exitCte(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCte" ):
                return visitor.visitCte(self)
            else:
                return visitor.visitChildren(self)




    def cte(self):

        localctx = IceSqlParser.CteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_cte)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            self.identifier()
            self.state = 171
            self.match(IceSqlParser.AS)
            self.state = 172
            self.match(IceSqlParser.T__0)
            self.state = 173
            self.select()
            self.state = 174
            self.match(IceSqlParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetSelectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parenSelect(self):
            return self.getTypedRuleContext(IceSqlParser.ParenSelectContext,0)


        def setSelectItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.SetSelectItemContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.SetSelectItemContext,i)


        def getRuleIndex(self):
            return IceSqlParser.RULE_setSelect

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetSelect" ):
                listener.enterSetSelect(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetSelect" ):
                listener.exitSetSelect(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetSelect" ):
                return visitor.visitSetSelect(self)
            else:
                return visitor.visitChildren(self)




    def setSelect(self):

        localctx = IceSqlParser.SetSelectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_setSelect)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            self.parenSelect()
            self.state = 180
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 45)) & ~0x3f) == 0 and ((1 << (_la - 45)) & ((1 << (IceSqlParser.EXCEPT - 45)) | (1 << (IceSqlParser.INTERSECT - 45)) | (1 << (IceSqlParser.MINUS - 45)) | (1 << (IceSqlParser.UNION - 45)))) != 0):
                self.state = 177
                self.setSelectItem()
                self.state = 182
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetSelectItemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def setSelectKind(self):
            return self.getTypedRuleContext(IceSqlParser.SetSelectKindContext,0)


        def parenSelect(self):
            return self.getTypedRuleContext(IceSqlParser.ParenSelectContext,0)


        def setQuantifier(self):
            return self.getTypedRuleContext(IceSqlParser.SetQuantifierContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_setSelectItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetSelectItem" ):
                listener.enterSetSelectItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetSelectItem" ):
                listener.exitSetSelectItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetSelectItem" ):
                return visitor.visitSetSelectItem(self)
            else:
                return visitor.visitChildren(self)




    def setSelectItem(self):

        localctx = IceSqlParser.SetSelectItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_setSelectItem)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 183
            self.setSelectKind()
            self.state = 185
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.ALL or _la==IceSqlParser.DISTINCT:
                self.state = 184
                self.setQuantifier()


            self.state = 187
            self.parenSelect()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetSelectKindContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTERSECT(self):
            return self.getToken(IceSqlParser.INTERSECT, 0)

        def MINUS(self):
            return self.getToken(IceSqlParser.MINUS, 0)

        def EXCEPT(self):
            return self.getToken(IceSqlParser.EXCEPT, 0)

        def UNION(self):
            return self.getToken(IceSqlParser.UNION, 0)

        def ALL(self):
            return self.getToken(IceSqlParser.ALL, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_setSelectKind

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetSelectKind" ):
                listener.enterSetSelectKind(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetSelectKind" ):
                listener.exitSetSelectKind(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetSelectKind" ):
                return visitor.visitSetSelectKind(self)
            else:
                return visitor.visitChildren(self)




    def setSelectKind(self):

        localctx = IceSqlParser.SetSelectKindContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_setSelectKind)
        try:
            self.state = 196
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [IceSqlParser.INTERSECT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 189
                self.match(IceSqlParser.INTERSECT)
                pass
            elif token in [IceSqlParser.MINUS]:
                self.enterOuterAlt(localctx, 2)
                self.state = 190
                self.match(IceSqlParser.MINUS)
                pass
            elif token in [IceSqlParser.EXCEPT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 191
                self.match(IceSqlParser.EXCEPT)
                pass
            elif token in [IceSqlParser.UNION]:
                self.enterOuterAlt(localctx, 4)
                self.state = 192
                self.match(IceSqlParser.UNION)
                self.state = 194
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
                if la_ == 1:
                    self.state = 193
                    self.match(IceSqlParser.ALL)


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


    class ParenSelectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parenSelect(self):
            return self.getTypedRuleContext(IceSqlParser.ParenSelectContext,0)


        def primarySelect(self):
            return self.getTypedRuleContext(IceSqlParser.PrimarySelectContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_parenSelect

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenSelect" ):
                listener.enterParenSelect(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenSelect" ):
                listener.exitParenSelect(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenSelect" ):
                return visitor.visitParenSelect(self)
            else:
                return visitor.visitChildren(self)




    def parenSelect(self):

        localctx = IceSqlParser.ParenSelectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_parenSelect)
        try:
            self.state = 203
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [IceSqlParser.T__0]:
                self.enterOuterAlt(localctx, 1)
                self.state = 198
                self.match(IceSqlParser.T__0)
                self.state = 199
                self.parenSelect()
                self.state = 200
                self.match(IceSqlParser.T__2)
                pass
            elif token in [IceSqlParser.SELECT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 202
                self.primarySelect()
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


    class PrimarySelectContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.where = None # BooleanExpressionContext
            self.having = None # BooleanExpressionContext
            self.qualify = None # BooleanExpressionContext

        def SELECT(self):
            return self.getToken(IceSqlParser.SELECT, 0)

        def selectItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.SelectItemContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.SelectItemContext,i)


        def topN(self):
            return self.getTypedRuleContext(IceSqlParser.TopNContext,0)


        def setQuantifier(self):
            return self.getTypedRuleContext(IceSqlParser.SetQuantifierContext,0)


        def FROM(self):
            return self.getToken(IceSqlParser.FROM, 0)

        def relation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.RelationContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.RelationContext,i)


        def WHERE(self):
            return self.getToken(IceSqlParser.WHERE, 0)

        def GROUP(self):
            return self.getToken(IceSqlParser.GROUP, 0)

        def BY(self, i:int=None):
            if i is None:
                return self.getTokens(IceSqlParser.BY)
            else:
                return self.getToken(IceSqlParser.BY, i)

        def grouping(self):
            return self.getTypedRuleContext(IceSqlParser.GroupingContext,0)


        def HAVING(self):
            return self.getToken(IceSqlParser.HAVING, 0)

        def QUALIFY(self):
            return self.getToken(IceSqlParser.QUALIFY, 0)

        def ORDER(self):
            return self.getToken(IceSqlParser.ORDER, 0)

        def sortItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.SortItemContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.SortItemContext,i)


        def LIMIT(self):
            return self.getToken(IceSqlParser.LIMIT, 0)

        def INTEGER_VALUE(self):
            return self.getToken(IceSqlParser.INTEGER_VALUE, 0)

        def booleanExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.BooleanExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.BooleanExpressionContext,i)


        def getRuleIndex(self):
            return IceSqlParser.RULE_primarySelect

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimarySelect" ):
                listener.enterPrimarySelect(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimarySelect" ):
                listener.exitPrimarySelect(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimarySelect" ):
                return visitor.visitPrimarySelect(self)
            else:
                return visitor.visitChildren(self)




    def primarySelect(self):

        localctx = IceSqlParser.PrimarySelectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_primarySelect)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 205
            self.match(IceSqlParser.SELECT)
            self.state = 207
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.state = 206
                self.topN()


            self.state = 210
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.state = 209
                self.setQuantifier()


            self.state = 212
            self.selectItem()
            self.state = 217
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==IceSqlParser.T__1:
                self.state = 213
                self.match(IceSqlParser.T__1)
                self.state = 214
                self.selectItem()
                self.state = 219
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 229
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.FROM:
                self.state = 220
                self.match(IceSqlParser.FROM)
                self.state = 221
                self.relation(0)
                self.state = 226
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 222
                    self.match(IceSqlParser.T__1)
                    self.state = 223
                    self.relation(0)
                    self.state = 228
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 233
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.WHERE:
                self.state = 231
                self.match(IceSqlParser.WHERE)
                self.state = 232
                localctx.where = self.booleanExpression(0)


            self.state = 238
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.GROUP:
                self.state = 235
                self.match(IceSqlParser.GROUP)
                self.state = 236
                self.match(IceSqlParser.BY)
                self.state = 237
                self.grouping()


            self.state = 242
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.HAVING:
                self.state = 240
                self.match(IceSqlParser.HAVING)
                self.state = 241
                localctx.having = self.booleanExpression(0)


            self.state = 246
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.QUALIFY:
                self.state = 244
                self.match(IceSqlParser.QUALIFY)
                self.state = 245
                localctx.qualify = self.booleanExpression(0)


            self.state = 258
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.ORDER:
                self.state = 248
                self.match(IceSqlParser.ORDER)
                self.state = 249
                self.match(IceSqlParser.BY)
                self.state = 250
                self.sortItem()
                self.state = 255
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 251
                    self.match(IceSqlParser.T__1)
                    self.state = 252
                    self.sortItem()
                    self.state = 257
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 262
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.LIMIT:
                self.state = 260
                self.match(IceSqlParser.LIMIT)
                self.state = 261
                self.match(IceSqlParser.INTEGER_VALUE)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TopNContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TOP(self):
            return self.getToken(IceSqlParser.TOP, 0)

        def number(self):
            return self.getTypedRuleContext(IceSqlParser.NumberContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_topN

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTopN" ):
                listener.enterTopN(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTopN" ):
                listener.exitTopN(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTopN" ):
                return visitor.visitTopN(self)
            else:
                return visitor.visitChildren(self)




    def topN(self):

        localctx = IceSqlParser.TopNContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_topN)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 264
            self.match(IceSqlParser.TOP)
            self.state = 265
            self.number()
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


        def getRuleIndex(self):
            return IceSqlParser.RULE_selectItem

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class IdentifierAllSelectItemContext(SelectItemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.SelectItemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def identifier(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifierAllSelectItem" ):
                listener.enterIdentifierAllSelectItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifierAllSelectItem" ):
                listener.exitIdentifierAllSelectItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifierAllSelectItem" ):
                return visitor.visitIdentifierAllSelectItem(self)
            else:
                return visitor.visitChildren(self)


    class ExpressionSelectItemContext(SelectItemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.SelectItemContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(IceSqlParser.ExpressionContext,0)

        def identifier(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierContext,0)

        def AS(self):
            return self.getToken(IceSqlParser.AS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpressionSelectItem" ):
                listener.enterExpressionSelectItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpressionSelectItem" ):
                listener.exitExpressionSelectItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionSelectItem" ):
                return visitor.visitExpressionSelectItem(self)
            else:
                return visitor.visitChildren(self)


    class AllSelectItemContext(SelectItemContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.SelectItemContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAllSelectItem" ):
                listener.enterAllSelectItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAllSelectItem" ):
                listener.exitAllSelectItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAllSelectItem" ):
                return visitor.visitAllSelectItem(self)
            else:
                return visitor.visitChildren(self)



    def selectItem(self):

        localctx = IceSqlParser.SelectItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_selectItem)
        self._la = 0 # Token type
        try:
            self.state = 279
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                localctx = IceSqlParser.AllSelectItemContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 267
                self.match(IceSqlParser.T__3)
                pass

            elif la_ == 2:
                localctx = IceSqlParser.IdentifierAllSelectItemContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 268
                self.identifier()
                self.state = 269
                self.match(IceSqlParser.T__4)
                self.state = 270
                self.match(IceSqlParser.T__3)
                pass

            elif la_ == 3:
                localctx = IceSqlParser.ExpressionSelectItemContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 272
                self.expression()
                self.state = 277
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << IceSqlParser.AS) | (1 << IceSqlParser.CASE) | (1 << IceSqlParser.DATE) | (1 << IceSqlParser.DAY) | (1 << IceSqlParser.EXTRACT) | (1 << IceSqlParser.FIRST) | (1 << IceSqlParser.GROUPING) | (1 << IceSqlParser.HOUR) | (1 << IceSqlParser.ILIKE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (IceSqlParser.LAST - 68)) | (1 << (IceSqlParser.LEFT - 68)) | (1 << (IceSqlParser.LIKE - 68)) | (1 << (IceSqlParser.MINUTE - 68)) | (1 << (IceSqlParser.MONTH - 68)) | (1 << (IceSqlParser.OUTER - 68)) | (1 << (IceSqlParser.RANGE - 68)) | (1 << (IceSqlParser.REPLACE - 68)) | (1 << (IceSqlParser.RIGHT - 68)) | (1 << (IceSqlParser.RLIKE - 68)) | (1 << (IceSqlParser.SECOND - 68)) | (1 << (IceSqlParser.YEAR - 68)) | (1 << (IceSqlParser.IDENTIFIER - 68)) | (1 << (IceSqlParser.QUOTED_IDENTIFIER - 68)))) != 0):
                    self.state = 274
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==IceSqlParser.AS:
                        self.state = 273
                        self.match(IceSqlParser.AS)


                    self.state = 276
                    self.identifier()


                pass


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
            return self.getTypedRuleContext(IceSqlParser.BooleanExpressionContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_expression

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

        localctx = IceSqlParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 281
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
            return IceSqlParser.RULE_booleanExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class BinaryBooleanExpressionContext(BooleanExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.BooleanExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def booleanExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.BooleanExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.BooleanExpressionContext,i)

        def AND(self):
            return self.getToken(IceSqlParser.AND, 0)
        def OR(self):
            return self.getToken(IceSqlParser.OR, 0)

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


    class PredicatedBooleanExpressionContext(BooleanExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.BooleanExpressionContext
            super().__init__(parser)
            self._valueExpression = None # ValueExpressionContext
            self.copyFrom(ctx)

        def valueExpression(self):
            return self.getTypedRuleContext(IceSqlParser.ValueExpressionContext,0)

        def predicate(self):
            return self.getTypedRuleContext(IceSqlParser.PredicateContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicatedBooleanExpression" ):
                listener.enterPredicatedBooleanExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicatedBooleanExpression" ):
                listener.exitPredicatedBooleanExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPredicatedBooleanExpression" ):
                return visitor.visitPredicatedBooleanExpression(self)
            else:
                return visitor.visitChildren(self)


    class UnaryBooleanExpressionContext(BooleanExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.BooleanExpressionContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def booleanExpression(self):
            return self.getTypedRuleContext(IceSqlParser.BooleanExpressionContext,0)

        def NOT(self):
            return self.getToken(IceSqlParser.NOT, 0)

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
        localctx = IceSqlParser.BooleanExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 34
        self.enterRecursionRule(localctx, 34, self.RULE_booleanExpression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 290
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
            if la_ == 1:
                localctx = IceSqlParser.PredicatedBooleanExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 284
                localctx._valueExpression = self.valueExpression(0)
                self.state = 286
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,29,self._ctx)
                if la_ == 1:
                    self.state = 285
                    self.predicate(localctx._valueExpression)


                pass

            elif la_ == 2:
                localctx = IceSqlParser.UnaryBooleanExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 288
                localctx.op = self.match(IceSqlParser.NOT)
                self.state = 289
                self.booleanExpression(2)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 297
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,31,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = IceSqlParser.BinaryBooleanExpressionContext(self, IceSqlParser.BooleanExpressionContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_booleanExpression)
                    self.state = 292
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 293
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==IceSqlParser.AND or _la==IceSqlParser.OR):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 294
                    self.booleanExpression(2) 
                self.state = 299
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,31,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PredicateContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1, value:ParserRuleContext=None):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None
            self.value = value


        def getRuleIndex(self):
            return IceSqlParser.RULE_predicate

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)
            self.value = ctx.value



    class BetweenPredicateContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PredicateContext
            super().__init__(parser)
            self.lower = None # ValueExpressionContext
            self.upper = None # ValueExpressionContext
            self.copyFrom(ctx)

        def BETWEEN(self):
            return self.getToken(IceSqlParser.BETWEEN, 0)
        def AND(self):
            return self.getToken(IceSqlParser.AND, 0)
        def valueExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ValueExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ValueExpressionContext,i)

        def NOT(self):
            return self.getToken(IceSqlParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBetweenPredicate" ):
                listener.enterBetweenPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBetweenPredicate" ):
                listener.exitBetweenPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBetweenPredicate" ):
                return visitor.visitBetweenPredicate(self)
            else:
                return visitor.visitChildren(self)


    class IsNullPredicateContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PredicateContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IS(self):
            return self.getToken(IceSqlParser.IS, 0)
        def NULL(self):
            return self.getToken(IceSqlParser.NULL, 0)
        def NOT(self):
            return self.getToken(IceSqlParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIsNullPredicate" ):
                listener.enterIsNullPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIsNullPredicate" ):
                listener.exitIsNullPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIsNullPredicate" ):
                return visitor.visitIsNullPredicate(self)
            else:
                return visitor.visitChildren(self)


    class CmpPredicateContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PredicateContext
            super().__init__(parser)
            self.right = None # ValueExpressionContext
            self.copyFrom(ctx)

        def cmpOp(self):
            return self.getTypedRuleContext(IceSqlParser.CmpOpContext,0)

        def valueExpression(self):
            return self.getTypedRuleContext(IceSqlParser.ValueExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCmpPredicate" ):
                listener.enterCmpPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCmpPredicate" ):
                listener.exitCmpPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCmpPredicate" ):
                return visitor.visitCmpPredicate(self)
            else:
                return visitor.visitChildren(self)


    class LikePredicateContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PredicateContext
            super().__init__(parser)
            self.kind = None # Token
            self.esc = None # StringContext
            self.copyFrom(ctx)

        def LIKE(self):
            return self.getToken(IceSqlParser.LIKE, 0)
        def ILIKE(self):
            return self.getToken(IceSqlParser.ILIKE, 0)
        def RLIKE(self):
            return self.getToken(IceSqlParser.RLIKE, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ExpressionContext,i)

        def NOT(self):
            return self.getToken(IceSqlParser.NOT, 0)
        def ANY(self):
            return self.getToken(IceSqlParser.ANY, 0)
        def ESCAPE(self):
            return self.getToken(IceSqlParser.ESCAPE, 0)
        def string(self):
            return self.getTypedRuleContext(IceSqlParser.StringContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLikePredicate" ):
                listener.enterLikePredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLikePredicate" ):
                listener.exitLikePredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLikePredicate" ):
                return visitor.visitLikePredicate(self)
            else:
                return visitor.visitChildren(self)


    class InSelectPredicateContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PredicateContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IN(self):
            return self.getToken(IceSqlParser.IN, 0)
        def select(self):
            return self.getTypedRuleContext(IceSqlParser.SelectContext,0)

        def NOT(self):
            return self.getToken(IceSqlParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInSelectPredicate" ):
                listener.enterInSelectPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInSelectPredicate" ):
                listener.exitInSelectPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInSelectPredicate" ):
                return visitor.visitInSelectPredicate(self)
            else:
                return visitor.visitChildren(self)


    class InListPredicateContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PredicateContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IN(self):
            return self.getToken(IceSqlParser.IN, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ExpressionContext,i)

        def NOT(self):
            return self.getToken(IceSqlParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInListPredicate" ):
                listener.enterInListPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInListPredicate" ):
                listener.exitInListPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInListPredicate" ):
                return visitor.visitInListPredicate(self)
            else:
                return visitor.visitChildren(self)


    class InJinjaPredicateContext(PredicateContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PredicateContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IN(self):
            return self.getToken(IceSqlParser.IN, 0)
        def JINJA(self):
            return self.getToken(IceSqlParser.JINJA, 0)
        def NOT(self):
            return self.getToken(IceSqlParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInJinjaPredicate" ):
                listener.enterInJinjaPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInJinjaPredicate" ):
                listener.exitInJinjaPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInJinjaPredicate" ):
                return visitor.visitInJinjaPredicate(self)
            else:
                return visitor.visitChildren(self)



    def predicate(self, value:ParserRuleContext):

        localctx = IceSqlParser.PredicateContext(self, self._ctx, self.state, value)
        self.enterRule(localctx, 36, self.RULE_predicate)
        self._la = 0 # Token type
        try:
            self.state = 369
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,43,self._ctx)
            if la_ == 1:
                localctx = IceSqlParser.CmpPredicateContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 300
                self.cmpOp()
                self.state = 301
                localctx.right = self.valueExpression(0)
                pass

            elif la_ == 2:
                localctx = IceSqlParser.IsNullPredicateContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 303
                self.match(IceSqlParser.IS)
                self.state = 305
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==IceSqlParser.NOT:
                    self.state = 304
                    self.match(IceSqlParser.NOT)


                self.state = 307
                self.match(IceSqlParser.NULL)
                pass

            elif la_ == 3:
                localctx = IceSqlParser.BetweenPredicateContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 309
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==IceSqlParser.NOT:
                    self.state = 308
                    self.match(IceSqlParser.NOT)


                self.state = 311
                self.match(IceSqlParser.BETWEEN)
                self.state = 312
                localctx.lower = self.valueExpression(0)
                self.state = 313
                self.match(IceSqlParser.AND)
                self.state = 314
                localctx.upper = self.valueExpression(0)
                pass

            elif la_ == 4:
                localctx = IceSqlParser.InListPredicateContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 317
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==IceSqlParser.NOT:
                    self.state = 316
                    self.match(IceSqlParser.NOT)


                self.state = 319
                self.match(IceSqlParser.IN)
                self.state = 320
                self.match(IceSqlParser.T__0)
                self.state = 321
                self.expression()
                self.state = 326
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 322
                    self.match(IceSqlParser.T__1)
                    self.state = 323
                    self.expression()
                    self.state = 328
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 329
                self.match(IceSqlParser.T__2)
                pass

            elif la_ == 5:
                localctx = IceSqlParser.InSelectPredicateContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 332
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==IceSqlParser.NOT:
                    self.state = 331
                    self.match(IceSqlParser.NOT)


                self.state = 334
                self.match(IceSqlParser.IN)
                self.state = 335
                self.match(IceSqlParser.T__0)
                self.state = 336
                self.select()
                self.state = 337
                self.match(IceSqlParser.T__2)
                pass

            elif la_ == 6:
                localctx = IceSqlParser.InJinjaPredicateContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 340
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==IceSqlParser.NOT:
                    self.state = 339
                    self.match(IceSqlParser.NOT)


                self.state = 342
                self.match(IceSqlParser.IN)
                self.state = 343
                self.match(IceSqlParser.JINJA)
                pass

            elif la_ == 7:
                localctx = IceSqlParser.LikePredicateContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 345
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==IceSqlParser.NOT:
                    self.state = 344
                    self.match(IceSqlParser.NOT)


                self.state = 347
                localctx.kind = self._input.LT(1)
                _la = self._input.LA(1)
                if not(((((_la - 59)) & ~0x3f) == 0 and ((1 << (_la - 59)) & ((1 << (IceSqlParser.ILIKE - 59)) | (1 << (IceSqlParser.LIKE - 59)) | (1 << (IceSqlParser.RLIKE - 59)))) != 0)):
                    localctx.kind = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 349
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
                if la_ == 1:
                    self.state = 348
                    self.match(IceSqlParser.ANY)


                self.state = 363
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,41,self._ctx)
                if la_ == 1:
                    self.state = 351
                    self.expression()
                    pass

                elif la_ == 2:
                    self.state = 352
                    self.match(IceSqlParser.T__0)
                    self.state = 353
                    self.expression()
                    self.state = 358
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==IceSqlParser.T__1:
                        self.state = 354
                        self.match(IceSqlParser.T__1)
                        self.state = 355
                        self.expression()
                        self.state = 360
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 361
                    self.match(IceSqlParser.T__2)
                    pass


                self.state = 367
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,42,self._ctx)
                if la_ == 1:
                    self.state = 365
                    self.match(IceSqlParser.ESCAPE)
                    self.state = 366
                    localctx.esc = self.string()


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return IceSqlParser.RULE_valueExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class PrimaryValueExpressionContext(ValueExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.ValueExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def primaryExpression(self):
            return self.getTypedRuleContext(IceSqlParser.PrimaryExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimaryValueExpression" ):
                listener.enterPrimaryValueExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimaryValueExpression" ):
                listener.exitPrimaryValueExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryValueExpression" ):
                return visitor.visitPrimaryValueExpression(self)
            else:
                return visitor.visitChildren(self)


    class UnaryValueExpressionContext(ValueExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.ValueExpressionContext
            super().__init__(parser)
            self.op = None # UnaryOpContext
            self.copyFrom(ctx)

        def valueExpression(self):
            return self.getTypedRuleContext(IceSqlParser.ValueExpressionContext,0)

        def unaryOp(self):
            return self.getTypedRuleContext(IceSqlParser.UnaryOpContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryValueExpression" ):
                listener.enterUnaryValueExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryValueExpression" ):
                listener.exitUnaryValueExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryValueExpression" ):
                return visitor.visitUnaryValueExpression(self)
            else:
                return visitor.visitChildren(self)


    class TraversalValueExpressionContext(ValueExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.ValueExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valueExpression(self):
            return self.getTypedRuleContext(IceSqlParser.ValueExpressionContext,0)

        def traversalKey(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.TraversalKeyContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.TraversalKeyContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTraversalValueExpression" ):
                listener.enterTraversalValueExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTraversalValueExpression" ):
                listener.exitTraversalValueExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTraversalValueExpression" ):
                return visitor.visitTraversalValueExpression(self)
            else:
                return visitor.visitChildren(self)


    class CastValueExpressionContext(ValueExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.ValueExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valueExpression(self):
            return self.getTypedRuleContext(IceSqlParser.ValueExpressionContext,0)

        def typeSpec(self):
            return self.getTypedRuleContext(IceSqlParser.TypeSpecContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCastValueExpression" ):
                listener.enterCastValueExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCastValueExpression" ):
                listener.exitCastValueExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCastValueExpression" ):
                return visitor.visitCastValueExpression(self)
            else:
                return visitor.visitChildren(self)


    class ArithValueExpressionContext(ValueExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.ValueExpressionContext
            super().__init__(parser)
            self.left = None # ValueExpressionContext
            self.op = None # ArithOpContext
            self.right = None # ValueExpressionContext
            self.copyFrom(ctx)

        def valueExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ValueExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ValueExpressionContext,i)

        def arithOp(self):
            return self.getTypedRuleContext(IceSqlParser.ArithOpContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithValueExpression" ):
                listener.enterArithValueExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithValueExpression" ):
                listener.exitArithValueExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArithValueExpression" ):
                return visitor.visitArithValueExpression(self)
            else:
                return visitor.visitChildren(self)



    def valueExpression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = IceSqlParser.ValueExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 38
        self.enterRecursionRule(localctx, 38, self.RULE_valueExpression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 376
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,44,self._ctx)
            if la_ == 1:
                localctx = IceSqlParser.PrimaryValueExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 372
                self.primaryExpression()
                pass

            elif la_ == 2:
                localctx = IceSqlParser.UnaryValueExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 373
                localctx.op = self.unaryOp()
                self.state = 374
                self.valueExpression(4)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 410
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,50,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 408
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
                    if la_ == 1:
                        localctx = IceSqlParser.ArithValueExpressionContext(self, IceSqlParser.ValueExpressionContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valueExpression)
                        self.state = 378
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 379
                        localctx.op = self.arithOp()
                        self.state = 380
                        localctx.right = self.valueExpression(4)
                        pass

                    elif la_ == 2:
                        localctx = IceSqlParser.TraversalValueExpressionContext(self, IceSqlParser.ValueExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valueExpression)
                        self.state = 382
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 392
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,46,self._ctx)
                        if la_ == 1:
                            self.state = 383
                            self.match(IceSqlParser.T__5)
                            self.state = 384
                            self.traversalKey()
                            pass

                        elif la_ == 2:
                            self.state = 386
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if _la==IceSqlParser.T__5:
                                self.state = 385
                                self.match(IceSqlParser.T__5)


                            self.state = 388
                            self.match(IceSqlParser.T__6)
                            self.state = 389
                            self.traversalKey()
                            self.state = 390
                            self.match(IceSqlParser.T__7)
                            pass


                        self.state = 402
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input,48,self._ctx)
                        while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                            if _alt==1:
                                self.state = 400
                                self._errHandler.sync(self)
                                token = self._input.LA(1)
                                if token in [IceSqlParser.T__4]:
                                    self.state = 394
                                    self.match(IceSqlParser.T__4)
                                    self.state = 395
                                    self.traversalKey()
                                    pass
                                elif token in [IceSqlParser.T__6]:
                                    self.state = 396
                                    self.match(IceSqlParser.T__6)
                                    self.state = 397
                                    self.traversalKey()
                                    self.state = 398
                                    self.match(IceSqlParser.T__7)
                                    pass
                                else:
                                    raise NoViableAltException(self)
                         
                            self.state = 404
                            self._errHandler.sync(self)
                            _alt = self._interp.adaptivePredict(self._input,48,self._ctx)

                        pass

                    elif la_ == 3:
                        localctx = IceSqlParser.CastValueExpressionContext(self, IceSqlParser.ValueExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valueExpression)
                        self.state = 405
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 406
                        self.match(IceSqlParser.T__8)
                        self.state = 407
                        self.typeSpec()
                        pass

             
                self.state = 412
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,50,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class TraversalKeyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierContext,0)


        def string(self):
            return self.getTypedRuleContext(IceSqlParser.StringContext,0)


        def integer(self):
            return self.getTypedRuleContext(IceSqlParser.IntegerContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_traversalKey

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTraversalKey" ):
                listener.enterTraversalKey(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTraversalKey" ):
                listener.exitTraversalKey(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTraversalKey" ):
                return visitor.visitTraversalKey(self)
            else:
                return visitor.visitChildren(self)




    def traversalKey(self):

        localctx = IceSqlParser.TraversalKeyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_traversalKey)
        try:
            self.state = 416
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [IceSqlParser.CASE, IceSqlParser.DATE, IceSqlParser.DAY, IceSqlParser.EXTRACT, IceSqlParser.FIRST, IceSqlParser.GROUPING, IceSqlParser.HOUR, IceSqlParser.ILIKE, IceSqlParser.LAST, IceSqlParser.LEFT, IceSqlParser.LIKE, IceSqlParser.MINUTE, IceSqlParser.MONTH, IceSqlParser.OUTER, IceSqlParser.RANGE, IceSqlParser.REPLACE, IceSqlParser.RIGHT, IceSqlParser.RLIKE, IceSqlParser.SECOND, IceSqlParser.YEAR, IceSqlParser.IDENTIFIER, IceSqlParser.QUOTED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 413
                self.identifier()
                pass
            elif token in [IceSqlParser.STRING]:
                self.enterOuterAlt(localctx, 2)
                self.state = 414
                self.string()
                pass
            elif token in [IceSqlParser.INTEGER_VALUE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 415
                self.integer()
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


    class PrimaryExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return IceSqlParser.RULE_primaryExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class IntervalExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INTERVAL(self):
            return self.getToken(IceSqlParser.INTERVAL, 0)
        def expression(self):
            return self.getTypedRuleContext(IceSqlParser.ExpressionContext,0)

        def intervalUnit(self):
            return self.getTypedRuleContext(IceSqlParser.IntervalUnitContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntervalExpression" ):
                listener.enterIntervalExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntervalExpression" ):
                listener.exitIntervalExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntervalExpression" ):
                return visitor.visitIntervalExpression(self)
            else:
                return visitor.visitChildren(self)


    class ExtractExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.part = None # IdentifierContext
            self.value = None # ExpressionContext
            self.copyFrom(ctx)

        def EXTRACT(self):
            return self.getToken(IceSqlParser.EXTRACT, 0)
        def FROM(self):
            return self.getToken(IceSqlParser.FROM, 0)
        def identifier(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierContext,0)

        def expression(self):
            return self.getTypedRuleContext(IceSqlParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExtractExpression" ):
                listener.enterExtractExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExtractExpression" ):
                listener.exitExtractExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtractExpression" ):
                return visitor.visitExtractExpression(self)
            else:
                return visitor.visitChildren(self)


    class CastCallExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CAST(self):
            return self.getToken(IceSqlParser.CAST, 0)
        def expression(self):
            return self.getTypedRuleContext(IceSqlParser.ExpressionContext,0)

        def AS(self):
            return self.getToken(IceSqlParser.AS, 0)
        def typeSpec(self):
            return self.getTypedRuleContext(IceSqlParser.TypeSpecContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCastCallExpression" ):
                listener.enterCastCallExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCastCallExpression" ):
                listener.exitCastCallExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCastCallExpression" ):
                return visitor.visitCastCallExpression(self)
            else:
                return visitor.visitChildren(self)


    class SimplePrimaryExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def simpleExpression(self):
            return self.getTypedRuleContext(IceSqlParser.SimpleExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimplePrimaryExpression" ):
                listener.enterSimplePrimaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimplePrimaryExpression" ):
                listener.exitSimplePrimaryExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimplePrimaryExpression" ):
                return visitor.visitSimplePrimaryExpression(self)
            else:
                return visitor.visitChildren(self)


    class CaseExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.val = None # ExpressionContext
            self.default = None # ExpressionContext
            self.copyFrom(ctx)

        def CASE(self):
            return self.getToken(IceSqlParser.CASE, 0)
        def END(self):
            return self.getToken(IceSqlParser.END, 0)
        def caseItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.CaseItemContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.CaseItemContext,i)

        def ELSE(self):
            return self.getToken(IceSqlParser.ELSE, 0)
        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseExpression" ):
                listener.enterCaseExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseExpression" ):
                listener.exitCaseExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseExpression" ):
                return visitor.visitCaseExpression(self)
            else:
                return visitor.visitChildren(self)


    class FunctionCallExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def functionCall(self):
            return self.getTypedRuleContext(IceSqlParser.FunctionCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCallExpression" ):
                listener.enterFunctionCallExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCallExpression" ):
                listener.exitFunctionCallExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallExpression" ):
                return visitor.visitFunctionCallExpression(self)
            else:
                return visitor.visitChildren(self)


    class DateExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DATE(self):
            return self.getToken(IceSqlParser.DATE, 0)
        def string(self):
            return self.getTypedRuleContext(IceSqlParser.StringContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateExpression" ):
                listener.enterDateExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateExpression" ):
                listener.exitDateExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDateExpression" ):
                return visitor.visitDateExpression(self)
            else:
                return visitor.visitChildren(self)


    class ParenExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(IceSqlParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpression" ):
                listener.enterParenExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpression" ):
                listener.exitParenExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpression" ):
                return visitor.visitParenExpression(self)
            else:
                return visitor.visitChildren(self)


    class JinjaExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def JINJA(self):
            return self.getToken(IceSqlParser.JINJA, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJinjaExpression" ):
                listener.enterJinjaExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJinjaExpression" ):
                listener.exitJinjaExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJinjaExpression" ):
                return visitor.visitJinjaExpression(self)
            else:
                return visitor.visitChildren(self)


    class SelectExpressionContext(PrimaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.PrimaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def select(self):
            return self.getTypedRuleContext(IceSqlParser.SelectContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectExpression" ):
                listener.enterSelectExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectExpression" ):
                listener.exitSelectExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectExpression" ):
                return visitor.visitSelectExpression(self)
            else:
                return visitor.visitChildren(self)



    def primaryExpression(self):

        localctx = IceSqlParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_primaryExpression)
        self._la = 0 # Token type
        try:
            self.state = 472
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,55,self._ctx)
            if la_ == 1:
                localctx = IceSqlParser.FunctionCallExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 418
                self.functionCall()
                pass

            elif la_ == 2:
                localctx = IceSqlParser.CaseExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 419
                self.match(IceSqlParser.CASE)
                self.state = 421
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,52,self._ctx)
                if la_ == 1:
                    self.state = 420
                    localctx.val = self.expression()


                self.state = 426
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.WHEN:
                    self.state = 423
                    self.caseItem()
                    self.state = 428
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 431
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==IceSqlParser.ELSE:
                    self.state = 429
                    self.match(IceSqlParser.ELSE)
                    self.state = 430
                    localctx.default = self.expression()


                self.state = 433
                self.match(IceSqlParser.END)
                pass

            elif la_ == 3:
                localctx = IceSqlParser.IntervalExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 434
                if not  not self.config.interval_units :
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, " not self.config.interval_units ")
                self.state = 435
                self.match(IceSqlParser.INTERVAL)
                self.state = 436
                self.expression()
                pass

            elif la_ == 4:
                localctx = IceSqlParser.IntervalExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 437
                if not  self.config.interval_units :
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, " self.config.interval_units ")
                self.state = 438
                self.match(IceSqlParser.INTERVAL)
                self.state = 439
                self.expression()
                self.state = 440
                self.intervalUnit()
                pass

            elif la_ == 5:
                localctx = IceSqlParser.IntervalExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 442
                self.match(IceSqlParser.INTERVAL)
                self.state = 443
                self.expression()
                self.state = 444
                self.intervalUnit()
                pass

            elif la_ == 6:
                localctx = IceSqlParser.SelectExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 446
                self.match(IceSqlParser.T__0)
                self.state = 447
                self.select()
                self.state = 448
                self.match(IceSqlParser.T__2)
                pass

            elif la_ == 7:
                localctx = IceSqlParser.ParenExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 450
                self.match(IceSqlParser.T__0)
                self.state = 451
                self.expression()
                self.state = 452
                self.match(IceSqlParser.T__2)
                pass

            elif la_ == 8:
                localctx = IceSqlParser.CastCallExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 454
                self.match(IceSqlParser.CAST)
                self.state = 455
                self.match(IceSqlParser.T__0)
                self.state = 456
                self.expression()
                self.state = 457
                self.match(IceSqlParser.AS)
                self.state = 458
                self.typeSpec()
                self.state = 459
                self.match(IceSqlParser.T__2)
                pass

            elif la_ == 9:
                localctx = IceSqlParser.DateExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 461
                self.match(IceSqlParser.DATE)
                self.state = 462
                self.string()
                pass

            elif la_ == 10:
                localctx = IceSqlParser.ExtractExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 463
                self.match(IceSqlParser.EXTRACT)
                self.state = 464
                self.match(IceSqlParser.T__0)
                self.state = 465
                localctx.part = self.identifier()
                self.state = 466
                self.match(IceSqlParser.FROM)
                self.state = 467
                localctx.value = self.expression()
                self.state = 468
                self.match(IceSqlParser.T__2)
                pass

            elif la_ == 11:
                localctx = IceSqlParser.JinjaExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 11)
                self.state = 470
                self.match(IceSqlParser.JINJA)
                pass

            elif la_ == 12:
                localctx = IceSqlParser.SimplePrimaryExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 12)
                self.state = 471
                self.simpleExpression()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SimpleExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def var(self):
            return self.getTypedRuleContext(IceSqlParser.VarContext,0)


        def param(self):
            return self.getTypedRuleContext(IceSqlParser.ParamContext,0)


        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)


        def number(self):
            return self.getTypedRuleContext(IceSqlParser.NumberContext,0)


        def string(self):
            return self.getTypedRuleContext(IceSqlParser.StringContext,0)


        def null(self):
            return self.getTypedRuleContext(IceSqlParser.NullContext,0)


        def true(self):
            return self.getTypedRuleContext(IceSqlParser.TrueContext,0)


        def false(self):
            return self.getTypedRuleContext(IceSqlParser.FalseContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_simpleExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleExpression" ):
                listener.enterSimpleExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleExpression" ):
                listener.exitSimpleExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleExpression" ):
                return visitor.visitSimpleExpression(self)
            else:
                return visitor.visitChildren(self)




    def simpleExpression(self):

        localctx = IceSqlParser.SimpleExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_simpleExpression)
        try:
            self.state = 482
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [IceSqlParser.T__10]:
                self.enterOuterAlt(localctx, 1)
                self.state = 474
                self.var()
                pass
            elif token in [IceSqlParser.T__5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 475
                self.param()
                pass
            elif token in [IceSqlParser.CASE, IceSqlParser.DATE, IceSqlParser.DAY, IceSqlParser.EXTRACT, IceSqlParser.FIRST, IceSqlParser.GROUPING, IceSqlParser.HOUR, IceSqlParser.ILIKE, IceSqlParser.LAST, IceSqlParser.LEFT, IceSqlParser.LIKE, IceSqlParser.MINUTE, IceSqlParser.MONTH, IceSqlParser.OUTER, IceSqlParser.RANGE, IceSqlParser.REPLACE, IceSqlParser.RIGHT, IceSqlParser.RLIKE, IceSqlParser.SECOND, IceSqlParser.YEAR, IceSqlParser.IDENTIFIER, IceSqlParser.QUOTED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 3)
                self.state = 476
                self.qualifiedName()
                pass
            elif token in [IceSqlParser.INTEGER_VALUE, IceSqlParser.DECIMAL_VALUE, IceSqlParser.FLOAT_VALUE]:
                self.enterOuterAlt(localctx, 4)
                self.state = 477
                self.number()
                pass
            elif token in [IceSqlParser.STRING]:
                self.enterOuterAlt(localctx, 5)
                self.state = 478
                self.string()
                pass
            elif token in [IceSqlParser.NULL]:
                self.enterOuterAlt(localctx, 6)
                self.state = 479
                self.null()
                pass
            elif token in [IceSqlParser.TRUE]:
                self.enterOuterAlt(localctx, 7)
                self.state = 480
                self.true()
                pass
            elif token in [IceSqlParser.FALSE]:
                self.enterOuterAlt(localctx, 8)
                self.state = 481
                self.false()
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


    class TypeSpecContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierContext,0)


        def simpleExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.SimpleExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.SimpleExpressionContext,i)


        def getRuleIndex(self):
            return IceSqlParser.RULE_typeSpec

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeSpec" ):
                listener.enterTypeSpec(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeSpec" ):
                listener.exitTypeSpec(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeSpec" ):
                return visitor.visitTypeSpec(self)
            else:
                return visitor.visitChildren(self)




    def typeSpec(self):

        localctx = IceSqlParser.TypeSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_typeSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 484
            self.identifier()
            self.state = 497
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,59,self._ctx)
            if la_ == 1:
                self.state = 485
                self.match(IceSqlParser.T__0)
                self.state = 494
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << IceSqlParser.T__5) | (1 << IceSqlParser.T__10) | (1 << IceSqlParser.CASE) | (1 << IceSqlParser.DATE) | (1 << IceSqlParser.DAY) | (1 << IceSqlParser.EXTRACT) | (1 << IceSqlParser.FALSE) | (1 << IceSqlParser.FIRST) | (1 << IceSqlParser.GROUPING) | (1 << IceSqlParser.HOUR) | (1 << IceSqlParser.ILIKE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (IceSqlParser.LAST - 68)) | (1 << (IceSqlParser.LEFT - 68)) | (1 << (IceSqlParser.LIKE - 68)) | (1 << (IceSqlParser.MINUTE - 68)) | (1 << (IceSqlParser.MONTH - 68)) | (1 << (IceSqlParser.NULL - 68)) | (1 << (IceSqlParser.OUTER - 68)) | (1 << (IceSqlParser.RANGE - 68)) | (1 << (IceSqlParser.REPLACE - 68)) | (1 << (IceSqlParser.RIGHT - 68)) | (1 << (IceSqlParser.RLIKE - 68)) | (1 << (IceSqlParser.SECOND - 68)) | (1 << (IceSqlParser.TRUE - 68)) | (1 << (IceSqlParser.YEAR - 68)) | (1 << (IceSqlParser.STRING - 68)) | (1 << (IceSqlParser.INTEGER_VALUE - 68)) | (1 << (IceSqlParser.DECIMAL_VALUE - 68)) | (1 << (IceSqlParser.FLOAT_VALUE - 68)) | (1 << (IceSqlParser.IDENTIFIER - 68)) | (1 << (IceSqlParser.QUOTED_IDENTIFIER - 68)))) != 0):
                    self.state = 486
                    self.simpleExpression()
                    self.state = 491
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==IceSqlParser.T__1:
                        self.state = 487
                        self.match(IceSqlParser.T__1)
                        self.state = 488
                        self.simpleExpression()
                        self.state = 493
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 496
                self.match(IceSqlParser.T__2)


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


        def getRuleIndex(self):
            return IceSqlParser.RULE_functionCall

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class NullsFunctionCallContext(FunctionCallContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.FunctionCallContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)

        def expression(self):
            return self.getTypedRuleContext(IceSqlParser.ExpressionContext,0)

        def NULLS(self):
            return self.getToken(IceSqlParser.NULLS, 0)
        def IGNORE(self):
            return self.getToken(IceSqlParser.IGNORE, 0)
        def RESPECT(self):
            return self.getToken(IceSqlParser.RESPECT, 0)
        def setQuantifier(self):
            return self.getTypedRuleContext(IceSqlParser.SetQuantifierContext,0)

        def WITHIN(self):
            return self.getToken(IceSqlParser.WITHIN, 0)
        def GROUP(self):
            return self.getToken(IceSqlParser.GROUP, 0)
        def ORDER(self):
            return self.getToken(IceSqlParser.ORDER, 0)
        def BY(self):
            return self.getToken(IceSqlParser.BY, 0)
        def sortItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.SortItemContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.SortItemContext,i)

        def over(self):
            return self.getTypedRuleContext(IceSqlParser.OverContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNullsFunctionCall" ):
                listener.enterNullsFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNullsFunctionCall" ):
                listener.exitNullsFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNullsFunctionCall" ):
                return visitor.visitNullsFunctionCall(self)
            else:
                return visitor.visitChildren(self)


    class ExpressionFunctionCallContext(FunctionCallContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.FunctionCallContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)

        def setQuantifier(self):
            return self.getTypedRuleContext(IceSqlParser.SetQuantifierContext,0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ExpressionContext,i)

        def NULLS(self):
            return self.getToken(IceSqlParser.NULLS, 0)
        def WITHIN(self):
            return self.getToken(IceSqlParser.WITHIN, 0)
        def GROUP(self):
            return self.getToken(IceSqlParser.GROUP, 0)
        def ORDER(self):
            return self.getToken(IceSqlParser.ORDER, 0)
        def BY(self):
            return self.getToken(IceSqlParser.BY, 0)
        def sortItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.SortItemContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.SortItemContext,i)

        def over(self):
            return self.getTypedRuleContext(IceSqlParser.OverContext,0)

        def IGNORE(self):
            return self.getToken(IceSqlParser.IGNORE, 0)
        def RESPECT(self):
            return self.getToken(IceSqlParser.RESPECT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpressionFunctionCall" ):
                listener.enterExpressionFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpressionFunctionCall" ):
                listener.exitExpressionFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionFunctionCall" ):
                return visitor.visitExpressionFunctionCall(self)
            else:
                return visitor.visitChildren(self)


    class KwargFunctionCallContext(FunctionCallContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.FunctionCallContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)

        def kwarg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.KwargContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.KwargContext,i)

        def NULLS(self):
            return self.getToken(IceSqlParser.NULLS, 0)
        def WITHIN(self):
            return self.getToken(IceSqlParser.WITHIN, 0)
        def GROUP(self):
            return self.getToken(IceSqlParser.GROUP, 0)
        def ORDER(self):
            return self.getToken(IceSqlParser.ORDER, 0)
        def BY(self):
            return self.getToken(IceSqlParser.BY, 0)
        def sortItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.SortItemContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.SortItemContext,i)

        def over(self):
            return self.getTypedRuleContext(IceSqlParser.OverContext,0)

        def IGNORE(self):
            return self.getToken(IceSqlParser.IGNORE, 0)
        def RESPECT(self):
            return self.getToken(IceSqlParser.RESPECT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKwargFunctionCall" ):
                listener.enterKwargFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKwargFunctionCall" ):
                listener.exitKwargFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKwargFunctionCall" ):
                return visitor.visitKwargFunctionCall(self)
            else:
                return visitor.visitChildren(self)


    class StarFunctionCallContext(FunctionCallContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.FunctionCallContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)

        def over(self):
            return self.getTypedRuleContext(IceSqlParser.OverContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStarFunctionCall" ):
                listener.enterStarFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStarFunctionCall" ):
                listener.exitStarFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStarFunctionCall" ):
                return visitor.visitStarFunctionCall(self)
            else:
                return visitor.visitChildren(self)



    def functionCall(self):

        localctx = IceSqlParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.state = 610
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,77,self._ctx)
            if la_ == 1:
                localctx = IceSqlParser.ExpressionFunctionCallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 499
                self.qualifiedName()
                self.state = 500
                self.match(IceSqlParser.T__0)
                self.state = 502
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,60,self._ctx)
                if la_ == 1:
                    self.state = 501
                    self.setQuantifier()


                self.state = 512
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,62,self._ctx)
                if la_ == 1:
                    self.state = 504
                    self.expression()
                    self.state = 509
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==IceSqlParser.T__1:
                        self.state = 505
                        self.match(IceSqlParser.T__1)
                        self.state = 506
                        self.expression()
                        self.state = 511
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 514
                self.match(IceSqlParser.T__2)
                self.state = 517
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,63,self._ctx)
                if la_ == 1:
                    self.state = 515
                    _la = self._input.LA(1)
                    if not(_la==IceSqlParser.IGNORE or _la==IceSqlParser.RESPECT):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 516
                    self.match(IceSqlParser.NULLS)


                self.state = 534
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,65,self._ctx)
                if la_ == 1:
                    self.state = 519
                    self.match(IceSqlParser.WITHIN)
                    self.state = 520
                    self.match(IceSqlParser.GROUP)
                    self.state = 521
                    self.match(IceSqlParser.T__0)
                    self.state = 522
                    self.match(IceSqlParser.ORDER)
                    self.state = 523
                    self.match(IceSqlParser.BY)
                    self.state = 524
                    self.sortItem()
                    self.state = 529
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==IceSqlParser.T__1:
                        self.state = 525
                        self.match(IceSqlParser.T__1)
                        self.state = 526
                        self.sortItem()
                        self.state = 531
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 532
                    self.match(IceSqlParser.T__2)


                self.state = 537
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,66,self._ctx)
                if la_ == 1:
                    self.state = 536
                    self.over()


                pass

            elif la_ == 2:
                localctx = IceSqlParser.KwargFunctionCallContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 539
                self.qualifiedName()
                self.state = 540
                self.match(IceSqlParser.T__0)
                self.state = 541
                self.kwarg()
                self.state = 546
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 542
                    self.match(IceSqlParser.T__1)
                    self.state = 543
                    self.kwarg()
                    self.state = 548
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 549
                self.match(IceSqlParser.T__2)
                self.state = 552
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,68,self._ctx)
                if la_ == 1:
                    self.state = 550
                    _la = self._input.LA(1)
                    if not(_la==IceSqlParser.IGNORE or _la==IceSqlParser.RESPECT):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 551
                    self.match(IceSqlParser.NULLS)


                self.state = 569
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,70,self._ctx)
                if la_ == 1:
                    self.state = 554
                    self.match(IceSqlParser.WITHIN)
                    self.state = 555
                    self.match(IceSqlParser.GROUP)
                    self.state = 556
                    self.match(IceSqlParser.T__0)
                    self.state = 557
                    self.match(IceSqlParser.ORDER)
                    self.state = 558
                    self.match(IceSqlParser.BY)
                    self.state = 559
                    self.sortItem()
                    self.state = 564
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==IceSqlParser.T__1:
                        self.state = 560
                        self.match(IceSqlParser.T__1)
                        self.state = 561
                        self.sortItem()
                        self.state = 566
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 567
                    self.match(IceSqlParser.T__2)


                self.state = 572
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,71,self._ctx)
                if la_ == 1:
                    self.state = 571
                    self.over()


                pass

            elif la_ == 3:
                localctx = IceSqlParser.NullsFunctionCallContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 574
                self.qualifiedName()
                self.state = 575
                self.match(IceSqlParser.T__0)
                self.state = 577
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,72,self._ctx)
                if la_ == 1:
                    self.state = 576
                    self.setQuantifier()


                self.state = 579
                self.expression()
                self.state = 580
                _la = self._input.LA(1)
                if not(_la==IceSqlParser.IGNORE or _la==IceSqlParser.RESPECT):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 581
                self.match(IceSqlParser.NULLS)
                self.state = 582
                self.match(IceSqlParser.T__2)
                self.state = 598
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,74,self._ctx)
                if la_ == 1:
                    self.state = 583
                    self.match(IceSqlParser.WITHIN)
                    self.state = 584
                    self.match(IceSqlParser.GROUP)
                    self.state = 585
                    self.match(IceSqlParser.T__0)
                    self.state = 586
                    self.match(IceSqlParser.ORDER)
                    self.state = 587
                    self.match(IceSqlParser.BY)
                    self.state = 588
                    self.sortItem()
                    self.state = 593
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==IceSqlParser.T__1:
                        self.state = 589
                        self.match(IceSqlParser.T__1)
                        self.state = 590
                        self.sortItem()
                        self.state = 595
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 596
                    self.match(IceSqlParser.T__2)


                self.state = 601
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,75,self._ctx)
                if la_ == 1:
                    self.state = 600
                    self.over()


                pass

            elif la_ == 4:
                localctx = IceSqlParser.StarFunctionCallContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 603
                self.qualifiedName()
                self.state = 604
                self.match(IceSqlParser.T__0)
                self.state = 605
                self.match(IceSqlParser.T__3)
                self.state = 606
                self.match(IceSqlParser.T__2)
                self.state = 608
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,76,self._ctx)
                if la_ == 1:
                    self.state = 607
                    self.over()


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KwargContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierContext,0)


        def expression(self):
            return self.getTypedRuleContext(IceSqlParser.ExpressionContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_kwarg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKwarg" ):
                listener.enterKwarg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKwarg" ):
                listener.exitKwarg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKwarg" ):
                return visitor.visitKwarg(self)
            else:
                return visitor.visitChildren(self)




    def kwarg(self):

        localctx = IceSqlParser.KwargContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_kwarg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 612
            self.identifier()
            self.state = 613
            self.match(IceSqlParser.T__9)
            self.state = 614
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CaseItemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHEN(self):
            return self.getToken(IceSqlParser.WHEN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ExpressionContext,i)


        def THEN(self):
            return self.getToken(IceSqlParser.THEN, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_caseItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseItem" ):
                listener.enterCaseItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseItem" ):
                listener.exitCaseItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseItem" ):
                return visitor.visitCaseItem(self)
            else:
                return visitor.visitChildren(self)




    def caseItem(self):

        localctx = IceSqlParser.CaseItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_caseItem)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 616
            self.match(IceSqlParser.WHEN)
            self.state = 617
            self.expression()
            self.state = 618
            self.match(IceSqlParser.THEN)
            self.state = 619
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntervalUnitContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SECOND(self):
            return self.getToken(IceSqlParser.SECOND, 0)

        def MINUTE(self):
            return self.getToken(IceSqlParser.MINUTE, 0)

        def HOUR(self):
            return self.getToken(IceSqlParser.HOUR, 0)

        def DAY(self):
            return self.getToken(IceSqlParser.DAY, 0)

        def MONTH(self):
            return self.getToken(IceSqlParser.MONTH, 0)

        def YEAR(self):
            return self.getToken(IceSqlParser.YEAR, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_intervalUnit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntervalUnit" ):
                listener.enterIntervalUnit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntervalUnit" ):
                listener.exitIntervalUnit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntervalUnit" ):
                return visitor.visitIntervalUnit(self)
            else:
                return visitor.visitChildren(self)




    def intervalUnit(self):

        localctx = IceSqlParser.IntervalUnitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_intervalUnit)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 621
            _la = self._input.LA(1)
            if not(_la==IceSqlParser.DAY or _la==IceSqlParser.HOUR or ((((_la - 74)) & ~0x3f) == 0 and ((1 << (_la - 74)) & ((1 << (IceSqlParser.MINUTE - 74)) | (1 << (IceSqlParser.MONTH - 74)) | (1 << (IceSqlParser.SECOND - 74)) | (1 << (IceSqlParser.YEAR - 74)))) != 0)):
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


    class OverContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OVER(self):
            return self.getToken(IceSqlParser.OVER, 0)

        def PARTITION(self):
            return self.getToken(IceSqlParser.PARTITION, 0)

        def BY(self, i:int=None):
            if i is None:
                return self.getTokens(IceSqlParser.BY)
            else:
                return self.getToken(IceSqlParser.BY, i)

        def ORDER(self):
            return self.getToken(IceSqlParser.ORDER, 0)

        def sortItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.SortItemContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.SortItemContext,i)


        def frame(self):
            return self.getTypedRuleContext(IceSqlParser.FrameContext,0)


        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ExpressionContext,i)


        def getRuleIndex(self):
            return IceSqlParser.RULE_over

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOver" ):
                listener.enterOver(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOver" ):
                listener.exitOver(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOver" ):
                return visitor.visitOver(self)
            else:
                return visitor.visitChildren(self)




    def over(self):

        localctx = IceSqlParser.OverContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_over)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 623
            self.match(IceSqlParser.OVER)
            self.state = 624
            self.match(IceSqlParser.T__0)
            self.state = 635
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.PARTITION:
                self.state = 625
                self.match(IceSqlParser.PARTITION)
                self.state = 626
                self.match(IceSqlParser.BY)

                self.state = 627
                self.expression()
                self.state = 632
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 628
                    self.match(IceSqlParser.T__1)
                    self.state = 629
                    self.expression()
                    self.state = 634
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 647
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.ORDER:
                self.state = 637
                self.match(IceSqlParser.ORDER)
                self.state = 638
                self.match(IceSqlParser.BY)
                self.state = 639
                self.sortItem()
                self.state = 644
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 640
                    self.match(IceSqlParser.T__1)
                    self.state = 641
                    self.sortItem()
                    self.state = 646
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 650
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.RANGE or _la==IceSqlParser.ROWS:
                self.state = 649
                self.frame()


            self.state = 652
            self.match(IceSqlParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FrameBoundContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return IceSqlParser.RULE_frameBound

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class NumFrameBoundContext(FrameBoundContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.FrameBoundContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INTEGER_VALUE(self):
            return self.getToken(IceSqlParser.INTEGER_VALUE, 0)
        def PRECEDING(self):
            return self.getToken(IceSqlParser.PRECEDING, 0)
        def FOLLOWING(self):
            return self.getToken(IceSqlParser.FOLLOWING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumFrameBound" ):
                listener.enterNumFrameBound(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumFrameBound" ):
                listener.exitNumFrameBound(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumFrameBound" ):
                return visitor.visitNumFrameBound(self)
            else:
                return visitor.visitChildren(self)


    class CurrentRowFrameBoundContext(FrameBoundContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.FrameBoundContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CURRENT(self):
            return self.getToken(IceSqlParser.CURRENT, 0)
        def ROW(self):
            return self.getToken(IceSqlParser.ROW, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCurrentRowFrameBound" ):
                listener.enterCurrentRowFrameBound(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCurrentRowFrameBound" ):
                listener.exitCurrentRowFrameBound(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCurrentRowFrameBound" ):
                return visitor.visitCurrentRowFrameBound(self)
            else:
                return visitor.visitChildren(self)


    class UnboundedFrameBoundContext(FrameBoundContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.FrameBoundContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def UNBOUNDED(self):
            return self.getToken(IceSqlParser.UNBOUNDED, 0)
        def PRECEDING(self):
            return self.getToken(IceSqlParser.PRECEDING, 0)
        def FOLLOWING(self):
            return self.getToken(IceSqlParser.FOLLOWING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnboundedFrameBound" ):
                listener.enterUnboundedFrameBound(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnboundedFrameBound" ):
                listener.exitUnboundedFrameBound(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnboundedFrameBound" ):
                return visitor.visitUnboundedFrameBound(self)
            else:
                return visitor.visitChildren(self)



    def frameBound(self):

        localctx = IceSqlParser.FrameBoundContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_frameBound)
        self._la = 0 # Token type
        try:
            self.state = 660
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [IceSqlParser.INTEGER_VALUE]:
                localctx = IceSqlParser.NumFrameBoundContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 654
                self.match(IceSqlParser.INTEGER_VALUE)
                self.state = 655
                _la = self._input.LA(1)
                if not(_la==IceSqlParser.FOLLOWING or _la==IceSqlParser.PRECEDING):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [IceSqlParser.UNBOUNDED]:
                localctx = IceSqlParser.UnboundedFrameBoundContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 656
                self.match(IceSqlParser.UNBOUNDED)
                self.state = 657
                _la = self._input.LA(1)
                if not(_la==IceSqlParser.FOLLOWING or _la==IceSqlParser.PRECEDING):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [IceSqlParser.CURRENT]:
                localctx = IceSqlParser.CurrentRowFrameBoundContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 658
                self.match(IceSqlParser.CURRENT)
                self.state = 659
                self.match(IceSqlParser.ROW)
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


    class FrameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return IceSqlParser.RULE_frame

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SingleFrameContext(FrameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.FrameContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def frameBound(self):
            return self.getTypedRuleContext(IceSqlParser.FrameBoundContext,0)

        def ROWS(self):
            return self.getToken(IceSqlParser.ROWS, 0)
        def RANGE(self):
            return self.getToken(IceSqlParser.RANGE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleFrame" ):
                listener.enterSingleFrame(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleFrame" ):
                listener.exitSingleFrame(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingleFrame" ):
                return visitor.visitSingleFrame(self)
            else:
                return visitor.visitChildren(self)


    class DoubleFrameContext(FrameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.FrameContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BETWEEN(self):
            return self.getToken(IceSqlParser.BETWEEN, 0)
        def frameBound(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.FrameBoundContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.FrameBoundContext,i)

        def AND(self):
            return self.getToken(IceSqlParser.AND, 0)
        def ROWS(self):
            return self.getToken(IceSqlParser.ROWS, 0)
        def RANGE(self):
            return self.getToken(IceSqlParser.RANGE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoubleFrame" ):
                listener.enterDoubleFrame(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoubleFrame" ):
                listener.exitDoubleFrame(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoubleFrame" ):
                return visitor.visitDoubleFrame(self)
            else:
                return visitor.visitChildren(self)



    def frame(self):

        localctx = IceSqlParser.FrameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_frame)
        self._la = 0 # Token type
        try:
            self.state = 670
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,84,self._ctx)
            if la_ == 1:
                localctx = IceSqlParser.SingleFrameContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 662
                _la = self._input.LA(1)
                if not(_la==IceSqlParser.RANGE or _la==IceSqlParser.ROWS):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 663
                self.frameBound()
                pass

            elif la_ == 2:
                localctx = IceSqlParser.DoubleFrameContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 664
                _la = self._input.LA(1)
                if not(_la==IceSqlParser.RANGE or _la==IceSqlParser.ROWS):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 665
                self.match(IceSqlParser.BETWEEN)
                self.state = 666
                self.frameBound()
                self.state = 667
                self.match(IceSqlParser.AND)
                self.state = 668
                self.frameBound()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SortItemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.direction = None # Token

        def expression(self):
            return self.getTypedRuleContext(IceSqlParser.ExpressionContext,0)


        def NULLS(self):
            return self.getToken(IceSqlParser.NULLS, 0)

        def FIRST(self):
            return self.getToken(IceSqlParser.FIRST, 0)

        def LAST(self):
            return self.getToken(IceSqlParser.LAST, 0)

        def ASC(self):
            return self.getToken(IceSqlParser.ASC, 0)

        def DESC(self):
            return self.getToken(IceSqlParser.DESC, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_sortItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSortItem" ):
                listener.enterSortItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSortItem" ):
                listener.exitSortItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSortItem" ):
                return visitor.visitSortItem(self)
            else:
                return visitor.visitChildren(self)




    def sortItem(self):

        localctx = IceSqlParser.SortItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_sortItem)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 672
            self.expression()
            self.state = 674
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.ASC or _la==IceSqlParser.DESC:
                self.state = 673
                localctx.direction = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==IceSqlParser.ASC or _la==IceSqlParser.DESC):
                    localctx.direction = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 678
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==IceSqlParser.NULLS:
                self.state = 676
                self.match(IceSqlParser.NULLS)
                self.state = 677
                _la = self._input.LA(1)
                if not(_la==IceSqlParser.FIRST or _la==IceSqlParser.LAST):
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


    class RelationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return IceSqlParser.RULE_relation

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class UnpivotRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.vc = None # IdentifierContext
            self.nc = None # IdentifierContext
            self.copyFrom(ctx)

        def relation(self):
            return self.getTypedRuleContext(IceSqlParser.RelationContext,0)

        def UNPIVOT(self):
            return self.getToken(IceSqlParser.UNPIVOT, 0)
        def FOR(self):
            return self.getToken(IceSqlParser.FOR, 0)
        def IN(self):
            return self.getToken(IceSqlParser.IN, 0)
        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.IdentifierContext,i)

        def identifierList(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierListContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnpivotRelation" ):
                listener.enterUnpivotRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnpivotRelation" ):
                listener.exitUnpivotRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnpivotRelation" ):
                return visitor.visitUnpivotRelation(self)
            else:
                return visitor.visitChildren(self)


    class FunctionCallRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def functionCall(self):
            return self.getTypedRuleContext(IceSqlParser.FunctionCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCallRelation" ):
                listener.enterFunctionCallRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCallRelation" ):
                listener.exitFunctionCallRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallRelation" ):
                return visitor.visitFunctionCallRelation(self)
            else:
                return visitor.visitChildren(self)


    class JinjaRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def JINJA(self):
            return self.getToken(IceSqlParser.JINJA, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJinjaRelation" ):
                listener.enterJinjaRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJinjaRelation" ):
                listener.exitJinjaRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJinjaRelation" ):
                return visitor.visitJinjaRelation(self)
            else:
                return visitor.visitChildren(self)


    class AliasedRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relation(self):
            return self.getTypedRuleContext(IceSqlParser.RelationContext,0)

        def identifier(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierContext,0)

        def AS(self):
            return self.getToken(IceSqlParser.AS, 0)
        def identifierList(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierListContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAliasedRelation" ):
                listener.enterAliasedRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAliasedRelation" ):
                listener.exitAliasedRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAliasedRelation" ):
                return visitor.visitAliasedRelation(self)
            else:
                return visitor.visitChildren(self)


    class LateralRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LATERAL(self):
            return self.getToken(IceSqlParser.LATERAL, 0)
        def relation(self):
            return self.getTypedRuleContext(IceSqlParser.RelationContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLateralRelation" ):
                listener.enterLateralRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLateralRelation" ):
                listener.exitLateralRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLateralRelation" ):
                return visitor.visitLateralRelation(self)
            else:
                return visitor.visitChildren(self)


    class JoinRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.left = None # RelationContext
            self.ty = None # JoinTypeContext
            self.right = None # RelationContext
            self.cond = None # BooleanExpressionContext
            self.using = None # IdentifierListContext
            self.copyFrom(ctx)

        def JOIN(self):
            return self.getToken(IceSqlParser.JOIN, 0)
        def relation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.RelationContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.RelationContext,i)

        def ON(self):
            return self.getToken(IceSqlParser.ON, 0)
        def USING(self):
            return self.getToken(IceSqlParser.USING, 0)
        def joinType(self):
            return self.getTypedRuleContext(IceSqlParser.JoinTypeContext,0)

        def booleanExpression(self):
            return self.getTypedRuleContext(IceSqlParser.BooleanExpressionContext,0)

        def identifierList(self):
            return self.getTypedRuleContext(IceSqlParser.IdentifierListContext,0)


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


    class PivotRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.func = None # QualifiedNameContext
            self.pc = None # IdentifierContext
            self.vc = None # IdentifierContext
            self.copyFrom(ctx)

        def relation(self):
            return self.getTypedRuleContext(IceSqlParser.RelationContext,0)

        def PIVOT(self):
            return self.getToken(IceSqlParser.PIVOT, 0)
        def FOR(self):
            return self.getToken(IceSqlParser.FOR, 0)
        def IN(self):
            return self.getToken(IceSqlParser.IN, 0)
        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.IdentifierContext,i)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPivotRelation" ):
                listener.enterPivotRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPivotRelation" ):
                listener.exitPivotRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPivotRelation" ):
                return visitor.visitPivotRelation(self)
            else:
                return visitor.visitChildren(self)


    class SelectRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def select(self):
            return self.getTypedRuleContext(IceSqlParser.SelectContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectRelation" ):
                listener.enterSelectRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectRelation" ):
                listener.exitSelectRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectRelation" ):
                return visitor.visitSelectRelation(self)
            else:
                return visitor.visitChildren(self)


    class TableRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def qualifiedName(self):
            return self.getTypedRuleContext(IceSqlParser.QualifiedNameContext,0)


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


    class ParenRelationContext(RelationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.RelationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relation(self):
            return self.getTypedRuleContext(IceSqlParser.RelationContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenRelation" ):
                listener.enterParenRelation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenRelation" ):
                listener.exitParenRelation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenRelation" ):
                return visitor.visitParenRelation(self)
            else:
                return visitor.visitChildren(self)



    def relation(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = IceSqlParser.RelationContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 64
        self.enterRecursionRule(localctx, 64, self.RULE_relation, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 694
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,87,self._ctx)
            if la_ == 1:
                localctx = IceSqlParser.LateralRelationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 681
                self.match(IceSqlParser.LATERAL)
                self.state = 682
                self.relation(7)
                pass

            elif la_ == 2:
                localctx = IceSqlParser.FunctionCallRelationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 683
                self.functionCall()
                pass

            elif la_ == 3:
                localctx = IceSqlParser.SelectRelationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 684
                self.match(IceSqlParser.T__0)
                self.state = 685
                self.select()
                self.state = 686
                self.match(IceSqlParser.T__2)
                pass

            elif la_ == 4:
                localctx = IceSqlParser.ParenRelationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 688
                self.match(IceSqlParser.T__0)
                self.state = 689
                self.relation(0)
                self.state = 690
                self.match(IceSqlParser.T__2)
                pass

            elif la_ == 5:
                localctx = IceSqlParser.JinjaRelationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 692
                self.match(IceSqlParser.JINJA)
                pass

            elif la_ == 6:
                localctx = IceSqlParser.TableRelationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 693
                self.qualifiedName()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 764
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,97,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 762
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,96,self._ctx)
                    if la_ == 1:
                        localctx = IceSqlParser.JoinRelationContext(self, IceSqlParser.RelationContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relation)
                        self.state = 696
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 698
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if ((((_la - 34)) & ~0x3f) == 0 and ((1 << (_la - 34)) & ((1 << (IceSqlParser.CROSS - 34)) | (1 << (IceSqlParser.FULL - 34)) | (1 << (IceSqlParser.INNER - 34)) | (1 << (IceSqlParser.LEFT - 34)) | (1 << (IceSqlParser.NATURAL - 34)) | (1 << (IceSqlParser.RIGHT - 34)))) != 0):
                            self.state = 697
                            localctx.ty = self.joinType()


                        self.state = 700
                        self.match(IceSqlParser.JOIN)
                        self.state = 701
                        localctx.right = self.relation(0)
                        self.state = 704
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,89,self._ctx)
                        if la_ == 1:
                            self.state = 702
                            self.match(IceSqlParser.ON)
                            self.state = 703
                            localctx.cond = self.booleanExpression(0)


                        self.state = 711
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,90,self._ctx)
                        if la_ == 1:
                            self.state = 706
                            self.match(IceSqlParser.USING)
                            self.state = 707
                            self.match(IceSqlParser.T__0)
                            self.state = 708
                            localctx.using = self.identifierList()
                            self.state = 709
                            self.match(IceSqlParser.T__2)


                        pass

                    elif la_ == 2:
                        localctx = IceSqlParser.PivotRelationContext(self, IceSqlParser.RelationContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relation)
                        self.state = 713
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 714
                        self.match(IceSqlParser.PIVOT)
                        self.state = 715
                        self.match(IceSqlParser.T__0)
                        self.state = 716
                        localctx.func = self.qualifiedName()
                        self.state = 717
                        self.match(IceSqlParser.T__0)
                        self.state = 718
                        localctx.pc = self.identifier()
                        self.state = 719
                        self.match(IceSqlParser.T__2)
                        self.state = 720
                        self.match(IceSqlParser.FOR)
                        self.state = 721
                        localctx.vc = self.identifier()
                        self.state = 722
                        self.match(IceSqlParser.IN)
                        self.state = 723
                        self.match(IceSqlParser.T__0)
                        self.state = 732
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,92,self._ctx)
                        if la_ == 1:
                            self.state = 724
                            self.expression()
                            self.state = 729
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            while _la==IceSqlParser.T__1:
                                self.state = 725
                                self.match(IceSqlParser.T__1)
                                self.state = 726
                                self.expression()
                                self.state = 731
                                self._errHandler.sync(self)
                                _la = self._input.LA(1)



                        self.state = 734
                        self.match(IceSqlParser.T__2)
                        self.state = 735
                        self.match(IceSqlParser.T__2)
                        pass

                    elif la_ == 3:
                        localctx = IceSqlParser.UnpivotRelationContext(self, IceSqlParser.RelationContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relation)
                        self.state = 737
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 738
                        self.match(IceSqlParser.UNPIVOT)
                        self.state = 739
                        self.match(IceSqlParser.T__0)
                        self.state = 740
                        localctx.vc = self.identifier()
                        self.state = 741
                        self.match(IceSqlParser.FOR)
                        self.state = 742
                        localctx.nc = self.identifier()
                        self.state = 743
                        self.match(IceSqlParser.IN)
                        self.state = 744
                        self.match(IceSqlParser.T__0)
                        self.state = 746
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << IceSqlParser.CASE) | (1 << IceSqlParser.DATE) | (1 << IceSqlParser.DAY) | (1 << IceSqlParser.EXTRACT) | (1 << IceSqlParser.FIRST) | (1 << IceSqlParser.GROUPING) | (1 << IceSqlParser.HOUR) | (1 << IceSqlParser.ILIKE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (IceSqlParser.LAST - 68)) | (1 << (IceSqlParser.LEFT - 68)) | (1 << (IceSqlParser.LIKE - 68)) | (1 << (IceSqlParser.MINUTE - 68)) | (1 << (IceSqlParser.MONTH - 68)) | (1 << (IceSqlParser.OUTER - 68)) | (1 << (IceSqlParser.RANGE - 68)) | (1 << (IceSqlParser.REPLACE - 68)) | (1 << (IceSqlParser.RIGHT - 68)) | (1 << (IceSqlParser.RLIKE - 68)) | (1 << (IceSqlParser.SECOND - 68)) | (1 << (IceSqlParser.YEAR - 68)) | (1 << (IceSqlParser.IDENTIFIER - 68)) | (1 << (IceSqlParser.QUOTED_IDENTIFIER - 68)))) != 0):
                            self.state = 745
                            self.identifierList()


                        self.state = 748
                        self.match(IceSqlParser.T__2)
                        self.state = 749
                        self.match(IceSqlParser.T__2)
                        pass

                    elif la_ == 4:
                        localctx = IceSqlParser.AliasedRelationContext(self, IceSqlParser.RelationContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relation)
                        self.state = 751
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 753
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==IceSqlParser.AS:
                            self.state = 752
                            self.match(IceSqlParser.AS)


                        self.state = 755
                        self.identifier()
                        self.state = 760
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,95,self._ctx)
                        if la_ == 1:
                            self.state = 756
                            self.match(IceSqlParser.T__0)
                            self.state = 757
                            self.identifierList()
                            self.state = 758
                            self.match(IceSqlParser.T__2)


                        pass

             
                self.state = 766
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,97,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class GroupingContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return IceSqlParser.RULE_grouping

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SetsGroupingContext(GroupingContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.GroupingContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def GROUPING(self):
            return self.getToken(IceSqlParser.GROUPING, 0)
        def SETS(self):
            return self.getToken(IceSqlParser.SETS, 0)
        def groupingSet(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.GroupingSetContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.GroupingSetContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetsGrouping" ):
                listener.enterSetsGrouping(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetsGrouping" ):
                listener.exitSetsGrouping(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetsGrouping" ):
                return visitor.visitSetsGrouping(self)
            else:
                return visitor.visitChildren(self)


    class FlatGroupingContext(GroupingContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.GroupingContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFlatGrouping" ):
                listener.enterFlatGrouping(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFlatGrouping" ):
                listener.exitFlatGrouping(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFlatGrouping" ):
                return visitor.visitFlatGrouping(self)
            else:
                return visitor.visitChildren(self)



    def grouping(self):

        localctx = IceSqlParser.GroupingContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_grouping)
        self._la = 0 # Token type
        try:
            self.state = 788
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,100,self._ctx)
            if la_ == 1:
                localctx = IceSqlParser.FlatGroupingContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 767
                self.expression()
                self.state = 772
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 768
                    self.match(IceSqlParser.T__1)
                    self.state = 769
                    self.expression()
                    self.state = 774
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass

            elif la_ == 2:
                localctx = IceSqlParser.SetsGroupingContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 775
                self.match(IceSqlParser.GROUPING)
                self.state = 776
                self.match(IceSqlParser.SETS)
                self.state = 777
                self.match(IceSqlParser.T__0)
                self.state = 778
                self.groupingSet()
                self.state = 783
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==IceSqlParser.T__1:
                    self.state = 779
                    self.match(IceSqlParser.T__1)
                    self.state = 780
                    self.groupingSet()
                    self.state = 785
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 786
                self.match(IceSqlParser.T__2)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroupingSetContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.ExpressionContext,i)


        def getRuleIndex(self):
            return IceSqlParser.RULE_groupingSet

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroupingSet" ):
                listener.enterGroupingSet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroupingSet" ):
                listener.exitGroupingSet(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroupingSet" ):
                return visitor.visitGroupingSet(self)
            else:
                return visitor.visitChildren(self)




    def groupingSet(self):

        localctx = IceSqlParser.GroupingSetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_groupingSet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 790
            self.match(IceSqlParser.T__0)
            self.state = 791
            self.expression()
            self.state = 796
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==IceSqlParser.T__1:
                self.state = 792
                self.match(IceSqlParser.T__1)
                self.state = 793
                self.expression()
                self.state = 798
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 799
            self.match(IceSqlParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QualifiedNameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.IdentifierContext,i)


        def getRuleIndex(self):
            return IceSqlParser.RULE_qualifiedName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQualifiedName" ):
                listener.enterQualifiedName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQualifiedName" ):
                listener.exitQualifiedName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQualifiedName" ):
                return visitor.visitQualifiedName(self)
            else:
                return visitor.visitChildren(self)




    def qualifiedName(self):

        localctx = IceSqlParser.QualifiedNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_qualifiedName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 801
            self.identifier()
            self.state = 806
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,102,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 802
                    self.match(IceSqlParser.T__4)
                    self.state = 803
                    self.identifier() 
                self.state = 808
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,102,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifierListContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IceSqlParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(IceSqlParser.IdentifierContext,i)


        def getRuleIndex(self):
            return IceSqlParser.RULE_identifierList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifierList" ):
                listener.enterIdentifierList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifierList" ):
                listener.exitIdentifierList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifierList" ):
                return visitor.visitIdentifierList(self)
            else:
                return visitor.visitChildren(self)




    def identifierList(self):

        localctx = IceSqlParser.IdentifierListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_identifierList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 809
            self.identifier()
            self.state = 814
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==IceSqlParser.T__1:
                self.state = 810
                self.match(IceSqlParser.T__1)
                self.state = 811
                self.identifier()
                self.state = 816
                self._errHandler.sync(self)
                _la = self._input.LA(1)

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

        def unquotedIdentifier(self):
            return self.getTypedRuleContext(IceSqlParser.UnquotedIdentifierContext,0)


        def quotedIdentifier(self):
            return self.getTypedRuleContext(IceSqlParser.QuotedIdentifierContext,0)


        def getRuleIndex(self):
            return IceSqlParser.RULE_identifier

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

        localctx = IceSqlParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_identifier)
        try:
            self.state = 819
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [IceSqlParser.CASE, IceSqlParser.DATE, IceSqlParser.DAY, IceSqlParser.EXTRACT, IceSqlParser.FIRST, IceSqlParser.GROUPING, IceSqlParser.HOUR, IceSqlParser.ILIKE, IceSqlParser.LAST, IceSqlParser.LEFT, IceSqlParser.LIKE, IceSqlParser.MINUTE, IceSqlParser.MONTH, IceSqlParser.OUTER, IceSqlParser.RANGE, IceSqlParser.REPLACE, IceSqlParser.RIGHT, IceSqlParser.RLIKE, IceSqlParser.SECOND, IceSqlParser.YEAR, IceSqlParser.IDENTIFIER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 817
                self.unquotedIdentifier()
                pass
            elif token in [IceSqlParser.QUOTED_IDENTIFIER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 818
                self.quotedIdentifier()
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


    class QuotedIdentifierContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTED_IDENTIFIER(self):
            return self.getToken(IceSqlParser.QUOTED_IDENTIFIER, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_quotedIdentifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuotedIdentifier" ):
                listener.enterQuotedIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuotedIdentifier" ):
                listener.exitQuotedIdentifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuotedIdentifier" ):
                return visitor.visitQuotedIdentifier(self)
            else:
                return visitor.visitChildren(self)




    def quotedIdentifier(self):

        localctx = IceSqlParser.QuotedIdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_quotedIdentifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 821
            self.match(IceSqlParser.QUOTED_IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(IceSqlParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_var

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar" ):
                listener.enterVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar" ):
                listener.exitVar(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVar" ):
                return visitor.visitVar(self)
            else:
                return visitor.visitChildren(self)




    def var(self):

        localctx = IceSqlParser.VarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_var)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 823
            self.match(IceSqlParser.T__10)
            self.state = 824
            self.match(IceSqlParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(IceSqlParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam" ):
                listener.enterParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam" ):
                listener.exitParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = IceSqlParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 826
            self.match(IceSqlParser.T__5)
            self.state = 827
            self.match(IceSqlParser.IDENTIFIER)
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


        def getRuleIndex(self):
            return IceSqlParser.RULE_number

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DecimalNumberContext(NumberContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.NumberContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DECIMAL_VALUE(self):
            return self.getToken(IceSqlParser.DECIMAL_VALUE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecimalNumber" ):
                listener.enterDecimalNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecimalNumber" ):
                listener.exitDecimalNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDecimalNumber" ):
                return visitor.visitDecimalNumber(self)
            else:
                return visitor.visitChildren(self)


    class IntegerNumberContext(NumberContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.NumberContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def integer(self):
            return self.getTypedRuleContext(IceSqlParser.IntegerContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntegerNumber" ):
                listener.enterIntegerNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntegerNumber" ):
                listener.exitIntegerNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntegerNumber" ):
                return visitor.visitIntegerNumber(self)
            else:
                return visitor.visitChildren(self)


    class FloatNumberContext(NumberContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a IceSqlParser.NumberContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT_VALUE(self):
            return self.getToken(IceSqlParser.FLOAT_VALUE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloatNumber" ):
                listener.enterFloatNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloatNumber" ):
                listener.exitFloatNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloatNumber" ):
                return visitor.visitFloatNumber(self)
            else:
                return visitor.visitChildren(self)



    def number(self):

        localctx = IceSqlParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_number)
        try:
            self.state = 832
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [IceSqlParser.INTEGER_VALUE]:
                localctx = IceSqlParser.IntegerNumberContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 829
                self.integer()
                pass
            elif token in [IceSqlParser.DECIMAL_VALUE]:
                localctx = IceSqlParser.DecimalNumberContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 830
                self.match(IceSqlParser.DECIMAL_VALUE)
                pass
            elif token in [IceSqlParser.FLOAT_VALUE]:
                localctx = IceSqlParser.FloatNumberContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 831
                self.match(IceSqlParser.FLOAT_VALUE)
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


    class IntegerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER_VALUE(self):
            return self.getToken(IceSqlParser.INTEGER_VALUE, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_integer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInteger" ):
                listener.enterInteger(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInteger" ):
                listener.exitInteger(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInteger" ):
                return visitor.visitInteger(self)
            else:
                return visitor.visitChildren(self)




    def integer(self):

        localctx = IceSqlParser.IntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_integer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 834
            self.match(IceSqlParser.INTEGER_VALUE)
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
            return self.getToken(IceSqlParser.STRING, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_string

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

        localctx = IceSqlParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 836
            self.match(IceSqlParser.STRING)
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
            return self.getToken(IceSqlParser.NULL, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_null

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

        localctx = IceSqlParser.NullContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_null)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 838
            self.match(IceSqlParser.NULL)
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
            return self.getToken(IceSqlParser.TRUE, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_true

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

        localctx = IceSqlParser.TrueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_true)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 840
            self.match(IceSqlParser.TRUE)
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
            return self.getToken(IceSqlParser.FALSE, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_false

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

        localctx = IceSqlParser.FalseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_false)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 842
            self.match(IceSqlParser.FALSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetQuantifierContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DISTINCT(self):
            return self.getToken(IceSqlParser.DISTINCT, 0)

        def ALL(self):
            return self.getToken(IceSqlParser.ALL, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_setQuantifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetQuantifier" ):
                listener.enterSetQuantifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetQuantifier" ):
                listener.exitSetQuantifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetQuantifier" ):
                return visitor.visitSetQuantifier(self)
            else:
                return visitor.visitChildren(self)




    def setQuantifier(self):

        localctx = IceSqlParser.SetQuantifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_setQuantifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 844
            _la = self._input.LA(1)
            if not(_la==IceSqlParser.ALL or _la==IceSqlParser.DISTINCT):
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


    class JoinTypeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INNER(self):
            return self.getToken(IceSqlParser.INNER, 0)

        def LEFT(self):
            return self.getToken(IceSqlParser.LEFT, 0)

        def OUTER(self):
            return self.getToken(IceSqlParser.OUTER, 0)

        def RIGHT(self):
            return self.getToken(IceSqlParser.RIGHT, 0)

        def FULL(self):
            return self.getToken(IceSqlParser.FULL, 0)

        def CROSS(self):
            return self.getToken(IceSqlParser.CROSS, 0)

        def NATURAL(self):
            return self.getToken(IceSqlParser.NATURAL, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_joinType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJoinType" ):
                listener.enterJoinType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJoinType" ):
                listener.exitJoinType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJoinType" ):
                return visitor.visitJoinType(self)
            else:
                return visitor.visitChildren(self)




    def joinType(self):

        localctx = IceSqlParser.JoinTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_joinType)
        try:
            self.state = 858
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,106,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 846
                self.match(IceSqlParser.INNER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 847
                self.match(IceSqlParser.LEFT)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 848
                self.match(IceSqlParser.LEFT)
                self.state = 849
                self.match(IceSqlParser.OUTER)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 850
                self.match(IceSqlParser.RIGHT)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 851
                self.match(IceSqlParser.RIGHT)
                self.state = 852
                self.match(IceSqlParser.OUTER)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 853
                self.match(IceSqlParser.FULL)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 854
                self.match(IceSqlParser.FULL)
                self.state = 855
                self.match(IceSqlParser.OUTER)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 856
                self.match(IceSqlParser.CROSS)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 857
                self.match(IceSqlParser.NATURAL)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CmpOpContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return IceSqlParser.RULE_cmpOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCmpOp" ):
                listener.enterCmpOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCmpOp" ):
                listener.exitCmpOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCmpOp" ):
                return visitor.visitCmpOp(self)
            else:
                return visitor.visitChildren(self)




    def cmpOp(self):

        localctx = IceSqlParser.CmpOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_cmpOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 860
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << IceSqlParser.T__11) | (1 << IceSqlParser.T__12) | (1 << IceSqlParser.T__13) | (1 << IceSqlParser.T__14) | (1 << IceSqlParser.T__15) | (1 << IceSqlParser.T__16) | (1 << IceSqlParser.T__17))) != 0)):
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


    class ArithOpContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return IceSqlParser.RULE_arithOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithOp" ):
                listener.enterArithOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithOp" ):
                listener.exitArithOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArithOp" ):
                return visitor.visitArithOp(self)
            else:
                return visitor.visitChildren(self)




    def arithOp(self):

        localctx = IceSqlParser.ArithOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_arithOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 862
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << IceSqlParser.T__3) | (1 << IceSqlParser.T__18) | (1 << IceSqlParser.T__19) | (1 << IceSqlParser.T__20) | (1 << IceSqlParser.T__21) | (1 << IceSqlParser.T__22))) != 0)):
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


    class UnaryOpContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return IceSqlParser.RULE_unaryOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryOp" ):
                listener.enterUnaryOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryOp" ):
                listener.exitUnaryOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryOp" ):
                return visitor.visitUnaryOp(self)
            else:
                return visitor.visitChildren(self)




    def unaryOp(self):

        localctx = IceSqlParser.UnaryOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_unaryOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 864
            _la = self._input.LA(1)
            if not(_la==IceSqlParser.T__18 or _la==IceSqlParser.T__19):
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


    class UnquotedIdentifierContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(IceSqlParser.IDENTIFIER, 0)

        def CASE(self):
            return self.getToken(IceSqlParser.CASE, 0)

        def DATE(self):
            return self.getToken(IceSqlParser.DATE, 0)

        def DAY(self):
            return self.getToken(IceSqlParser.DAY, 0)

        def EXTRACT(self):
            return self.getToken(IceSqlParser.EXTRACT, 0)

        def FIRST(self):
            return self.getToken(IceSqlParser.FIRST, 0)

        def GROUPING(self):
            return self.getToken(IceSqlParser.GROUPING, 0)

        def HOUR(self):
            return self.getToken(IceSqlParser.HOUR, 0)

        def ILIKE(self):
            return self.getToken(IceSqlParser.ILIKE, 0)

        def LAST(self):
            return self.getToken(IceSqlParser.LAST, 0)

        def LEFT(self):
            return self.getToken(IceSqlParser.LEFT, 0)

        def LIKE(self):
            return self.getToken(IceSqlParser.LIKE, 0)

        def MINUTE(self):
            return self.getToken(IceSqlParser.MINUTE, 0)

        def MONTH(self):
            return self.getToken(IceSqlParser.MONTH, 0)

        def OUTER(self):
            return self.getToken(IceSqlParser.OUTER, 0)

        def RANGE(self):
            return self.getToken(IceSqlParser.RANGE, 0)

        def REPLACE(self):
            return self.getToken(IceSqlParser.REPLACE, 0)

        def RIGHT(self):
            return self.getToken(IceSqlParser.RIGHT, 0)

        def RLIKE(self):
            return self.getToken(IceSqlParser.RLIKE, 0)

        def SECOND(self):
            return self.getToken(IceSqlParser.SECOND, 0)

        def YEAR(self):
            return self.getToken(IceSqlParser.YEAR, 0)

        def getRuleIndex(self):
            return IceSqlParser.RULE_unquotedIdentifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnquotedIdentifier" ):
                listener.enterUnquotedIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnquotedIdentifier" ):
                listener.exitUnquotedIdentifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnquotedIdentifier" ):
                return visitor.visitUnquotedIdentifier(self)
            else:
                return visitor.visitChildren(self)




    def unquotedIdentifier(self):

        localctx = IceSqlParser.UnquotedIdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_unquotedIdentifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 866
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << IceSqlParser.CASE) | (1 << IceSqlParser.DATE) | (1 << IceSqlParser.DAY) | (1 << IceSqlParser.EXTRACT) | (1 << IceSqlParser.FIRST) | (1 << IceSqlParser.GROUPING) | (1 << IceSqlParser.HOUR) | (1 << IceSqlParser.ILIKE))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (IceSqlParser.LAST - 68)) | (1 << (IceSqlParser.LEFT - 68)) | (1 << (IceSqlParser.LIKE - 68)) | (1 << (IceSqlParser.MINUTE - 68)) | (1 << (IceSqlParser.MONTH - 68)) | (1 << (IceSqlParser.OUTER - 68)) | (1 << (IceSqlParser.RANGE - 68)) | (1 << (IceSqlParser.REPLACE - 68)) | (1 << (IceSqlParser.RIGHT - 68)) | (1 << (IceSqlParser.RLIKE - 68)) | (1 << (IceSqlParser.SECOND - 68)) | (1 << (IceSqlParser.YEAR - 68)) | (1 << (IceSqlParser.IDENTIFIER - 68)))) != 0)):
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



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[17] = self.booleanExpression_sempred
        self._predicates[19] = self.valueExpression_sempred
        self._predicates[21] = self.primaryExpression_sempred
        self._predicates[32] = self.relation_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def booleanExpression_sempred(self, localctx:BooleanExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def valueExpression_sempred(self, localctx:ValueExpressionContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 1)
         

    def primaryExpression_sempred(self, localctx:PrimaryExpressionContext, predIndex:int):
            if predIndex == 4:
                return  not self.config.interval_units 
         

            if predIndex == 5:
                return  self.config.interval_units 
         

    def relation_sempred(self, localctx:RelationContext, predIndex:int):
            if predIndex == 6:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 2)
