grammar SnowflakeSql;


singleStatement
    : statement ';'? EOF
    ;

statement
    : select
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
    : SELECT topN? setQuantifier? selectItem (',' selectItem)*
      (FROM relation (',' relation)*)?
      (WHERE where=booleanExpression)?
      (GROUP BY groupBy)?
      (HAVING having=booleanExpression)?
      (QUALIFY qualify=booleanExpression)?
      (ORDER BY sortItem (',' sortItem)*)?
      (LIMIT INTEGER_VALUE)?
    ;

topN
    : TOP number
    ;

selectItem
    : '*'                           #allSelectItem
    | identifier '.' '*'            #identifierAllSelectItem
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
    : cmpOp right=valueExpression                                   #cmpPredicate
    | IS NOT? NULL                                                  #isNullPredicate
    | NOT? BETWEEN lower=valueExpression AND upper=valueExpression  #betweenPredicate
    | NOT? IN '(' expression (',' expression)* ')'                  #inListPredicate
    | NOT? IN '(' select ')'                                        #inSelectPredicate
    | NOT? IN JINJA                                                 #inJinjaPredicate
    | NOT? kind=(LIKE | ILIKE | RLIKE) ANY?
      (expression | ('(' expression (',' expression)* ')'))
      (ESCAPE esc=string)?                                          #likePredicate
    ;

valueExpression
    : primaryExpression                                      #primaryValueExpression
    | op=unaryOp valueExpression                             #unaryValueExpression
    | left=valueExpression op=arithOp right=valueExpression  #arithValueExpression
    | valueExpression ':' identifier                         #colonValueExpression
    | value=valueExpression '[' index=valueExpression ']'    #brackeetValueExpression
    | valueExpression '::' typeSpec                          #castValueExpression
    ;

primaryExpression
    : functionCall                                                     #functionCallExpression
    | LAST_VALUE '(' expression ((IGNORE | RESPECT) NULLS)? ')' over?  #lastValueExpression
    | CASE (val=expression)? caseItem* (ELSE default=expression)? END  #caseExpression
    | INTERVAL expression                                              #intervalExpression
    | '(' select ')'                                                   #selectExpression
    | '(' expression ')'                                               #parenExpression
    | CAST '(' expression AS typeSpec ')'                              #castCallExpression
    | JINJA                                                            #jinjaExpression
    | simpleExpression                                                 #simplePrimaryExpression
    ;

simpleExpression
    : qualifiedName
    | number
    | string
    | null
    | true
    | false
    ;

typeSpec
    : identifier ('(' (simpleExpression (',' simpleExpression)*)? ')')?
    ;

functionCall
    : qualifiedName '(' setQuantifier? (expression (',' expression)*)? ')'
      ((IGNORE | RESPECT) NULLS)?
      (WITHIN GROUP '(' ORDER BY sortItem (',' sortItem)* ')')?
      over?                                                                 #expressionFunctionCall
    | qualifiedName '(' kwarg (',' kwarg)* ')'
      ((IGNORE | RESPECT) NULLS)?
      (WITHIN GROUP '(' ORDER BY sortItem (',' sortItem)* ')')?
      over?                                                                 #kwargFunctionCall
    | qualifiedName '(' '*' ')'
      over?                                                                 #starFunctionCall
    ;

kwarg
    : identifier '=>' expression
    ;

caseItem
    : WHEN expression THEN expression
    ;

over
    : OVER '(' (PARTITION BY (expression (',' expression)*))? (ORDER BY sortItem (',' sortItem)*)? frame? ')'
    ;

cumulativeFrameMin
    : UNBOUNDED PRECEDING
    | CURRENT ROW
    ;

cumulativeFrameMax
    : UNBOUNDED FOLLOWING
    | CURRENT ROW
    ;

slidingFrameMin
    : INTEGER_VALUE (PRECEDING | FOLLOWING)
    | UNBOUNDED PRECEDING
    ;

slidingFrameMax
    : INTEGER_VALUE (PRECEDING | FOLLOWING)
    | UNBOUNDED FOLLOWING
    ;

frame
    : ROWS UNBOUNDED (PRECEDING | FOLLOWING)                            #unboundedFrame
    | (ROWS | RANGE) BETWEEN cumulativeFrameMin AND cumulativeFrameMax  #cumulativeFrame
    | ROWS BETWEEN slidingFrameMin AND slidingFrameMax                  #slidingFrame
    ;

sortItem
    : expression direction=(ASC | DESC)? (NULLS (FIRST | LAST))?
    ;

relation
    : relation AS? identifier ('(' identifierList ')')?                 #aliasedRelation
    | left=relation ty=joinType?
      JOIN right=relation
      (ON cond=booleanExpression)?
      (USING '(' using=identifierList ')')?                             #joinRelation
    | relation PIVOT '('
      func=qualifiedName '(' pc=identifier ')'
      FOR vc=identifier IN '(' (expression (',' expression)*)? ')' ')'  #pivotRelation
    | relation UNPIVOT '('
      vc=identifier
      FOR nc=identifier IN '(' identifierList? ')' ')'                  #unpivotRelation
    | LATERAL relation                                                  #lateralRelation
    | functionCall                                                      #functionCallRelation
    | '(' select ')'                                                    #selectRelation
    | '(' relation ')'                                                  #parenRelation
    | JINJA                                                             #jinjaRelation
    | qualifiedName                                                     #tableRelation
    ;

groupBy
    : expression (',' expression)*
    ;

qualifiedName
    : identifier ('.' identifier)*
    ;

identifierList
    : identifier (',' identifier)*
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
    | DECIMAL_VALUE  #decimalNumber
    | FLOAT_VALUE    #floatNumber
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

    | FIRST
    | LEFT
    | OUTER
    | RIGHT

    ;

ALL: 'all';
AND: 'and';
ANY: 'any';
AS: 'as';
ASC: 'asc';
BETWEEN: 'between';
BY: 'by';
CASE: 'case';
CAST: 'cast';
CROSS: 'cross';
CURRENT: 'current';
DESC: 'desc';
DISTINCT: 'distinct';
ELSE: 'else';
END: 'end';
ESCAPE: 'escape';
FALSE: 'false';
FIRST: 'first';
FOLLOWING: 'following';
FOR: 'for';
FROM: 'from';
FULL: 'full';
GROUP: 'group';
HAVING: 'having';
IGNORE: 'ignore';
ILIKE: 'ilike';
IN: 'in';
INNER: 'inner';
INTERVAL: 'interval';
IS: 'is';
JOIN: 'join';
LAST: 'last';
LAST_VALUE: 'last_value';
LATERAL: 'lateral';
LEFT: 'left';
LIKE: 'like';
LIMIT: 'limit';
NATURAL: 'natural';
NOT: 'not';
NULL: 'null';
NULLS: 'nulls';
ON: 'on';
OR: 'or';
ORDER: 'order';
OUTER: 'outer';
OVER: 'over';
PARTITION: 'partition';
PIVOT: 'pivot';
PRECEDING: 'preceding';
QUALIFY: 'qualify';
RANGE: 'range';
RESPECT: 'respect';
RIGHT: 'right';
RLIKE: 'rlike';
ROW: 'row';
ROWS: 'rows';
SELECT: 'select';
THEN: 'then';
TOP: 'top';
TRUE: 'true';
UNBOUNDED: 'unbounded';
UNION: 'union';
UNPIVOT: 'unpivot';
USING: 'using';
WHEN: 'when';
WHERE: 'where';
WITH: 'with';
WITHIN: 'within';

STRING
    : '\'' (~'\'' | '\'\'' | '\\\'')* '\''
    ;

INTEGER_VALUE
    : DIGIT+
    ;

DECIMAL_VALUE
    : DIGIT+ '.' DIGIT*
    | '.' DIGIT+
    ;

FLOAT_VALUE
    : DIGIT+ ('.' DIGIT*)? EXPONENT
    | '.' DIGIT+ EXPONENT
    ;

IDENTIFIER
    : (LETTER | '_') (LETTER | DIGIT | '_' | '@' | '$')*
    ;

QUOTED_IDENTIFIER
    : '"' (~'"' | '""')* '"'
    ;

JINJA
    : '{{' .*? '}}'
    ;

fragment EXPONENT
    : [Ee] [+-]? DIGIT+
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
