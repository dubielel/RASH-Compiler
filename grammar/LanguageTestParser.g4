parser grammar LanguageTestParser;
options { tokenVocab = LanguageTestLexer; }

parse
    :   importStatement* (classDefinition)* EOF
    ;

// IMPORTS
importStatement
    :   (KW_FROM identifier)? KW_IMPORT identifier SEMI
    ;

statement
    :   functionDefinition
    |   classDefinition
    |   codeBlock
    |   conditionalStatement
    |   variableDeclStatement
    |   variableAssignment
    |   loopStatement
    ;

arrayDeclaration
    :   KW_NEW simpleTypeSpecifier LBRACKET literal RBRACKET bracedInitList
    ;

primaryExpression
    :   literal+
    |   LPAREN expression RPAREN
    |   arrayDeclaration
    |   identifier
    ;


// EXPRESSIONS
postfixExpression
    :   primaryExpression
    |   postfixExpression LBRACKET (expression | bracedInitList) RBRACKET
    ;

multiplicativeExpression
    :   postfixExpression ( ( STAR | DIV | MOD ) postfixExpression )*
    ;

additiveExpression
    :   multiplicativeExpression ( ( PLUS | MINUS ) multiplicativeExpression )*
    ;

relationalExpression
    :   additiveExpression ( ( LT | GT | LE | GE ) additiveExpression )*
    ;

equalityExpression
    :   relationalExpression ( ( EQ | NE ) relationalExpression )*
    ;

logicalAndExpression
    :   equalityExpression ( KW_AND equalityExpression )*
    ;

logicalOrExpression
    :   logicalAndExpression ( KW_OR logicalAndExpression )*
    ;

conditionalExpression
    :   logicalOrExpression ( QUESTION expression COLON assignmentExpression )?
    ;

assignmentExpression
    :   conditionalExpression
    |   logicalOrExpression assignmentOperator initializerClause
    ;

expression
   :   assignmentExpression
   ;

initializerClause
    :   assignmentExpression
    |   bracedInitList
    ;

bracedInitList
    :   LBRACE initializerList? RBRACE
    ;

initializerList
    :   initializerClause ( COMMA initializerClause )*
    ;


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


// LOOPS
loopStatement
    :   KW_WHILE LPAREN expression? RPAREN codeBlock
    |   KW_FOR LPAREN DECL_VAR identifier COLON typeSpecifier KW_IN identifier RPAREN codeBlock
    ;


//CONDITIONAL INSTRUCTIONS
conditionalStatement
    :   KW_IF LPAREN expression RPAREN statement (KW_ELSE KW_IF LPAREN expression RPAREN statement)* (KW_ELSE statement)?
    ;


//OTHER STUFF
codeBlock
    : LBRACE statement* RBRACE
    ;

literal
    :   INTEGER_LITERAL
    |   FLOAT_LITERAL
    |   DOUBLE_LITERAL
    |   STRING_LITERAL
    |   BOOL_LITERAL
    ;

variableDeclStatement
    :   DECL_VAR nameIdentifier COLON typeSpecifier (ASSIGN expression)? SEMI
    ;

variableAssignment
    :   identifier assignmentOperator expression SEMI
    |   identifier LBRACKET expression RBRACKET assignmentOperator expression SEMI
    ;

assignmentOperator
    :   ASSIGN
    |   STAR_ASSIGN
    |   DIV_ASSIGN
    |   MOD_ASSIGN
    |   PLUS_ASSIGN
    |   MINUS_ASSIGN
    |   POW_ASSIGN
    ;

typeSpecifier
    :   (simpleTypeSpecifier | identifier) arrayBrackets?
    ;
    // | customTypeSpecifier

simpleTypeSpecifier
    :   T_INT | T_FLOAT | T_CHAR | T_STRING | T_VOID | T_BOOL
    ;

identifier
    :   (nameIdentifier DOT)* nameIdentifier
    ;

nameIdentifier
    :   IDENTIFIER
    ;

arrayBrackets
    :   LBRACKET RBRACKET
    ;

scope
    :   KW_PUBLIC | KW_PRIVATE | KW_PROTECTED
    ;