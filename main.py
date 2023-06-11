from gen.LanguageTestLexer import LanguageTestLexer
from gen.LanguageTestParser import LanguageTestParser

from antlr4 import *
import sys

from testVisitor import RashVisitor


def main():
    try:
        input_filename = sys.argv[1]
    except:
        input_filename = 'RASHexamples/codeGenTest.rash'

    try:
        output_dir = sys.argv[2]
    except:
        output_dir = 'codeGenTest.rash.c'

    in_file = FileStream(input_filename)
    lexer = LanguageTestLexer(in_file)
    stream = CommonTokenStream(lexer)
    parser = LanguageTestParser(stream)
    tree = parser.parse()

    visitor = RashVisitor(output_dir)
    visitor.visit(tree)

if __name__ == '__main__':
    main()