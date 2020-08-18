grammar Minml;


root
    : value
    ;

obj
    : '{' pair (',' pair)* '}'
    | '{' '}'
    ;

pair
    : key=string ':' value
    ;

array
    : '[' value (',' value)* ']'
    | '[' ']'
    ;

value
    : obj
    | array
    | string
    | number
    | true
    | false
    | null
    ;

string
    : STRING
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

STRING
    : '"' (ESC | SAFECODEPOINT)* '"'
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

WS
    : [ \t\n\r] + -> skip
    ;
