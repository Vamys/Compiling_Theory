
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import operator
sys.setrecursionlimit(10000)


def dot_add(a,b):
    return [[a[i][j]+b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def dot_sub(a,b):
    return [[a[i][j]-b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def dot_mul(a,b):
    return [[a[i][j]*b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def dot_div(a,b):
    return [[a[i][j]/b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

operators = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '>=': operator.ge,
    '<=': operator.le,
    '<' : operator.lt,
    '>' : operator.gt,
    '!=': operator.ne,
    '==': operator.eq,
    '+=': operator.iadd,
    '-=': operator.isub,
    '*=': operator.imul,
    '/=': operator.itruediv,
    '&&': operator.and_,
    '||': operator.or_,
    '.+': lambda a,b: dot_add(a,b),
    '.-': lambda a,b: dot_sub(a,b),
    '.*': lambda a,b: dot_mul(a,b),
    './': lambda a,b: dot_div(a,b)
}

class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)
    
    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)
    
    @when(AST.Variable)
    def visit(self, node):
        return self.memory.get(node.name)
    
    @when(AST.ArrayElement)
    def visit(self, node):
        matrix = self.memory.get(node.name)
        indices = node.indices.accept(self)
        if indices[0] < 0 or indices[1] < 0 or indices[0] >= len(matrix) or indices[1] >= len(matrix[0]):
            raise Exception("Index out of range")
        return matrix[indices[0]][indices[1]]
    
    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        if isinstance(r1, list) and isinstance(r2, list) and node.op == '*':
            result = [[0 for _ in range(len(r2[0]))] for _ in range(len(r1))]
            for i in range(len(r1)):
                for j in range(len(r2[0])):
                    for k in range(len(r2)):
                        result[i][j] += r1[i][k] * r2[k][j]
            return result
        return operators[node.op](r1,r2)

    @when(AST.UnaryExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        if node.op == '-':
            return -r1
        elif node.op == '!':
            return not r1
        return operators[node.op](r1)

    @when(AST.AssignExpr)
    def visit(self, node):
        r1 = node.right.accept(self)
        # print('assign',node.left.name)
        if type(node.left) is AST.Variable:
            if node.op == '=':
                self.memory.set(node.left.name, r1)
            else:
                self.memory.set(node.left.name, operators[node.op](self.memory.get(node.left.name), r1))
        elif type(node.left) is AST.ArrayElement:
            matrix = self.memory.get(node.left.name)
            indices = node.left.indices.accept(self)
            if type(indices[0]) is int:
                matrix[indices[0]][indices[1]] = r1
            elif type(indices[0]) is range:
                for i in indices[0]:
                    for j in indices[1]:
                        matrix[i][j] = r1

    @when(AST.IfElseExpr)
    def visit(self, node):
        cond = node.cond.accept(self)
        if cond:
            self.memory.push(Memory("if"))
        else:
            self.memory.push(Memory("else"))
        try:
            node.false.accept(self)
        except BreakException or ContinueException:
            raise("Break or continue not in loop")
        finally:
            self.memory.pop()
    
    @when(AST.IfExpr)
    def visit(self, node):
        cond = node.cond.accept(self)
        if cond:
            self.memory.push(Memory("if"))
            try:
                node.true.accept(self)
            except BreakException or ContinueException:
                raise("Break or continue not in loop")
            finally:
                self.memory.pop()
            
    @when(AST.WhileExpr)
    def visit(self, node): #zleee
        self.memory.push(Memory("while loop"))
        while node.cond.accept(self):
            try:
                node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory.pop()

    @when(AST.ForExpr)
    def visit(self,node): 
        iterator = node.var
        loop_range = node.range.accept(self)
        if len(loop_range) == 0:
            return
        self.memory.push(Memory("for loop"))
        self.memory.set(iterator, loop_range[0])
        while self.memory.get(iterator) in loop_range:
            try:
                node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
            finally:
                self.memory.set(iterator, self.memory.get(iterator) + 1)
        self.memory.pop()

    @when(AST.BreakStmt)
    def visit(self, node):
        raise BreakException()
        
    
    @when(AST.ContinueStmt)
    def visit(self, node):
        raise ContinueException()
    
    @when(AST.ReturnStmt)
    def visit(self, node):
        raise ReturnValueException(node.expr.accept(self))
    
    @when(AST.PrintStmt)
    def visit(self, node):
        to_print = node.expr.accept(self)
        print(*to_print, sep='')
        

    @when(AST.CompoundStmt)
    def visit(self, node):
        if type(node.expr) == list:
            for instruction in node.expr:
                instruction.accept(self)
        else:
            node.expr.accept(self)
    
    @when(AST.RangeExpr)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return range(start, end)
    
    @when(AST.ListExpr)
    def visit(self, node):
        return [expression.accept(self) for expression in node.expr]
    
    @when(AST.ListInstr)
    def visit(self, node):
        temp = []
        for instruction in node.instr:
            # print('NEXT INSTRUCTION',instruction.__class__.__name__)
            temp.append(instruction)
            instruction.accept(self)
            # print('------------------')
        return temp
    
    @when(AST.MatrixCreate)
    def visit(self, node):
        arg = node.arg.accept(self)
        if len(arg) == 1:
            dim1,dim2 = arg[0],arg[0]
        else :
            dim1,dim2 = arg[0],arg[1]
        if node.func == 'zeros':
            return [[0 for _ in range(dim2)] for _ in range(dim1)]
        elif node.func == 'ones':
            return [[1 for _ in range(dim2)] for _ in range(dim1)]
        elif node.func == 'eye':
            return [[1 if i == j else 0 for j in range(dim2)] for i in range(dim1)]
        else:
            raise Exception("Wrong matrix type") 
    
    @when(AST.Transposition)
    def visit(self, node):
        matrix = node.expr.accept(self)
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    
    @when(AST.List)
    def visit(self, node):
        return [i for i in node.expr.accept(self)]
    
    @when(AST.Error)
    def visit(self, node):
        raise Exception("Error node found")
    
    @when(AST.String)
    def visit(self, node):
        return node.expr