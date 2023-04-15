parser grammar LanguageTestParser;
options { tokenVocab = LanguageTestLexer; }

parse
    :   (statement)* EOF
    ;

statement
    :   functionDefinition
    |   classDefinition
    |   structDefinition
    ;

functionDefinition
    :   KW_FUNCTION identifier templateParams functionParams functionReturnType functionBody
    ;

classDefinition
    :   KW_CLASS
    ;

structDefinition
    :   KW_STRUCT
    ;

templateParams
    :  ANGLE_LEFT ((templateParam COMMA)* templateParam COMMA?) ANGLE_RIGHT
    ;

templateParam
    :   IDENTIFIER
    ;

functionParams
    :   LPAREN paramDeclarationList RPAREN
    ;

paramDeclarationList
    :   (paramDeclaration COMMA)* paramDeclaration?
    ;

paramDeclaration
    :   identifier (COLON typeSpecifier)?
    ;

functionReturnType
    :   ARROW simpleTypeSpecifier
    ;

functionBody
    :   LBRACKET variableDeclStatement* RBRACKET
    ;

variableDeclStatement
    :   DECL_VAR identifier (COLON simpleTypeSpecifier)? ASSIGN INTEGER_LITERAL SEMI
    ;

typeSpecifier
    :   simpleTypeSpecifier
    ;
    // | customTypeSpecifier

simpleTypeSpecifier
    :   T_INT | T_FLOAT | T_CHAR
    ;

identifier
    :   IDENTIFIER
    ;

