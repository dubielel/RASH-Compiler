lexer grammar LanguageTestLexer;

// Loops etc.
KW_FOR: 'for';
KW_WHILE: 'while';
KW_IN: 'in';

// Conditionals
KW_IF: 'if';
KW_ELSE: 'else';

// Access modifiers
KW_PRIVATE: 'private';
KW_PROTECTED: 'protected';
KW_PUBLIC: 'public';

KW_STATIC: 'static';

// Classes and structs
KW_CLASS: 'class';

// Functions etc
KW_FUNCTION: 'func';
KW_RETURN: 'return';

// Expressions
KW_AND: 'and';
KW_OR: 'or';
KW_NOT: 'not';
KW_IS: 'is';

// Booleans
KW_TRUE: 'True';
KW_FALSE: 'False';

// Utils
KW_IMPORT: 'import';
KW_FROM: 'from';
KW_AS: 'as';
KW_NEW: 'new';

T_INT: 'int';
T_FLOAT: 'float';
T_CHAR: 'char';
T_STRING: 'str';
T_VOID: 'void';
T_BOOL: 'bool';

DECL_VAR: 'var';

WHITESPACE: [\p{Zs}\t] -> skip;
NEWLINE: ('\r\n' | [\r\n]) -> skip;

STRING_LITERAL
    : '"'
    (
        ~["]
        | QUOTE_ESCAPE
        | ASCII_ESCAPE
        | UNICODE_ESCAPE
        | NEWLINE_ESCAPE
    )* '"'
    ;

// Boolean
BOOL_LITERAL
    :   KW_TRUE
    |   KW_FALSE
    ;

// Numbers
INTEGER_LITERAL
    :   DEC_LITERAL
    |   BIN_LITERAL
    |   OCT_LITERAL
    |   HEX_LITERAL
    ;

FLOAT_LITERAL
    :   DEC_LITERAL '.' DEC_LITERAL 'f'
    ;

DOUBLE_LITERAL
    :   DEC_LITERAL '.' DEC_LITERAL
    ;

// Underscore allows for thousands division etc

DEC_LITERAL: DEC_DIGIT (DEC_DIGIT | '_')*;
HEX_LITERAL: '0x' '_'* HEX_DIGIT (HEX_DIGIT | '_')*;
OCT_LITERAL: '0o' '_'* OCT_DIGIT (OCT_DIGIT | '_')*;
BIN_LITERAL: '0b' '_'* BIN_DIGIT (BIN_DIGIT | '_')*;

IDENTIFIER
    : [A-Za-z_]+ [A-Za-z_0-9]*
    ;


// Fragments

fragment ASCII_ESCAPE: '\\x' OCT_DIGIT HEX_DIGIT | COMMON_ESCAPE;
fragment BYTE_ESCAPE: '\\x' HEX_DIGIT HEX_DIGIT | COMMON_ESCAPE;
fragment COMMON_ESCAPE: '\\' [nrt\\0];
fragment UNICODE_ESCAPE: '\\u{' HEX_DIGIT HEX_DIGIT? HEX_DIGIT? HEX_DIGIT? HEX_DIGIT? HEX_DIGIT? '}';
fragment QUOTE_ESCAPE: '\\' ['"];
fragment NEWLINE_ESCAPE: '\\' '\n';

fragment OCT_DIGIT: [0-7];
fragment DEC_DIGIT: [0-9];
fragment HEX_DIGIT: [0-9a-fA-F];
fragment BIN_DIGIT: [01];

COMMA: ',';
DOT: '.';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACKET: '[';
RBRACKET: ']';
COLON: ':';
ARROW: '->';

// Assignment operators
ASSIGN: '=';
STAR_ASSIGN: '*=';
DIV_ASSIGN: '/=';
MOD_ASSIGN: '%=';
PLUS_ASSIGN: '+=';
MINUS_ASSIGN: '-=';
POW_ASSIGN: '**=';
SEMI: ';';

// Relations
EQ: '==';
NE: '!=';
LT: '<';
GT: '>';
LE: '<=';
GE: '>=';
LSHIFT: '<<';
RSHIFT: '>>';

// Operations
PLUS: '+';
MINUS: '-';
STAR: '*';
DIV: '/';
MOD: '%';
POW: '**';

AND: '&';
CARET: '^';
OR: '|';
QUESTION: '?';

SINGLE_LINE_COMMENT: '//' ~[\r]* -> skip;
MULTI_LINE_COMMENT: '/*' .*? '*/' -> skip;