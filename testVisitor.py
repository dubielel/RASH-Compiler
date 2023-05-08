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
        "protected": "_",
        "private": "__",
    }

    current_class = ""
    function_prototypes = []

    def visitParse(self, ctx):
        res = self.visitChildren(ctx)
        for prototype in self.function_prototypes:
            print(prototype)
        print(res)
        return res

    def visitImportStatement(self, ctx:LanguageTestParser.ImportStatementContext):
        # TODO: Imports
        # We need to manage import statements - 1. Do we import header files, or do that somehow else?
        # 2. How do we manage importing only specific functions from a file?
        # For now, this returns nothing, we must do it later.
        pass

    def visitExpression(self, ctx:LanguageTestParser.ExpressionContext):
        return ctx.getText()

    def visitIdentifier(self, ctx:LanguageTestParser.IdentifierContext):
        return ctx.getText()

    def visitTypeSpecifier(self, ctx:LanguageTestParser.TypeSpecifierContext):
        return ctx.getText()

    def visitScope(self, ctx:LanguageTestParser.ScopeContext):
        return ctx.getText()

    def visitCodeBlock(self, ctx:LanguageTestParser.CodeBlockContext):
        return "{\n\n}"

    def visitClassDefinition(self, ctx:LanguageTestParser.ClassDefinitionContext):

        class_name = self.visitIdentifier(ctx.nameIdentifier())
        self.current_class = class_name

        c_class_definition = f"typedef struct s_{class_name}"
        c_class_definition += self.visitClassBody(ctx.classBody())
        c_class_definition += f" {class_name};"

        return c_class_definition

    def visitClassBody(self, ctx:LanguageTestParser.ClassBodyContext):

        # TODO: Static
        # What do we do with static methods? Or variables? How do we implement them?
        # For now, we just ignore them. But we need to do something about them later.

        c_class_body = " {\n"

        for attributeDeclaration in ctx.classAttributeDeclaration():
            c_class_body += self.visitClassAttributeDeclaration(attributeDeclaration)

        for methodDeclaration in ctx.classMethodDefinition():
            c_class_body += self.visitClassMethodDefinition(methodDeclaration)

        c_class_body += "}"

        return c_class_body

    def visitClassAttributeDeclaration(self, ctx:LanguageTestParser.ClassAttributeDeclarationContext):
        var_type = self.visitTypeSpecifier(ctx.typeSpecifier())
        var_scope = self.visitScope(ctx.scope())
        var_identifier = self.visitIdentifier(ctx.identifier())

        c_class_attribute_declaration = f"    {var_type} {self.SCOPE_TRANSLATOR[var_scope] + var_identifier};\n"
        return c_class_attribute_declaration

    def visitClassMethodDefinition(self, ctx:LanguageTestParser.ClassMethodDefinitionContext):
        method_scope = self.visitScope(ctx.scope())
        return self.visitFunctionDefinition(ctx.functionDefinition(), True, method_scope)

    def visitFunctionDefinition(self, ctx:LanguageTestParser.FunctionDefinitionContext, class_method=False,
                                scope="public"):

        function_name = self.visitIdentifier(ctx.nameIdentifier())
        function_return_type = self.visitFunctionReturnType(ctx.functionReturnType())
        function_params = self.visitFunctionParams(ctx.functionParams())
        function_body = self.visitCodeBlock(ctx.codeBlock())

        if class_method:
            global_name = f"{self.current_class}_{function_name}"
            in_class_name = f"{self.SCOPE_TRANSLATOR[scope]}{function_name}"

            self.function_prototypes.append(
                f"{function_return_type} {global_name}{function_params} {function_body}\n"
            )

            return f"    {function_return_type} (*{in_class_name}){function_params};\n"

        # TODO: Function definitions
        # We don't even have function definitions outside of classes, right?
        # That means we can remove class_method?

        return ""

    def visitFunctionReturnType(self, ctx:LanguageTestParser.FunctionReturnTypeContext):
        return self.visitTypeSpecifier(ctx.typeSpecifier())

    def visitFunctionParams(self, ctx:LanguageTestParser.FunctionParamsContext):
        c_params = f"({self.current_class} *self"
        return c_params + ")"

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is None and nextResult is None:
            return None
        if aggregate is None:
            return nextResult
        elif nextResult is None:
            return aggregate
        else:
            return str(aggregate) + str(nextResult)

"""
def visitVariableDeclStatement(self, ctx:LanguageTestParser.VariableDeclStatementContext):
    var_type = self.visitTypeSpecifier(ctx.typeSpecifier())
    var_identifier = self.visitIdentifier(ctx.nameIdentifier())
    var_value = self.visitExpression(ctx.expression())

    c_text = f"{var_type} {var_identifier} = {var_value};"
    print(c_text)

    return self.visitChildren(ctx)
"""