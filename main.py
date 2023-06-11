from gen.LanguageTestLexer import LanguageTestLexer
from gen.LanguageTestParser import LanguageTestParser

from antlr4 import *
import sys
import os

from testVisitor import RASHTestVisitor


def main():
    try:
        input_filename = sys.argv[1]
    except:
        input_filename = 'RASHexamples/codeGenTest.rash'

    try:
        output_filename = sys.argv[2]
    except:
        output_filename = '.rashc/codeGenTest.rash.c'

    in_file = FileStream(input_filename)
    lexer = LanguageTestLexer(in_file)
    stream = CommonTokenStream(lexer)
    parser = LanguageTestParser(stream)
    tree = parser.parse()

    visitor = RASHTestVisitor("test")
    result = visitor.visit(tree)

    if not os.path.isdir('.rashc'):
        os.mkdir('.rashc')

    with open(output_filename, "w+") as f:
        f.write(result) 


if __name__ == '__main__':
    main()