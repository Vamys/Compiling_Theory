
import sys
import ply.yacc as yacc
import Mparser as Mparser
import scanner
import AST
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)
        
 
    parser = Mparser.parser
    text = file.read()
    print(text)
    ast = parser.parse(text, lexer=scanner.lexer)
   
    ast.printTree()
        
    typeChecker = TypeChecker()   
    typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)

    #typeChecker.symbol_table.print_scope() # for debug