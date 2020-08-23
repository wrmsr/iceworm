grammar Minml;


root
    : value
    ;

value
    : obj
    | array
    | identifier
    | string
    | number
    | true
    | false
    | null
    ;

obj
    : '{' pair (',' pair)* ','? '}'
    | '{' '}'
    ;

pair
    : key (':' value)?
    ;

key
    : identifier
    | string
    ;

array
    : '[' value (',' value)*  ','? ']'
    | '[' ']'
    ;

identifier
    : IDENTIFIER
    ;

string
    : TRI_DQ_STRING
    | TRI_SQ_STRING
    | DQ_STRING
    | SQ_STRING
    ;

number
    : NUMBER
    ;

true
    : TRUE
    ;

false
    : FALSE
    ;

null
    : NULL
    ;

FALSE: 'false';
NULL: 'null';
TRUE: 'true';

DQ_STRING
    : '"' (ESC | SAFECODEPOINT)* '"'
    ;

SQ_STRING
    : '\'' (ESC | SAFECODEPOINT)* '\''
    ;

TRI_DQ_STRING
    : '"""' (~'"' | '\\"' | ('"' ~'"') | ('""' ~'"'))* '"""'
    ;

TRI_SQ_STRING
    : '\'\'\'' (~'\'' | '\\\'' | ('\'' ~'\'') | ('\'\'' ~'\''))* '\'\'\''
    ;

IDENTIFIER
    : [A-Za-z_]
    ;

fragment ESC
    : '\\' (["\\/bfnrt] | UNICODE)
    ;

fragment UNICODE
    : 'u' HEX HEX HEX HEX
    ;

fragment HEX
    : [0-9a-fA-F]
    ;

fragment SAFECODEPOINT
    : ~ ["\\\u0000-\u001F]
    ;

NUMBER
    : '-'? INT ('.' [0-9] +)? EXP?
    ;

fragment INT
    : '0'
    | [1-9] [0-9]*
    ;

fragment EXP
    : [Ee] [+\-]? INT
    ;

COMMENT
    : '#' ~[\r\n]* '\r'? '\n'? -> channel(HIDDEN)
    ;

WS
    : [ \t\n\r] + -> skip
    ;
