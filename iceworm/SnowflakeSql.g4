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
    | null
    ;

functionCall
    : identifier '(' (expression (',' expression*))? ')'
    ;

relation
    : left=relation JOIN right=relation (ON condition=booleanExpression)?  #joinRelation
    | identifier                                                           #tableRelation
    ;

groupBy
    : expression (',' expression)*
    ;

identifier
    : IDENTIFIER
    ;

number
    : INTEGER_VALUE  #integerNumber
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
