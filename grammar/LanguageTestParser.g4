parser grammar LanguageTestParser;
options { tokenVocab = LanguageTestLexer; }

parse
    :   (KW_IMPORT identifier SEMI)* (classDefinition)* EOF
    ;

statement
    :   functionDefinition
    |   classDefinition
    ;

 expresion
    :
    ;

functionDefinition
    :   scope KW_STATIC? KW_FUNCTION identifier functionParams functionReturnType functionBody
    ;

functionBody
    :   LBRACE variableDeclStatement* RBRACE
    ;

classDefinition
    :   KW_CLASS identifier classBody
    ;

classBody
    :   LBRACE attributeDeclaration* functionDefinition* RBRACE
    ;

attributeDeclaration
    :   KW_STATIC? DECL_VAR identifier COLON typeSpecifier SEMI
    ;

functionParams
    :   LPAREN paramDeclarationList RPAREN
    ;

paramDeclarationList
    :   (paramDeclaration COMMA)+ paramDeclaration
    |   paramDeclaration?
    ;

paramDeclaration
    :   nameIdentifier COLON typeSpecifier
    ;

functionReturnType
    :   ARROW simpleTypeSpecifier
    ;

variableDeclStatement
    :   DECL_VAR nameIdentifier COLON typeSpecifier ASSIGN INTEGER_LITERAL SEMI
    ;

typeSpecifier
    :   (simpleTypeSpecifier | identifier) arrayBrackets?
    ;
    // | customTypeSpecifier

simpleTypeSpecifier
    :   T_INT | T_FLOAT | T_CHAR | T_STRING | T_VOID
    ;

identifier
    :   (nameIdentifier DOT)* nameIdentifier
    ;

nameIdentifier
    :   IDENTIFIER
    ;

arrayBrackets
    : LBRACKET RBRACKET
    ;

scope
    : KW_PRIVATE
    | KW_PUBLIC
    ;

