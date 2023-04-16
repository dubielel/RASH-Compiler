parser grammar LanguageTestParser;
options { tokenVocab = LanguageTestLexer; }

parse
    :   (KW_IMPORT identifier SEMI)* (classDefinition)* EOF
    ;

statement
    :   functionDefinition
    |   classDefinition
    |   codeBlock
    |   conditionalStatement
    |   variableDeclStatement
    |   variableAssignment
    ;

 expresion
    :   identifier
    |   relation
    ;


// FUNCTIONS
functionDefinition
    :   scope KW_STATIC? KW_FUNCTION nameIdentifier functionParams functionReturnType codeBlock
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


//CLASSES
classDefinition
    :   KW_CLASS identifier classBody
    ;

classBody
    :   LBRACE attributeDeclaration* functionDefinition* RBRACE
    ;

attributeDeclaration
    :   KW_STATIC? DECL_VAR identifier COLON typeSpecifier SEMI
    ;


//CONDITIONAL INSTRUCTIONS
conditionalStatement
    :   KW_IF (expresion) statement (KW_ELSE KW_IF (expresion) statement)* (KW_ELSE statement)?
    ;


//OTHER STUFF
codeBlock
    : LBRACE statement* RBRACE
    ;

variableDeclStatement
    :   DECL_VAR nameIdentifier COLON typeSpecifier ASSIGN expresion SEMI
    ;

variableAssignment
    :   identifier ASSIGN expresion SEMI
    ;

relation // ????????
    :   expresion (EQ | NE | LT | GT | LE | GE) expresion
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

