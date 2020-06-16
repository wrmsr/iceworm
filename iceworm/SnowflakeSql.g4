grammar SnowflakeSql;


singleStatement
    : selectStatement ';' EOF
    ;

selectStatement
    : SELECT selectItem (',' selectItem)*
      (FROM relation (',' relation)*)?
    ;

selectItem
    : expression
    ;

expression
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

SELECT: 'select';
FROM: 'from';

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
