from gen.LanguageTestParser import LanguageTestParser
from gen.LanguageTestParserVisitor import LanguageTestParserVisitor


class RASHTestVisitor(LanguageTestParserVisitor):
    RASH_C_TYPE_MAP = {
        "int": "int",
        "float": "float",
        "str": "char*",
        "bool": "bool",
        "void": "void",
    }

    SCOPE_TRANSLATOR = {
        "public": "",
        "protected": "pr_",
        "private": "pv_",
    }

    INDENT_SIZE = 4

    typedefs = []
    static_vars = []
    function_prototypes = []
    current_class = ""
    entry_point = ""

    indent = 0

    # TODO: Variables
    # Variables that are in scope must be stored with their types,
    # e.g. for printf() function
    variables = {}
    libraries = set()

    def visitParse(self, ctx):
        program = self.visitChildren(ctx)
        libraries = "\n".join([f"#include<{lib}>" for lib in self.libraries])
        typedefs = "\n".join(self.typedefs)
        static_vars = "\n".join(self.static_vars)
        prototypes = "\n".join(self.function_prototypes)
        program_parts = [libraries, typedefs, program, static_vars, prototypes, self.entry_point]

        return "\n\n".join(program_parts)

    def visitImportStatement(self, ctx: LanguageTestParser.ImportStatementContext):
        # TODO: Imports
        # We need to manage import statements - 1. Do we import header files, or do that somehow else?
        # 2. How do we manage importing only specific functions from a file?
        # For now, this returns nothing, we must do it later.
        pass

    # Parts of parser that evaluate only to their text -----------------------------------------------------------------

    def visitNameIdentifier(self, ctx: LanguageTestParser.NameIdentifierContext):
        return ctx.getText()

    def visitSimpleTypeSpecifier(self, ctx: LanguageTestParser.SimpleTypeSpecifierContext):
        return ctx.getText()

    def visitIdentifier(self, ctx: LanguageTestParser.IdentifierContext):
        return ctx.getText()

    def visitUnaryOperator(self, ctx: LanguageTestParser.UnaryOperatorContext):
        return ctx.getText()

    def visitScope(self, ctx: LanguageTestParser.ScopeContext):
        return ctx.getText()

    # Uncategorized ----------------------------------------------------------------------------------------------------

    def visitTypeSpecifier(self, ctx: LanguageTestParser.TypeSpecifierContext):
        array_dim = 0 if not ctx.arrayBrackets() else len(ctx.arrayBrackets())
        if ctx.identifier():
            return self.visitIdentifier(ctx.identifier()) + array_dim * "*"
        else:
            return self.RASH_C_TYPE_MAP[self.visitSimpleTypeSpecifier(ctx.simpleTypeSpecifier())] + array_dim * "*"

    def visitCodeBlock(self, ctx: LanguageTestParser.CodeBlockContext):
        return "{\n" + "\n".join(str(self.visitStatement(s)) for s in ctx.statement()) + "\n}"

    # Classes ----------------------------------------------------------------------------------------------------------

    def visitClassDefinition(self, ctx: LanguageTestParser.ClassDefinitionContext):

        class_name = self.visitIdentifier(ctx.nameIdentifier())
        self.current_class = class_name

        self.typedefs.append(f"typedef struct s_{class_name} {class_name};")

        c_class_definition = f"struct s_{class_name}"
        c_class_definition += self.visitClassBody(ctx.classBody())
        c_class_definition += f";\n"
        self.createNewMethod(ctx)

        return c_class_definition

    def createNewMethod(self, ctx: LanguageTestParser.ClassDefinitionContext):
        c_method_new = ""
        params = ""
        args = ""
        has_init = False

        class_name = self.visitIdentifier(ctx.nameIdentifier())
        class_body = ctx.classBody()
        methods_declarations = class_body.classMethodDefinition()

        for methods_declaration in methods_declarations:
            if methods_declaration.KW_STATIC() is not None:
                continue

            scope = self.visitScope(methods_declaration.scope())
            function_definition = methods_declaration.functionDefinition()
            function_name = self.visitIdentifier(function_definition.nameIdentifier())
            c_method_new += f"    obj.{function_name} = " \
                            f" {self.current_class}_{self.SCOPE_TRANSLATOR[scope]}{function_name};\n"

            if function_name == '__init__':
                has_init = True
                param_declaration_list = function_definition.functionParams().paramDeclarationList()
                params = self.visitParamDeclarationList(param_declaration_list, True)
                args = ','.join([param.split(' ')[-1] for param in params.split(',')])
                print(args)

        c_method_new = f"{class_name}* new__{class_name}({params}) {{\n" \
                       f"    {class_name}* obj = ({class_name}*) malloc(sizeof({class_name});\n" + c_method_new

        if has_init:
            c_method_new += f"    obj.__init__(obj,{args});\n"
        c_method_new += f"    return obj; \n"
        c_method_new += "}\n"

        self.function_prototypes.append(c_method_new)

    def visitClassBody(self, ctx: LanguageTestParser.ClassBodyContext):
        c_class_body = " {\n"

        for attributeDeclaration in ctx.classAttributeDeclaration():
            c_class_body += self.visitClassAttributeDeclaration(attributeDeclaration)

        for methodDeclaration in ctx.classMethodDefinition():
            c_class_body += self.visitClassMethodDefinition(methodDeclaration)

        c_class_body += "}"

        return c_class_body

    def visitClassAttributeDeclaration(self, ctx: LanguageTestParser.ClassAttributeDeclarationContext):
        var_decl_statement = ctx.variableDeclStatement()
        var_type = self.visitTypeSpecifier(var_decl_statement.typeSpecifier())
        var_identifier = self.visitNameIdentifier(var_decl_statement.nameIdentifier())
        var_expression = self.visitExpression(
            var_decl_statement.expression()) if var_decl_statement.expression() else None
        var_scope = self.visitScope(ctx.scope())

        if ctx.KW_STATIC():
            if var_expression:
                self.static_vars.append(
                    f"{var_type} {self.SCOPE_TRANSLATOR[var_scope] + var_identifier} = {var_expression};\n"
                )
            else:
                self.static_vars.append(
                    f"{var_type} {self.SCOPE_TRANSLATOR[var_scope] + var_identifier};\n"
                )
            return ""

        # TODO solve the situation when we declare and initialize attribute -> method new?
        return f"    {var_type} {self.SCOPE_TRANSLATOR[var_scope] + var_identifier};\n"

    # Functions and methods --------------------------------------------------------------------------------------------

    def visitClassMethodDefinition(self, ctx: LanguageTestParser.ClassMethodDefinitionContext):
        static = ctx.KW_STATIC() is not None
        method_scope = self.visitScope(ctx.scope())
        return self.visitFunctionDefinition(ctx.functionDefinition(), method_scope, static)

    def visitFunctionDefinition(self, ctx: LanguageTestParser.FunctionDefinitionContext, scope: str = "public",
                                is_static: bool = False):

        function_name = self.visitIdentifier(ctx.nameIdentifier())
        function_return_type = self.visitFunctionReturnType(ctx.functionReturnType())
        function_params = self.visitFunctionParams(ctx.functionParams(), is_static)
        function_body = self.visitCodeBlock(ctx.codeBlock())

        if function_name == "main" and is_static:
            self.entry_point = f"\nint main(int argc, {function_params[1:]} {function_body[:-1]}return 0;\n}}"
            return ""

        in_class_name = f"{self.SCOPE_TRANSLATOR[scope]}{function_name}"
        global_name = f"{self.current_class}_{in_class_name}"

        if is_static:
            self.function_prototypes.append(
                f"{function_return_type} {in_class_name}{function_params} {function_body}\n"
            )
            return ""

        self.function_prototypes.append(
            f"{function_return_type} {global_name}{function_params} {function_body}\n"
        )

        return f"    {function_return_type} (*{in_class_name}){function_params};\n"

    def visitFunctionReturnType(self, ctx: LanguageTestParser.FunctionReturnTypeContext):
        return self.visitTypeSpecifier(ctx.typeSpecifier())

    def visitFunctionParams(self, ctx: LanguageTestParser.FunctionParamsContext, is_static: bool = False):
        c_params = f"({self.visitParamDeclarationList(ctx.paramDeclarationList(), is_static)})"
        return c_params

    def visitParamDeclarationList(self, ctx: LanguageTestParser.ParamDeclarationListContext, is_static: bool = False):
        param_declarations = []

        if not is_static:
            param_declarations.append(f"{self.current_class}* self")

        # This checks if there are any parameters
        if ctx:
            for param_decl in ctx.paramDeclaration():
                param_declarations.append(self.visitParamDeclaration(param_decl))

        return ",".join(param_declarations)

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
            self.libraries.add("stdio.h")

            expr = ctx.expression(0)
            expr_value = self.visitExpression(expr)

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
