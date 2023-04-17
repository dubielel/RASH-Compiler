from gen.LanguageTestParser import LanguageTestParser
from gen.LanguageTestParserListener import LanguageTestParserListener
class RASHTestListener(LanguageTestParserListener):

    def enterParse(self, ctx: LanguageTestParser.ParseContext):
        print("enterParse")

    def exitParse(self, ctx: LanguageTestParser.ParseContext):
        print("exitParse")

    def enterImportStatement(self, ctx: LanguageTestParser.ImportStatementContext):
        print("enterImportStatement")
        print(ctx.getText())
