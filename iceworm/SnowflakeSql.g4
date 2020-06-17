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
    : '(' expression ')'                                 #parenBooleanExpression
    | primaryExpression                                  #primaryBooleanExpression
    | op=NOT booleanExpression                           #unaryBooleanExpression
    | booleanExpression op=(AND | OR) booleanExpression  #binaryBooleanExpression
    ;

primaryExpression
    : identifier
    | number
    | string
    | functionCall
    | null
    ;

functionCall
    : identifier '(' (expression (',' expression*))? ')'
    ;

relation
    : left=relation JOIN right=relation (ON condition=booleanExpression)?  #joinRelation
    | '(' relation ')'                                                     #parenRelation
    | identifier                                                           #tableRelation
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

AND: 'and';
AS: 'as';
BY: 'by';
FROM: 'from';
GROUP: 'group';
JOIN: 'join';
NOT: 'not';
NULL: 'null';
ON: 'on';
OR: 'or';
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
