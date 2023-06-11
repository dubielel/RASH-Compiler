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
    |   codeBlock
    |   conditionalStatement
    |   loopStatement
    |   jumpStatement SEMI
    |   variableDeclStatement SEMI
    |   variableAssignment SEMI
    |   expression SEMI
    ;

arrayDeclaration
    :   KW_NEW ( nameIdentifier | simpleTypeSpecifier ) ( LBRACKET literal RBRACKET bracedInitList ) ?
    ;

objectDeclaration
    :   KW_NEW (nameIdentifier | simpleTypeSpecifier) functionCallParams
    ;

functionCallParams
    :   LPAREN ( expression ( COMMA expression )* )? RPAREN
    ;

primaryExpression
    :   literal+
    |   functionCall
    |   LPAREN expression RPAREN
    |   arrayDeclaration
    |   objectDeclaration
    |   identifier
    ;


// EXPRESSIONS
postfixExpression
    :   primaryExpression
    |   postfixExpression LBRACKET (expression | bracedInitList) RBRACKET
    ;

unaryExpression
    :   postfixExpression
    |   unaryOperator unaryExpression
    ;

multiplicativeExpression
    :   unaryExpression ( ( STAR | DIV | MOD ) unaryExpression )*
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
    :   logicalOrExpression ( QUESTION expression COLON assignmentExpression )? // TODO why there is assignmentExpression instead of expression?
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
    :   KW_FUNCTION nameIdentifier functionParams functionReturnType codeBlock
    ;

functionParams
    :   LPAREN paramDeclarationList? RPAREN
    ;

paramDeclarationList
    :   paramDeclaration (COMMA paramDeclaration)*
    ;

paramDeclaration
    :   nameIdentifier COLON typeSpecifier (ASSIGN expression)?
    ;

functionReturnType
    :   ARROW typeSpecifier
    ;

functionCall
    :   identifier functionCallParams
    ;

//CLASSES
classDefinition
    :   KW_CLASS nameIdentifier classInheritance classBody
    ;

classInheritance
    :   (LPAREN identifier (COMMA identifier)* RPAREN)?
    ;

classBody
    :   LBRACE classAttributeDeclaration* classMethodDefinition* RBRACE
    ;

classAttributeDeclaration
    :    scope KW_STATIC? variableDeclStatement SEMI
    ;

classMethodDefinition
    :   scope KW_STATIC? functionDefinition
    ;


// LOOPS
loopStatement
    :   KW_WHILE LPAREN expression? RPAREN statement
    |   KW_FOR LPAREN DECL_VAR identifier COLON typeSpecifier KW_IN identifier RPAREN statement
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
    |   STRING_LITERAL
    |   BOOL_LITERAL
    ;

jumpStatement
    :   KW_RETURN expression?
    |   KW_BREAK
    |   KW_CONTINUE
    ;

variableDeclStatement
    :   DECL_VAR nameIdentifier COLON typeSpecifier (ASSIGN expression)?
    ;

variableAssignment
    :   identifier assignmentOperator expression SEMI
    |   identifier LBRACKET expression RBRACKET assignmentOperator expression
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
    :   (simpleTypeSpecifier | identifier) arrayBrackets*
    ;

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

unaryOperator
    :   KW_NOT
    ;