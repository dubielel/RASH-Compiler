# Generated from /home/milosz/SemestrIV/TKiK/RASH-Compiler/grammar/LanguageTestParser.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LanguageTestParser import LanguageTestParser
else:
    from LanguageTestParser import LanguageTestParser

# This class defines a complete generic visitor for a parse tree produced by LanguageTestParser.

class LanguageTestParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LanguageTestParser#parse.
    def visitParse(self, ctx:LanguageTestParser.ParseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#importStatement.
    def visitImportStatement(self, ctx:LanguageTestParser.ImportStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#statement.
    def visitStatement(self, ctx:LanguageTestParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#arrayDeclaration.
    def visitArrayDeclaration(self, ctx:LanguageTestParser.ArrayDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#objectDeclaration.
    def visitObjectDeclaration(self, ctx:LanguageTestParser.ObjectDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#functionCallParams.
    def visitFunctionCallParams(self, ctx:LanguageTestParser.FunctionCallParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:LanguageTestParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#postfixExpression.
    def visitPostfixExpression(self, ctx:LanguageTestParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#unaryExpression.
    def visitUnaryExpression(self, ctx:LanguageTestParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:LanguageTestParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:LanguageTestParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#relationalExpression.
    def visitRelationalExpression(self, ctx:LanguageTestParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#equalityExpression.
    def visitEqualityExpression(self, ctx:LanguageTestParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:LanguageTestParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:LanguageTestParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:LanguageTestParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:LanguageTestParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#expression.
    def visitExpression(self, ctx:LanguageTestParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#initializerClause.
    def visitInitializerClause(self, ctx:LanguageTestParser.InitializerClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#bracedInitList.
    def visitBracedInitList(self, ctx:LanguageTestParser.BracedInitListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#initializerList.
    def visitInitializerList(self, ctx:LanguageTestParser.InitializerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:LanguageTestParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#functionParams.
    def visitFunctionParams(self, ctx:LanguageTestParser.FunctionParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#paramDeclarationList.
    def visitParamDeclarationList(self, ctx:LanguageTestParser.ParamDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#paramDeclaration.
    def visitParamDeclaration(self, ctx:LanguageTestParser.ParamDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#functionReturnType.
    def visitFunctionReturnType(self, ctx:LanguageTestParser.FunctionReturnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#functionCall.
    def visitFunctionCall(self, ctx:LanguageTestParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#classDefinition.
    def visitClassDefinition(self, ctx:LanguageTestParser.ClassDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#classInheritance.
    def visitClassInheritance(self, ctx:LanguageTestParser.ClassInheritanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#classBody.
    def visitClassBody(self, ctx:LanguageTestParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#classAttributeDeclaration.
    def visitClassAttributeDeclaration(self, ctx:LanguageTestParser.ClassAttributeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#classMethodDefinition.
    def visitClassMethodDefinition(self, ctx:LanguageTestParser.ClassMethodDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#loopStatement.
    def visitLoopStatement(self, ctx:LanguageTestParser.LoopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#conditionalStatement.
    def visitConditionalStatement(self, ctx:LanguageTestParser.ConditionalStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#codeBlock.
    def visitCodeBlock(self, ctx:LanguageTestParser.CodeBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#literal.
    def visitLiteral(self, ctx:LanguageTestParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#jumpStatement.
    def visitJumpStatement(self, ctx:LanguageTestParser.JumpStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#variableDeclStatement.
    def visitVariableDeclStatement(self, ctx:LanguageTestParser.VariableDeclStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#variableAssignment.
    def visitVariableAssignment(self, ctx:LanguageTestParser.VariableAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:LanguageTestParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:LanguageTestParser.TypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#simpleTypeSpecifier.
    def visitSimpleTypeSpecifier(self, ctx:LanguageTestParser.SimpleTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#identifier.
    def visitIdentifier(self, ctx:LanguageTestParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#nameIdentifier.
    def visitNameIdentifier(self, ctx:LanguageTestParser.NameIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#arrayBrackets.
    def visitArrayBrackets(self, ctx:LanguageTestParser.ArrayBracketsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#scope.
    def visitScope(self, ctx:LanguageTestParser.ScopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageTestParser#unaryOperator.
    def visitUnaryOperator(self, ctx:LanguageTestParser.UnaryOperatorContext):
        return self.visitChildren(ctx)



del LanguageTestParser