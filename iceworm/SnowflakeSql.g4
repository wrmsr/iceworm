grammar SnowflakeSql;

singleStatement
    : selectStatement ';' EOF
    ;

selectStatement
    : SELECT selectItem (',' selectItem)* (FROM tableClause)?
    ;

selectItem
    : expression
    ;

expression
    : identifier
    | integer
    ;

tableClause
    : identifier
    ;

identifier
    : IDENTIFIER
    ;

integer
    : INTEGER
    ;

SELECT: 'select';
FROM: 'from';

IDENTIFIER: [A-Za-z_][A-Za-z_0-9]*;

INTEGER: [0-9]+;

WS: [ \t\n\r]+ -> skip;
