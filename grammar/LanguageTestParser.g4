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

 expression
    :   identifier
    ;

// EXPRESSIONS
castExpression
    :   // TODO
    ;

multiplicativeExpression
    :   castExpression ( ( STAR | DIV | MOD ) castExpression )*
    ;

additiveExpression
    :   multiplicativeExpression ( ( PLUS | MINUS ) multiplicativeExpression )*
    ;

shiftExpression
    :   additiveExpression ( ( GT GT | LT LT ) additiveExpression )*
    ;

relationalExpression
    :   shiftExpression ( ( LT | GT | LE | GE ) shiftExpression )*
    ;

equalityExpression
    :   relationalExpression ( ( EQ | NE ) relationalExpression )*
    ;

andExpression
    :   equalityExpression ( AND equalityExpression )*
    ;

exclusiveOrExpression
    :   andExpression ( CARET andExpression )*
    ;

inclusiveOrExpression
    :   exclusiveOrExpression ( OR exclusiveOrExpression )*
    ;

logicalAndExpression
    :   inclusiveOrExpression ( AND AND inclusiveOrExpression )*
    ;

logicalOrExpression
    :   logicalAndExpression ( OR OR logicalAndExpression )*
    ;

conditionalExpression
    :   logicalOrExpression ( QUESTION expression COLON assignmentExpression )?
    ;   // TODO discuss assignmentExpression vs. variableAssignment referring to Cpp grammar implementation

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
    :   KW_IF (expression) statement (KW_ELSE KW_IF (expression) statement)* (KW_ELSE statement)?
    ;


//OTHER STUFF
codeBlock
    : LBRACE statement* RBRACE
    ;

variableDeclStatement
    :   DECL_VAR nameIdentifier COLON typeSpecifier ASSIGN expression SEMI
    ;

variableAssignment
    :   identifier ASSIGN expression SEMI
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

