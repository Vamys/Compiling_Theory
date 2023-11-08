class Node(object):
    pass

class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name

class Array(Node):
    def __init__(self, name, indices):
        self.name = name
        self.indices = indices

class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnaryExpr(Node):
    def __init__(self, op, left):
        self.op = op
        self.left = left

class RelExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class AssignExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class IfElseExpr(Node):
    def __init__(self, cond, true, false):
        self.cond = cond
        self.true = true
        self.false = false
class IfExpr(Node):
    def __init__(self, cond, true):
        self.cond = cond
        self.true = true
class WhileExpr(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class ForExpr(Node):
    def __init__(self,var, range, body):
        self.var = var
        self.range = range
        self.body = body

class BreakStmt(Node):
    def __init__(self):
        pass

class ContinueStmt(Node):
    def __init__(self):
        pass

class ReturnStmt(Node):
    def __init__(self, expr):
        self.expr = expr

class PrintStmt(Node):
    def __init__(self, expr):
        self.expr = expr

class CompoundStmt(Node):
    def __init__(self, expr):
        self.expr = expr
    
class RangeExpr(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class ListExpr(Node):
    def __init__(self, expr):
        self.expr = [expr]
    def add(self, expr):
        self.expr.append(expr)

class ListInstr(Node):
    def __init__(self, instr):
        self.instr = [instr]
    def add(self, instr):
        self.instr.append(instr)

class Error(Node):
    def __init__(self):
        pass
      
