from gen.LanguageTestParser import LanguageTestParser
from gen.LanguageTestParserVisitor import LanguageTestParserVisitor
from typing import Optional
from enum import Enum
from dataclasses import dataclass


class Scope(Enum):
    PUBLIC = 1
    PROTECTED = 2
    PRIVATE = 3


@dataclass
class FunctionContainer:
    identifier: str
    return_type: str
    params: str
    scope: Scope
    body: str
    class_name: str
    is_new: bool = False

    @property
    def name(self):
        scope_map = {Scope.PUBLIC: "", Scope.PROTECTED: "pr_", Scope.PRIVATE: "pv_"}
        return f"{scope_map[self.scope]}{self.identifier}"

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot set name of FunctionContainer")

    def get_in_struct_declaration(self):
        return f"{self.return_type} (*{self.name}){self.params};"

    def get_global_declaration(self):
        if self.is_new:
            return f"{self.return_type} new__{self.class_name}{self.params};"
        return f"{self.return_type} {self.class_name}_{self.name}{self.params};"

    def get_definition(self):
        if self.is_new:
            return f"{self.return_type} new__{self.class_name}{self.params} {self.body}"
        return f"{self.return_type} {self.class_name}_{self.name}{self.params} {self.body}"

    def get_entry_point_definition(self):
        return f"{self.return_type} {self.name}{self.params} {self.body}"


@dataclass
class VariableContainer:
    identifier: str
    type: str
    value: Optional[str]
    scope: Scope
    class_name: str

    @property
    def name(self):
        scope_map = {Scope.PUBLIC: "", Scope.PROTECTED: "pr_", Scope.PRIVATE: "pv_"}
        return f"{scope_map[self.scope]}{self.identifier}"

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot set name of AttributeContainer")

    def get_static_declaration(self):
        return f"{self.class_name}_{self.type} {self.name}"

    def get_static_definition(self):
        if self.value is None:
            return f"{self.class_name}_{self.type} {self.name};"
        else:
            return f"{self.class_name}_{self.type} {self.name} = {self.value};"

    def get_declaration(self):
        return f"{self.type} {self.name};"

    def get_definition(self):
        if self.value is None:
            return f"{self.type} {self.name};"
        else:
            return f"{self.type} {self.name} = {self.value};"


class ClassContainer:
    has_init: bool
    name: str
    methods: dict[str, FunctionContainer]
    attributes: dict[str, VariableContainer]

    static_methods: dict[str, FunctionContainer]
    static_attributes: dict[str, VariableContainer]

    library_dependencies: set[str]

    def __init__(self, name: str):
        self.name = name
        self.methods = {}
        self.attributes = {}
        self.static_methods = {}
        self.static_attributes = {}
        self.has_init = False
        self.library_dependencies = set()

    def add_attribute(self, attribute: VariableContainer, is_static: bool = False):
        if is_static:
            self.static_attributes[attribute.identifier] = attribute
        else:
            self.attributes[attribute.identifier] = attribute

    def add_method(self, method: FunctionContainer, is_static: bool = False):
        if method.identifier == "__init__":
            self.has_init = True

        if is_static:
            self.static_methods[method.identifier] = method
        else:
            self.methods[method.identifier] = method

    def add_library_dependency(self, lib: str):
        self.library_dependencies.add(lib)

    def create_new_method(self) -> FunctionContainer:
        self.library_dependencies.add("stdlib.h")

        body = f"{{\n\t{self.name}* this = ({self.name}*)malloc(sizeof({self.name}));\n"

        for name, method in self.methods.items():
            body += f"\tthis->{name} = {self.name}_{name};\n"

        if self.has_init:
            init_method = self.methods["__init__"]
            init_params = init_method.params.split(", ")
            init_params = [p.split(" ")[1] for p in init_params]
            body += f"\tthis->{init_method.name}{init_params};\n\treturn this;\n}}"
            return FunctionContainer(
                f"new__{self.name}",
                self.name + "*",
                init_method.params,
                init_method.scope,
                body,
                self.name,
                is_new=True,
            )

        body += "\treturn this;\n}}"

        return FunctionContainer(
            f"new__{self.name}",
            self.name + "*",
            "()",
            Scope.PRIVATE,
            body,
            self.name,
            is_new=True,
        )

    def save_class(self):
        header_path = f"{self.name}.h"
        source_path = f"{self.name}.c"

        new_method = self.create_new_method()

        with open(header_path, "w+") as f:
            f.write(f"#ifndef {self.name.upper()}_H\n")
            f.write(f"#define {self.name.upper()}_H\n\n")

            for lib in self.library_dependencies:
                f.write(f"#include<{lib}>\n")

            f.write(f"\n")
            f.write(f"typedef s_{self.name} {self.name};\n\n")

            f.write(f"struct s_{self.name} {{\n")
            for attribute in self.attributes.values():
                f.write(f"\t{attribute.get_definition()}\n")
            for method in self.methods.values():
                f.write(f"\t{method.get_in_struct_declaration()}\n")
            f.write(f"}};\n\n")

            for method in self.methods.values():
                f.write(f"{method.get_global_declaration()}\n")

            for method in self.static_methods.values():
                f.write(f"{method.get_global_declaration()}\n")

            for attribute in self.static_attributes.values():
                f.write(f"{attribute.get_static_declaration()}\n")

            f.write(f"{new_method.get_global_declaration()}\n")
            f.write(f"\n#endif\n")

        with open(source_path, "w+") as f:
            f.write(f"#include<{header_path}>\n\n")

            for method in self.methods.values():
                f.write(f"{method.get_definition()}\n\n")

            for attribute in self.static_attributes.values():
                if attribute.value is not None:
                    f.write(f"{attribute.get_static_definition()}\n\n")

            for method in self.static_methods.values():
                f.write(f"{method.get_definition()}\n\n")

            f.write(f"{new_method.get_definition()}\n\n")


class RASHTestVisitor(LanguageTestParserVisitor):
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

    variables = {}

    def __init__(self, dir: str):
        self.entry_point = None
        self.dir = dir

    def visitParse(self, ctx):
        self.visitChildren(ctx)
        """
        libraries = "\n".join([f"#include<{lib}>" for lib in self.libraries])
        typedefs = "\n".join(self.typedefs)
        static_vars = "\n".join(self.static_vars)
        prototypes = "\n".join(self.function_prototypes)
        # program_parts = [libraries, typedefs, program, static_vars, prototypes, self.entry_point]
        # return "\n\n".join(program_parts)
        """

        for class_name, class_container in self.classes.items():
            class_container.save_class()

        libraries = "\n".join([f"#include<{class_container.name}.h>" for class_container in self.classes.values()])
        entry_point = self.entry_point.get_entry_point_definition() if self.entry_point is not None else ""
        return f"{libraries}\n\n{entry_point}"

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
        else:
            self.classes[self.current_class_name].add_attribute(variable_container)

    # Functions and methods --------------------------------------------------------------------------------------------

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

    # Statements -------------------------------------------------------------------------------------------------------

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

    # Expressions ------------------------------------------------------------------------------------------------------

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

        if identifier == "print":
            self.classes[self.current_class_name].add_library_dependency("stdio.h")

            params = self.visitFunctionCallParams(ctx.functionCallParams())
            expr_value = params[1:-1].split(", ")[0].strip()

            if expr_value in self.variables:
                # If the expression is a variable name, we need to get its type
                var_type = self.variables[expr_value]
                if var_type == "int":
                    return f"printf(\"%d\\n\", {expr_value})"
                elif var_type == "float":
                    return f"printf(\"%f\\n\", {expr_value})"
                else:
                    return f"printf(\"%s\\n\", {expr_value})"

            else:
                # If the expression is not a variable name, we can just print it
                return f"printf(\"%s\\n\", {expr_value})"

        return identifier + res[len(identifier) + 1:]

    def visitObjectDeclaration(self, ctx: LanguageTestParser.ObjectDeclarationContext):
        type = self.visitIdentifier(ctx.nameIdentifier())
        params = self.visitFunctionCallParams(ctx.functionCallParams())
        return f"new__{type}{params}"

    def visitFunctionCallParams(self, ctx: LanguageTestParser.FunctionCallParamsContext):
        params = []
        for expr in ctx.expression():
            params.append(self.visitExpression(expr))
        return "(" + ", ".join(params) + ")"

    # Overrides --------------------------------------------------------------------------------------------------------

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

    # Helpers ----------------------------------------------------------------------------------------------------------
