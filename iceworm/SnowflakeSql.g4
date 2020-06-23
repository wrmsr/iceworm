grammar SnowflakeSql;


singleStatement
    : select ';' EOF
    ;

select
    : cteSelect
    ;

cteSelect
    : (WITH cte (',' cte)*)? unionSelect
    ;

cte
    : identifier AS '(' select ')'
    ;

unionSelect
    : primarySelect unionItem*
    ;

unionItem
    : UNION setQuantifier? primarySelect
    ;

primarySelect
    : SELECT setQuantifier? selectItem (',' selectItem)*
      (FROM relation (',' relation)*)?
      (WHERE where=booleanExpression)?
      (GROUP BY groupBy)?
      (ORDER BY sortItem (',' sortItem)*)?
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
    | booleanExpression '::' identifier                  #castBooleanExpression
    ;

predicate[ParserRuleContext value]
    : cmpOp right=valueExpression                   #cmpPredicate
    | IS NOT? NULL                                  #isNullPredicate
    | NOT? IN '(' expression (',' expression)* ')'  #inListPredicate
    | NOT? IN '(' select ')'                        #inSelectPredicate
    | NOT? IN JINJA                                 #inJinjaPredicate
    | NOT? LIKE expression                          #likePredicate
    ;

valueExpression
    : primaryExpression                                      #primaryValueExpression
    | op=unaryOp valueExpression                             #unaryValueExpression
    | left=valueExpression op=arithOp right=valueExpression  #arithValueExpression
    ;

primaryExpression
    : identifier '(' (expression (',' expression)*)? ')' over?  #functionCallExpression
    | CASE caseItem* (ELSE expression)? END                     #caseExpression
    | '(' select ')'                                            #selectExpression
    | '(' expression ')'                                        #parenExpression
    | JINJA                                                     #jinjaExpression
    | simpleExpression                                          #simplePrimaryExpression
    ;

simpleExpression
    : qualifiedName
    | number
    | string
    | null
    | true
    | false
    ;

caseItem
    : WHEN expression THEN expression
    ;

over
    : OVER '(' (ORDER BY sortItem (',' sortItem)*)? ')'
    ;

sortItem
    : expression direction=(ASC | DESC)?
    ;

relation
    : relation AS? identifier                                                      #aliasedRelation
    | left=relation ty=joinType? JOIN right=relation (ON cond=booleanExpression)?  #joinRelation
    | '(' select ')'                                                               #selectRelation
    | '(' relation ')'                                                             #parenRelation
    | JINJA                                                                        #jinjaRelation
    | qualifiedName                                                                #tableRelation
    ;

groupBy
    : expression (',' expression)*
    ;

qualifiedName
    : identifier ('.' identifier)*
    ;

identifier
    : unquotedIdentifier
    | quotedIdentifier
    ;

quotedIdentifier
    : QUOTED_IDENTIFIER
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

true
    : TRUE
    ;

false
    : FALSE
    ;

setQuantifier
    : DISTINCT
    | ALL
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
    | '||'
    ;

unaryOp
    : '+'
    | '-'
    ;

unquotedIdentifier
    : IDENTIFIER

    | LEFT
    | RIGHT

    ;

ALL: 'all';
AND: 'and';
AS: 'as';
ASC: 'asc';
BY: 'by';
CASE: 'case';
CROSS: 'cross';
DESC: 'desc';
DISTINCT: 'distinct';
ELSE: 'else';
END: 'end';
FALSE: 'false';
FROM: 'from';
FULL: 'full';
GROUP: 'group';
IN: 'in';
INNER: 'inner';
IS: 'is';
JOIN: 'join';
LEFT: 'left';
LIKE: 'like';
NATURAL: 'natural';
NOT: 'not';
NULL: 'null';
ON: 'on';
OR: 'or';
ORDER: 'order';
OUTER: 'outer';
OVER: 'over';
RIGHT: 'right';
SELECT: 'select';
THEN: 'then';
TRUE: 'true';
UNION: 'union';
WHEN: 'when';
WHERE: 'where';
WITH: 'with';

STRING
    : '\'' (~'\'' | '\'\'')* '\''
    ;

INTEGER_VALUE
    : DIGIT+
    ;

IDENTIFIER
    : (LETTER | '_') (LETTER | DIGIT | '_' | '@' | ':' | '$')*
    ;

QUOTED_IDENTIFIER
    : '"' (~'"' | '""')* '"'
    ;

JINJA
    : '{{' .*? '}}'
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

BLOCK_COMMENT
    : '/*' .*? '*/' -> channel(HIDDEN)
    ;

WS
    : [ \t\n\r]+ -> skip
    ;
