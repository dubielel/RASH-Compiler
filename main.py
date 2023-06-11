from gen.LanguageTestLexer import LanguageTestLexer
from gen.LanguageTestParser import LanguageTestParser

from antlr4 import *

from testVisitor import RASHTestVisitor


def main():
    in_file = FileStream('RASHexamples/codeGenTest.rash')
    lexer = LanguageTestLexer(in_file)
    stream = CommonTokenStream(lexer)
    parser = LanguageTestParser(stream)
    tree = parser.parse()

    visitor = RASHTestVisitor("test")
    result = visitor.visit(tree)
    with open("result.c", "w+") as f:
        f.write(result) 


if __name__ == '__main__':
    main()