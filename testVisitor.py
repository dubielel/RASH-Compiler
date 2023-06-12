import os

from containers.class_container import ClassContainer, AccessRestriction
from containers.function_container import FunctionContainer
from containers.variable_container import VariableContainer
from enums.scope import Scope
from exception.compiler_exceptions import ClassReferencedBeforeDefinitionException, PrivateAttributeAccessException, \
    ProtectedAttributeAccessException

from gen.LanguageTestParser import LanguageTestParser
from gen.LanguageTestParserVisitor import LanguageTestParserVisitor
from typing import Optional


class RashVisitor(LanguageTestParserVisitor):
    RASH_C_TYPE_MAP = {
        "int": "int",
        "float": "float",
        "str": "char*",
        "bool": "int",
        "void": "void",
    }

    SCOPE_TRANSLATOR = {
        "public": Scope.PUBLIC,
        "protected": Scope.PROTECTED,
        "private": Scope.PRIVATE,
    }

    entry_point: Optional[FunctionContainer]

    current_class_name: str = ""
    classes: dict[str, ClassContainer] = {}
    library_dependencies: set[str] = set()

    variables = {}

    def __init__(self, dir: str):
        self.entry_point = None
        self.dir = dir
        if not os.path.isdir(dir):
            os.mkdir(dir)

    def visitParse(self, ctx):
        self.visitChildren(ctx)

        for class_name, class_container in self.classes.items():
            class_container.save_class(self.dir)

        libraries = "\n".join([f"#include \"{class_container.name}.h\"" for class_container in self.classes.values()])

        # Import needed libraries which are not imported by the header files
        class_imported_libraries = set()
        for class_container in self.classes.values():
            class_imported_libraries.update(class_container.library_dependencies)
        libraries += "\n" + "\n".join(
            [f"#include<{lib}>" for lib in self.library_dependencies.difference(class_imported_libraries)])
        entry_point = self.entry_point.get_entry_point_definition() if self.entry_point is not None else ""

        with open(f"{self.dir}/main.c", "w+") as f:
            f.write(f"{libraries}\n\n{entry_point}")

        self.createCMake("rashProject")

    def createCMake(self, project_name: str):
        files = " ".join(["main.c", *[f"{class_container.name}.c" for class_container in self.classes.values()]])
        files += " " + " ".join([f"{class_container.name}.h" for class_container in self.classes.values()])

        with open(f"{self.dir}/CMakeLists.txt", "w+") as f:
            f.write(f"cmake_minimum_required(VERSION 3.21)\n"
                    f"project({project_name} C)\n\n"
                    f"set(CMAKE_C_STANDARD 11)\n\n"
                    f"add_executable({project_name} {files})\n")

    def visitImportStatement(self, ctx: LanguageTestParser.ImportStatementContext):
        # TODO: Imports
        # We need to manage import statements - 1. Do we import header files, or do that somehow else?
        # 2. How do we manage importing only specific functions from a file?
        # For now, this returns nothing, we must do it later.
        pass

    # region Parts of parser that evaluate only to their text
    # ------------------------------------------------------------------------------------------------------------------

    def visitNameIdentifier(self, ctx: LanguageTestParser.NameIdentifierContext):
        return ctx.getText()

    def visitSimpleTypeSpecifier(self, ctx: LanguageTestParser.SimpleTypeSpecifierContext):
        return ctx.getText()

    def visitIdentifier(self, ctx: LanguageTestParser.IdentifierContext):
        if self.current_class_name == "":
            return ctx.getText()
        if ctx.getText() in self.classes[self.current_class_name].static_attributes:
            return f"{self.current_class_name}_{ctx.getText()}"
        if ctx.getText() in self.classes[self.current_class_name].static_methods:
            return f"{self.current_class_name}_{ctx.getText()}"

        if len(ctx.getText().split(".")) > 1:
            # This is a property / method accessor
            # For now, this is only allowed for depth of 1, should be recursive
            obj_name, property_name = ctx.getText().split(".")[:2]
            class_name = self.variables[obj_name][:-1]

            if class_name not in self.classes:
                raise ClassReferencedBeforeDefinitionException(class_name, ctx.start.line)
            property_scope = Scope.PUBLIC

            if property_name in self.classes[class_name].attributes:
                property_scope = self.classes[class_name].attributes[property_name].scope
            else:
                property_scope = self.classes[class_name].methods[property_name].scope

            access = self.classes[class_name].has_access(property_scope, self.current_class_name)

            if access == AccessRestriction.RESTRICTED_PRIVATE:
                raise PrivateAttributeAccessException(property_name, ctx.start.line)
            elif access == AccessRestriction.RESTRICTED_PROTECTED:
                raise ProtectedAttributeAccessException(property_name, ctx.start.line)

            if obj_name in self.variables:
                return f"{obj_name}->{property_name}"

        if ctx.getText() in self.classes[self.current_class_name].attributes:
            attribute = self.classes[self.current_class_name].attributes[ctx.getText()]
            return f"self->{attribute.name}"

        if ctx.getText() in self.classes[self.current_class_name].methods:
            method = self.classes[self.current_class_name].methods[ctx.getText()]
            return f"self->{method.name}"

        return ctx.getText()

    def visitUnaryOperator(self, ctx: LanguageTestParser.UnaryOperatorContext):
        return ctx.getText()

    def visitScope(self, ctx: LanguageTestParser.ScopeContext):
        return ctx.getText()

    # endregion

    # region Uncategorized
    # ------------------------------------------------------------------------------------------------------------------

    def visitTypeSpecifier(self, ctx: LanguageTestParser.TypeSpecifierContext):
        array_dim = 0 if not ctx.arrayBrackets() else len(ctx.arrayBrackets())
        if ctx.identifier():
            return self.visitIdentifier(ctx.identifier()) + array_dim * "*"
        else:
            return self.RASH_C_TYPE_MAP[self.visitSimpleTypeSpecifier(ctx.simpleTypeSpecifier())] + array_dim * "*"

    def visitCodeBlock(self, ctx: LanguageTestParser.CodeBlockContext):
        return "{\n" + "\n".join(str(self.visitStatement(s)) for s in ctx.statement()) + "\n}"

    # endregion

    # region Classes
    # ------------------------------------------------------------------------------------------------------------------

    def visitClassDefinition(self, ctx: LanguageTestParser.ClassDefinitionContext):

        class_name = self.visitIdentifier(ctx.nameIdentifier())

        self.classes[class_name] = ClassContainer(class_name)
        self.current_class_name = class_name

        self.visitClassBody(ctx.classBody())

    def visitClassBody(self, ctx: LanguageTestParser.ClassBodyContext) -> None:
        for attributeDeclaration in ctx.classAttributeDeclaration():
            self.visitClassAttributeDeclaration(attributeDeclaration)

        for methodDeclaration in ctx.classMethodDefinition():
            self.visitClassMethodDefinition(methodDeclaration)

    def visitClassAttributeDeclaration(self, ctx: LanguageTestParser.ClassAttributeDeclarationContext) -> None:
        var_decl = ctx.variableDeclStatement()

        var_type = self.visitTypeSpecifier(var_decl.typeSpecifier())
        var_identifier = self.visitNameIdentifier(var_decl.nameIdentifier())
        var_expression = self.visitExpression(var_decl.expression()) if var_decl.expression() else None
        var_scope = self.SCOPE_TRANSLATOR[self.visitScope(ctx.scope())]

        variable_container = VariableContainer(var_identifier, var_type, var_expression,
                                               var_scope, self.current_class_name)

        if ctx.KW_STATIC():
            self.classes[self.current_class_name].add_attribute(variable_container, True)
            self.variables[f"{self.current_class_name}_{var_identifier}"] = var_type
        else:
            self.classes[self.current_class_name].add_attribute(variable_container)

    # endregion

    # region Functions and methods
    # ------------------------------------------------------------------------------------------------------------------

    def visitClassMethodDefinition(self, ctx: LanguageTestParser.ClassMethodDefinitionContext) -> None:
        static = ctx.KW_STATIC() is not None
        method_scope = self.visitScope(ctx.scope())
        self.visitFunctionDefinition(ctx.functionDefinition(), method_scope, static)

    def visitFunctionDefinition(self, ctx: LanguageTestParser.FunctionDefinitionContext, scope: str = "public",
                                is_static: bool = False):

        function_identifier = self.visitIdentifier(ctx.nameIdentifier())
        function_return_type = self.visitFunctionReturnType(ctx.functionReturnType())
        function_params = self.visitFunctionParams(ctx.functionParams(), is_static)
        function_body = self.visitCodeBlock(ctx.codeBlock())

        function_container = FunctionContainer(function_identifier, function_return_type, function_params,
                                               self.SCOPE_TRANSLATOR[scope], function_body, self.current_class_name)

        if function_identifier == "main" and is_static:
            self.entry_point = FunctionContainer("main", "int", f"(int argc, {function_params[1:]}",
                                                 Scope.PUBLIC, f"{function_body[:-1]}return 0;\n}}",
                                                 self.current_class_name)
            return

        if is_static:
            self.classes[self.current_class_name].add_method(function_container, True)
        else:
            self.classes[self.current_class_name].add_method(function_container)

    def visitFunctionReturnType(self, ctx: LanguageTestParser.FunctionReturnTypeContext):
        return self.visitTypeSpecifier(ctx.typeSpecifier())

    def visitFunctionParams(self, ctx: LanguageTestParser.FunctionParamsContext, is_static: bool = False):
        c_params = f"({self.visitParamDeclarationList(ctx.paramDeclarationList(), is_static)})"
        return c_params

    def visitParamDeclarationList(self, ctx: LanguageTestParser.ParamDeclarationListContext, is_static: bool = False):
        param_declarations = []

        if not is_static:
            param_declarations.append(f"{self.current_class_name}* self")

        # This checks if there are any parameters
        if ctx:
            for param_decl in ctx.paramDeclaration():
                param_declarations.append(self.visitParamDeclaration(param_decl))

        return ", ".join(param_declarations)

    def visitParamDeclaration(self, ctx: LanguageTestParser.ParamDeclarationContext):

        c_param_type = self.visitTypeSpecifier(ctx.typeSpecifier())
        c_param_name = self.visitNameIdentifier(ctx.nameIdentifier())

        if ctx.expression():
            c_param_value = self.visitExpression(ctx.expression())
            return f"{c_param_type} {c_param_name} = {c_param_value}"

        return f"{c_param_type} {c_param_name}"

    # endregion

    # region Statements
    # ------------------------------------------------------------------------------------------------------------------

    def visitStatement(self, ctx: LanguageTestParser.StatementContext):
        result = self.visitChildren(ctx)
        return result

    def visitVariableDeclStatement(self, ctx: LanguageTestParser.VariableDeclStatementContext):
        var_type = self.visitTypeSpecifier(ctx.typeSpecifier())
        var_identifier = self.visitIdentifier(ctx.nameIdentifier())
        var_value = self.visitExpression(ctx.expression())

        if var_type not in self.RASH_C_TYPE_MAP:
            var_type = var_type + "*"

        self.variables[var_identifier] = var_type
        return f"{var_type} {var_identifier} = {var_value}"

    def visitLoopStatement(self, ctx: LanguageTestParser.LoopStatementContext):
        if ctx.KW_WHILE():
            return f"while ({self.visitExpression(ctx.expression())}) {self.visitStatement(ctx.statement())}"
        else:
            var_identifier = self.visitIdentifier(ctx.identifier(0))
            var_type = self.visitTypeSpecifier(ctx.typeSpecifier())
            it_identifier = self.visitIdentifier(ctx.identifier(1))
            loop_init = f"for (int i = 0; i < sizeof({it_identifier}) / sizeof({it_identifier}[0]); i++) "

            var_definition = f"{var_type} {var_identifier} = {it_identifier}[i];\n"
            self.variables[var_identifier] = var_type

            loop_body = self.visitStatement(ctx.statement())
            return loop_init + "{\n" + var_definition + loop_body[2:]

    def visitConditionalStatement(self, ctx: LanguageTestParser.ConditionalStatementContext):
        # QUESTION: Do we need to do anything here?
        return self.visitChildren(ctx)

    # endregion

    # region Expressions
    # ------------------------------------------------------------------------------------------------------------------

    def visitExpression(self, ctx: LanguageTestParser.ExpressionContext):
        return self.visitAssignmentExpression(ctx.assignmentExpression())

    def visitAssignmentExpression(self, ctx: LanguageTestParser.AssignmentExpressionContext):
        if ctx.conditionalExpression() is not None:
            return self.visitConditionalExpression(ctx.conditionalExpression())
        else:
            # TODO: Assignment expression
            # Other cases
            # I think it would work just fine like this (?)
            return self.visitChildren(ctx)

    def visitConditionalExpression(self, ctx: LanguageTestParser.ConditionalExpressionContext):
        # This is a conditional expression of type test ? 1 : 5 if it contains question mark
        if ctx.QUESTION():
            logical_or_expression = self.visitLogicalOrExpression(ctx.logicalOrExpression())
            expression = self.visitExpression(ctx.expression())
            assigment_expression = self.visitAssignmentExpression(ctx.assignmentExpression())
            return f"{logical_or_expression} ? {expression} : {assigment_expression}"
        else:
            return self.visitLogicalOrExpression(ctx.logicalOrExpression())

    def visitLogicalOrExpression(self, ctx: LanguageTestParser.LogicalOrExpressionContext) -> str:
        expression_values = []
        for and_expression in ctx.logicalAndExpression():
            expression_values.append(self.visitLogicalAndExpression(and_expression))
        return " || ".join(expression_values)

    def visitLogicalAndExpression(self, ctx: LanguageTestParser.LogicalAndExpressionContext) -> str:
        expression_values = []
        for eq_expression in ctx.equalityExpression():
            expression_values.append(self.visitEqualityExpression(eq_expression))
        return " && ".join(expression_values)

    def visitEqualityExpression(self, ctx: LanguageTestParser.EqualityExpressionContext) -> str:
        first_rel_expression = ctx.relationalExpression(0)
        results = [self.visitRelationalExpression(first_rel_expression)]

        for i in range(1, len(ctx.relationalExpression())):
            operator = ctx.getChild(2 * i - 1)
            rel_expression = ctx.relationalExpression(i)
            results.append(str(operator))
            results.append(self.visitRelationalExpression(rel_expression))

        return " ".join(results)

    def visitRelationalExpression(self, ctx: LanguageTestParser.RelationalExpressionContext) -> str:
        first_add_expression = ctx.additiveExpression(0)
        results = [self.visitAdditiveExpression(first_add_expression)]

        for i in range(1, len(ctx.additiveExpression())):
            operator = ctx.getChild(2 * i - 1)
            add_expression = ctx.additiveExpression(i)
            results.append(str(operator))
            results.append(self.visitAdditiveExpression(add_expression))

        return " ".join(results)

    def visitAdditiveExpression(self, ctx: LanguageTestParser.AdditiveExpressionContext) -> str:
        first_mul_expression = ctx.multiplicativeExpression(0)
        results = [self.visitMultiplicativeExpression(first_mul_expression)]

        for i in range(1, len(ctx.multiplicativeExpression())):
            operator = ctx.getChild(2 * i - 1)
            mul_expression = ctx.multiplicativeExpression(i)
            results.append(str(operator))
            results.append(self.visitMultiplicativeExpression(mul_expression))

        return " ".join(results)

    def visitMultiplicativeExpression(self, ctx: LanguageTestParser.MultiplicativeExpressionContext):
        first_unary_expression = ctx.unaryExpression(0)
        results = [self.visitUnaryExpression(first_unary_expression)]

        for i in range(1, len(ctx.unaryExpression())):
            operator = ctx.getChild(2 * i - 1)
            unary_expression = ctx.unaryExpression(i)
            results.append(str(operator))
            results.append(self.visitUnaryExpression(unary_expression))

        return " ".join(results)

    def visitUnaryExpression(self, ctx: LanguageTestParser.UnaryExpressionContext):
        if ctx.postfixExpression():
            return self.visitPostfixExpression(ctx.postfixExpression())
        elif ctx.unaryExpression() and ctx.unaryOperator():
            unary_operator = self.visitUnaryOperator(ctx.unaryOperator())
            expr = self.visitUnaryExpression(ctx.unaryExpression())

            return f"{unary_operator} {expr}"

    def visitPostfixExpression(self, ctx: LanguageTestParser.PostfixExpressionContext):
        if ctx.primaryExpression():
            return self.visitPrimaryExpression(ctx.primaryExpression())
        elif ctx.postfixExpression():
            # QUESTION: IDK if this is correct, but we'll see
            return self.visitChildren(ctx)

    def visitPrimaryExpression(self, ctx: LanguageTestParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)

    def visitFunctionCall(self, ctx: LanguageTestParser.FunctionCallContext):
        identifier = self.visitIdentifier(ctx.identifier())
        res = self.visitChildren(ctx)

        if "->" in identifier:
            # This only works for depth 1, not for nested objects, e.g. a->b->c()
            obj_name = identifier.split("->")[0]
            params = self.visitFunctionCallParams(ctx.functionCallParams())
            all_params = obj_name if params == "()" else f"{obj_name}, {params[1:-1]}"
            return f"{identifier}({all_params})"

        if identifier == "print":
            self.classes[self.current_class_name].add_library_dependency("stdio.h")
            self.library_dependencies.add("stdio.h")

            params = self.visitFunctionCallParams(ctx.functionCallParams())
            expr_value = params[1:-1].split(", ")[0].strip()

            if len(expr_value.split("->")) > 1:
                print(expr_value.split("->"))
                # This is case where it is an object property
                if expr_value.split("->")[0] in self.variables:
                    # All objects are of pointer type <Class Name>* so we need to remove the last character
                    obj_type = self.variables[expr_value.split("->")[0]][:-1]
                    if obj_type not in self.classes:
                        raise ClassReferencedBeforeDefinitionException(obj_type, ctx.start.line)

                    attr_name = expr_value.split("->")[1]
                    # This should be recursive, but it's not needed for now
                    var_type = self.classes[obj_type].attributes[attr_name].type
                    return self.printWrapper(expr_value, var_type)

            if len(expr_value.split("->")) > 1:
                attr_name = expr_value.split("->")[1]
                if attr_name in self.classes[self.current_class_name].attributes:
                    var_type = self.classes[self.current_class_name].attributes[attr_name].type
                    return self.printWrapper(expr_value, var_type)

            if expr_value in self.variables:
                # If the expression is a variable name, we need to get its type
                var_type = self.variables[expr_value]
                return self.printWrapper(expr_value, var_type)
            else:
                # If the expression is not a variable name, we can just print it
                return f"printf(\"%s\\n\", {expr_value})"

        return identifier + res[len(identifier) + 1:]

    def printWrapper(self, expr_value: str, var_type: str):
        if var_type == "int":
            return f"printf(\"%d\\n\", {expr_value})"
        elif var_type == "float":
            return f"printf(\"%f\\n\", {expr_value})"
        else:
            return f"printf(\"%s\\n\", {expr_value})"

    def visitObjectDeclaration(self, ctx: LanguageTestParser.ObjectDeclarationContext):
        type = self.visitIdentifier(ctx.nameIdentifier())
        params = self.visitFunctionCallParams(ctx.functionCallParams())
        return f"new__{type}{params}"

    def visitFunctionCallParams(self, ctx: LanguageTestParser.FunctionCallParamsContext):
        params = []
        for expr in ctx.expression():
            params.append(self.visitExpression(expr))
        return "(" + ", ".join(params) + ")"

    # endregion

    # region Overrides
    # ------------------------------------------------------------------------------------------------------------------

    def visitTerminal(self, node):
        if node.getText() == "<EOF>":
            return ""
        return node.getText()

    def aggregateResult(self, aggregate, nextResult):
        remove_space_after = ["("]
        remove_space_before = [";", ")"]

        if aggregate is None and nextResult is None:
            return None
        if aggregate is None:
            return nextResult
        elif nextResult is None:
            return aggregate
        elif len(aggregate) > 0:
            if aggregate[-1] in remove_space_after or nextResult in remove_space_before:
                return f"{aggregate}{nextResult}"
            return f"{aggregate} {nextResult}"
        else:
            return f"{aggregate} {nextResult}"

    # endregion
