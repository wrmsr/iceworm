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
    : primaryExpression
    | NOT booleanExpression
    | booleanExpression (AND | OR) booleanExpression
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
    : identifier
    ;

identifier
    : IDENTIFIER
    ;

number
    : INTEGER_VALUE
    ;

AND: 'and';
AS: 'as';
FROM: 'from';
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
