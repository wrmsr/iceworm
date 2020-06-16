grammar SnowflakeSql;


singleStatement
    : selectStatement ';' EOF
    ;

selectStatement
    : SELECT selectItem (',' selectItem)*
      (FROM relation (',' relation)*)?
    ;

selectItem
    : expression (AS? identifier)?
    ;

expression
    : booleanExpression
    ;

booleanExpression
    : primaryExpression                                  #primaryBooleanExpression
    | op=NOT booleanExpression                           #unaryBooleanExpression
    | booleanExpression op=(AND | OR) booleanExpression  #binaryBooleanExpression
    ;

primaryExpression
    : identifier
    | number
    | functionCall
    ;

functionCall
    : identifier '(' (expression (',' expression*))? ')'
    ;

relation
    : left=relation JOIN right=relation  #joinRelation
    | identifier                         #tableRelation
    ;

identifier
    : IDENTIFIER
    ;

number
    : INTEGER_VALUE  #integerNumber
    ;

AND: 'and';
AS: 'as';
FROM: 'from';
JOIN: 'join';
NOT: 'not';
OR: 'or';
SELECT: 'select';

INTEGER_VALUE
    : DIGIT+
    ;

IDENTIFIER
    : (LETTER | '_') (LETTER | DIGIT | '_' | '@' | ':')*
    ;

fragment DIGIT
    : [0-9]
    ;

fragment LETTER
    : [A-Za-z]
    ;

WS
    : [ \t\n\r]+ -> skip
    ;
