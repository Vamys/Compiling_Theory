class Node(object):
    def __init__(self, position):
        self.position = position
        self.type = None

    def accept(self, visitor):
        return visitor.visit(self)

class IntNum(Node):
    def __init__(self, value, position):
        super().__init__(position)
        self.value = value

class FloatNum(Node):
    def __init__(self, value, position):
        super().__init__(position)
        self.value = value

class Variable(Node):
    def __init__(self, name, position):
        super().__init__(position)
        self.name = name

class ArrayElement(Node):
    def __init__(self, name, indices, position):
        super().__init__(position)
        self.name = name
        self.indices = indices

class BinExpr(Node):
    def __init__(self, op, left, right, position):
        super().__init__(position)
        self.op = op
        self.left = left
        self.right = right

class UnaryExpr(Node):
    def __init__(self, left,op, position):
        super().__init__(position)
        self.op = op
        self.left = left

# class RelExpr(Node):
#     def __init__(self, op, left, right, position):
#         super().__init__(position)
#         self.op = op
#         self.left = left
#         self.right = right

class AssignExpr(Node):
    def __init__(self, op, left, right, position):
        super().__init__(position)
        self.op = op
        self.left = left
        self.right = right

class IfElseExpr(Node):
    def __init__(self, cond, true, false, position):
        super().__init__(position)
        self.cond = cond
        self.true = true
        self.false = false

class IfExpr(Node):
    def __init__(self, cond, true, position):
        super().__init__(position)
        self.cond = cond
        self.true = true

class WhileExpr(Node):
    def __init__(self, cond, body, position):
        super().__init__(position)
        self.cond = cond
        self.body = body

class ForExpr(Node):
    def __init__(self,var, range, body, position):
        super().__init__(position)
        self.var = var
        self.range = range
        self.body = body

class BreakStmt(Node):
    def __init__(self, position):
        super().__init__(position)
        pass

class ContinueStmt(Node):
    def __init__(self, position):
        super().__init__(position)
        pass

class ReturnStmt(Node):
    def __init__(self, expr, position):
        super().__init__(position)
        self.expr = expr

class PrintStmt(Node):
    def __init__(self, expr, position):
        super().__init__(position)
        self.expr = expr

class CompoundStmt(Node):
    def __init__(self, expr, position):
        super().__init__(position)
        self.expr = expr
    
class RangeExpr(Node):
    def __init__(self, start, end, position):
        super().__init__(position)
        self.start = start
        self.end = end

class ListExpr(Node):
    def __init__(self, expr_, position):
        super().__init__(position)
        self.expr = [expr_]
    def add(self, new_expr):
        self.expr.append(new_expr)

class ListInstr(Node):
    def __init__(self, instr, position):
        super().__init__(position)
        self.instr = [instr]
    def add(self, new_instr):
        self.instr.append(new_instr)

class MatrixCreate(Node):
    def __init__(self, type , size, position):
        super().__init__(position)
        self.type = type
        self.size = size
class Transposition(Node):
    def __init__(self, expr, position):
        super().__init__(position)
        self.expr = expr

class List(Node):
    def __init__(self, expr, position):
        super().__init__(position)
        self.expr = expr

class Error(Node):
    def __init__(self, position):
        super().__init__(position)
        pass


      
