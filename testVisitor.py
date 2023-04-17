from gen.LanguageTestParser import LanguageTestParser
from gen.LanguageTestParserVisitor import LanguageTestParserVisitor


class RASHTestVisitor(LanguageTestParserVisitor):

    RASH_C_TYPE_MAP = {
        "int": "int",
        "float": "float",
        "str": "char*",
        "bool": "bool",
        "void": "void"
    }

    def visitParse(self, ctx):

        return self.visitChildren(ctx)

    def visitVariableDeclStatement(self, ctx:LanguageTestParser.VariableDeclStatementContext):
        var_type = self.visitTypeSpecifier(ctx.typeSpecifier())
        var_identifier = self.visitIdentifier(ctx.nameIdentifier())
        var_value = self.visitExpression(ctx.expression())

        c_text = f"{var_type} {var_identifier} = {var_value};"

        return self.visitChildren(ctx)

    def visitExpression(self, ctx:LanguageTestParser.ExpressionContext):
        return ctx.getText()

    def visitIdentifier(self, ctx:LanguageTestParser.IdentifierContext):
        return ctx.getText()

    def visitTypeSpecifier(self, ctx:LanguageTestParser.TypeSpecifierContext):
        return ctx.getText()

    def visitClassDefinition(self, ctx:LanguageTestParser.ClassDefinitionContext):
        class_definition_c = f"typedef struct s_{self.visitIdentifier(ctx.identifier())}"
        class_definition_c += str(self.visitClassBody(ctx.classBody()))
        class_definition_c += f" {self.visitIdentifier(ctx.identifier())};"

        print(class_definition_c)

        return class_definition_c

    def visitClassBody(self, ctx:LanguageTestParser.ClassBodyContext):
        class_body = " {\n"
        for member in ctx.attributeDeclaration():
            class_body += self.visitAttributeDeclaration(member)
        class_body += "}"

        return class_body

    def visitAttributeDeclaration(self, ctx:LanguageTestParser.AttributeDeclarationContext):
        attribute_declaration = f"\t"
        attribute_declaration += self.RASH_C_TYPE_MAP[self.visitTypeSpecifier(ctx.typeSpecifier())] + " "

        if self.visitAccessModifier(ctx.accessModifier()) == "private":
            attribute_declaration += "__"

        attribute_declaration += f"{self.visitIdentifier(ctx.identifier())};\n"
        return attribute_declaration

    def visitAccessModifier(self, ctx:LanguageTestParser.AccessModifierContext):
        return ctx.getText()