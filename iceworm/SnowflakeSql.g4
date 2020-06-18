grammar SnowflakeSql;


singleStatement
    : selectStatement ';' EOF
    ;

selectStatement
    : SELECT selectItem (',' selectItem)*
      (FROM relation (',' relation)*)?
      (WHERE where=booleanExpression)?
      (GROUP BY groupBy)?
    ;

selectItem
    : '*'                           #allSelectItem
    | expression (AS? identifier)?  #expressionSelectItem
    ;

expression
    : booleanExpression
    ;

booleanExpression
    : valueExpression predicate[$valueExpression.ctx]?   #predicatedBooleanExpression
    | op=NOT booleanExpression                           #unaryBooleanExpression
    | booleanExpression op=(AND | OR) booleanExpression  #binaryBooleanExpression
    ;

predicate[ParserRuleContext value]
    : cmpOp right=valueExpression                   #cmpPredicate
    | NOT? IN '(' expression (',' expression)* ')'  #inListPredicate
    | IS NOT? NULL                                  #isNullPredicate
    ;

valueExpression
    : primaryExpression                                      #primaryValueExpression
    | op=unaryOp valueExpression                             #unaryValueExpression
    | left=valueExpression op=arithOp right=valueExpression  #arithValueExpression
    ;

primaryExpression
    : identifier '(' (expression (',' expression*))? ')'  #functionCallPrimaryExpression
    | simpleExpression                                    #simplePrimaryExpression
    ;

simpleExpression
    : '(' expression ')'
    | identifier
    | number
    | string
    | null
    ;

relation
    : left=relation ty=joinType? JOIN right=relation (ON condition=booleanExpression)?  #joinRelation
    | '(' relation ')'                                                                  #parenRelation
    | identifier                                                                        #tableRelation
    ;

groupBy
    : expression (',' expression)*
    ;

identifier
    : IDENTIFIER         #unquotedIdentifier
    | QUOTED_IDENTIFIER  #quotedIdentifier
    ;

number
    : INTEGER_VALUE  #integerNumber
    ;

string
    : STRING
    ;

null
    : NULL
    ;

joinType
    : INNER
    | LEFT
    | LEFT OUTER
    | RIGHT
    | RIGHT OUTER
    | FULL
    | FULL OUTER
    | CROSS
    | NATURAL
    ;

cmpOp
    : '='
    | '!='
    | '<>'
    | '<'
    | '<='
    | '>'
    | '>='
    ;

arithOp
    : '+'
    | '-'
    | '*'
    | '/'
    | '%'
    ;

unaryOp
    : '+'
    | '-'
    ;

AND: 'and';
AS: 'as';
BY: 'by';
CROSS: 'cross';
FROM: 'from';
FULL: 'full';
GROUP: 'group';
IN: 'in';
INNER: 'inner';
IS: 'is';
JOIN: 'join';
LEFT: 'left';
NATURAL: 'natural';
NOT: 'not';
NULL: 'null';
ON: 'on';
OR: 'or';
OUTER: 'outer';
RIGHT: 'right';
SELECT: 'select';
WHERE: 'where';

STRING
    : '\'' (~'\'' | '\'\'')* '\''
    ;

INTEGER_VALUE
    : DIGIT+
    ;

IDENTIFIER
    : (LETTER | '_') (LETTER | DIGIT | '_' | '@' | ':')*
    ;

QUOTED_IDENTIFIER
    : '"' (~'"' | '""')* '"'
    ;

fragment DIGIT
    : [0-9]
    ;

fragment LETTER
    : [A-Za-z]
    ;

COMMENT
    : '--' ~[\r\n]* '\r'? '\n'? -> channel(HIDDEN)
    ;

WS
    : [ \t\n\r]+ -> skip
    ;
