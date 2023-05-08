from gen.LanguageTestLexer import LanguageTestLexer
from gen.LanguageTestParser import LanguageTestParser
from gen.LanguageTestParserVisitor import LanguageTestParserVisitor
from gen.LanguageTestParserListener import LanguageTestParserListener
from antlr4 import *

from testVisitor import RASHTestVisitor


def main():
    in_file = FileStream('RASHexamples/codeGenTest.rash')
    lexer = LanguageTestLexer(in_file)
    stream = CommonTokenStream(lexer)
    parser = LanguageTestParser(stream)
    tree = parser.parse()

    # print(tree.toStringTree(recog=parser))

    # walker = ParseTreeWalker()
    # listener = RASHTestListener()
    # walker.walk(listener, tree)

    visitor = RASHTestVisitor()
    visitor.visit(tree)


if __name__ == '__main__':
    main()