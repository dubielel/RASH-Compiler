parser grammar LanguageTestParser;
options { tokenVocab = LanguageTestLexer; }

parse
    :   ((KW_FROM identifier)? KW_IMPORT identifier SEMI)* (classDefinition)* EOF
    ;

statement
    :   functionDefinition
    |   classDefinition
    |   codeBlock
    |   conditionalStatement
    |   variableDeclStatement
    |   variableAssignment
    |   forLoop
    |   whileLoop
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
    :   additiveExpression ( ( LSHIFT | RSHIFT ) additiveExpression )*
    ;

relationalExpression
    :   shiftExpression ( ( LT | GT | LE | GE ) shiftExpression )*
    ;

equalityExpression
    :   relationalExpression ( ( EQ | NE ) relationalExpression )*
    ;

bitwiseAndExpression
    :   equalityExpression ( AND equalityExpression )*
    ;

bitwiseExclusiveOrExpression
    :   bitwiseAndExpression ( CARET bitwiseAndExpression )*
    ;

bitwiseInclusiveOrExpression
    :   bitwiseExclusiveOrExpression ( OR bitwiseExclusiveOrExpression )*
    ;

logicalAndExpression
    :   bitwiseInclusiveOrExpression ( KW_AND bitwiseInclusiveOrExpression )*
    ;

logicalOrExpression
    :   logicalAndExpression ( KW_OR logicalAndExpression )*
    ;

conditionalExpression
    :   logicalOrExpression ( QUESTION expression COLON /*assignmentExpression*/ )?
    ;   // TODO discuss assignmentExpression vs. variableAssignment referring to Cpp grammar implementation


// FUNCTIONS
functionDefinition
    :   scope KW_STATIC? KW_FUNCTION nameIdentifier functionParams functionReturnType codeBlock
    ;

functionParams
    :   LPAREN paramDeclarationList? RPAREN
    ;

paramDeclarationList
    :   paramDeclaration (COMMA paramDeclaration)*
    ;

paramDeclaration
    :   nameIdentifier COLON typeSpecifier (ASSIGN expression)
    ;

functionReturnType
    :   ARROW typeSpecifier
    ;


//CLASSES
classDefinition
    :   KW_CLASS nameIdentifier classInheritance  classBody
    ;

classInheritance
    :   (LPAREN identifier (COMMA identifier)* RPAREN)?
    ;

classBody
    :   LBRACE classAttributeDeclaration* functionDefinition* RBRACE
    ;

classAttributeDeclaration
    :   KW_STATIC? scope DECL_VAR identifier COLON typeSpecifier SEMI
    ;


 //LOOPS
 forLoop
    :   KW_FOR LPAREN variableDeclStatement KW_IN identifier RPAREN statement
    ;

 whileLoop
    :   KW_WHILE LPAREN expression RPAREN statement
    ;


//CONDITIONAL INSTRUCTIONS
conditionalStatement
    :   KW_IF LPAREN expression RPAREN statement (KW_ELSE KW_IF LPAREN expression RPAREN statement)* (KW_ELSE statement)?
    ;


//OTHER STUFF
codeBlock
    : LBRACE statement* RBRACE
    ;

variableDeclStatement
    :   DECL_VAR nameIdentifier COLON typeSpecifier (ASSIGN expression)? SEMI
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
    | KW_PROTECTED
    | KW_PUBLIC
    ;

