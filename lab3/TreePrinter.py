from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print("| " * indent + "ERROR")

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))
    
    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("| " * indent + str(self.name))
    
    @addToClass(AST.Array)
    def printTree(self, indent=0):
        print("| " * indent + str(self.name))
        self.indices.printTree(indent+1)
    
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("| " * indent + str(self.op))
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        print("| " * indent + str(self.op))
        self.left.printTree(indent+1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        print("| " * indent + str(self.op))
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)
    
    @addToClass(AST.AssignExpr)
    def printTree(self, indent=0):
        print("| " * indent + str(self.op))
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)
    
    @addToClass(AST.IfExpr)
    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.cond.printTree(indent+1)
        print("| " * indent + "THEN")
        self.true.printTree(indent+1)
        print("| " * indent + "ELSE")
        self.false.printTree(indent+1)

    @addToClass(AST.WhileExpr)
    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.cond.printTree(indent+1)
        print("| " * indent + "DO")
        self.body.printTree(indent+1)

    @addToClass(AST.ForExpr)
    def printTree(self, indent=0):
        print("| " * indent + "FOR")
        self.var.printTree(indent+1)
        print("| " * indent + "RANGE")
        self.range.printTree(indent+1)
        print("| " * indent + "DO")
        self.body.printTree(indent+1)
    
    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("| " * indent + "RANGE")
        self.start.printTree(indent+1)
        self.end.printTree(indent+1)
    
    @addToClass(AST.RangeStep)
    def printTree(self, indent=0):
        print("| " * indent + "RANGE")
        self.start.printTree(indent+1)
        self.end.printTree(indent+1)
        self.step.printTree(indent+1)
    
    @addToClass(AST.BreakStmt)
    def printTree(self, indent=0):
        print("| " * indent + "BREAK")

    @addToClass(AST.ContinueStmt)
    def printTree(self, indent=0):
        print("| " * indent + "CONTINUE")

    @addToClass(AST.PrintStmt)
    def printTree(self, indent=0):
        print("| " * indent + "PRINT")
        self.expr.printTree(indent+1)

    @addToClass(AST.CompoundStmt)
    def printTree(self, indent=0):
        print("| " * indent + "COMPOUND")
        self.expr.printTree(indent+1)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        print("| " * indent + "PROGRAM")
        self.expr.printTree(indent+1)

    @addToClass(AST.Statements)
    def printTree(self, indent=0):
        print("| " * indent + "STATEMENTS")
        for expr in self.expr:
            expr.printTree(indent+1)
    @addToClass(AST.Expressions)
    def printTree(self, indent=0):
        print("| " * indent + "EXPRESSIONS")
        for expr in self.expr:
            expr.printTree(indent+1)


    # define printTree for other classes
    # ...

