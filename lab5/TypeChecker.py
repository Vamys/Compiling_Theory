import AST
from SymbolTable import Type, SymbolTable, VariableSymbol

class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):  
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.found_error = False
        self.symbol_table = SymbolTable(None, "program scope")

    def error(self, position, desc):
        self.found_error = True
        print(f"Semantic error at [line: {position}]: {desc}")

    def visit_IntNum(self, node):
        node.type = Type.INTNUM
    
    def visit_FloatNum(self, node):
        node.type = Type.FLOATNUM

    def visit_Variable(self, node):
        sym = self.symbol_table.get(node.name)
        if sym is not None:
            node.type = sym.type
            node.size = sym.size
            return
        node.type = Type.UNKNOWN
    
    def visit_ArrayElement(self, node):
        self.visit(node.indices)
        sym = self.symbol_table.get(node.name)
        
        if sym is None:
                self.error(node.position, "matrix not initialized.")
                return 
        if sym.type != Type.MATRIX:
            self.error(node.position, "must be a matrix.")
            return 
        if node.indices.type != Type.VECTOR:
            print('aaaa',node.indices.expr.expr)
            self.error(node.position, "array indices must be list.")
            return
        if node.indices.expr.expr[0].type != Type.INTNUM and node.indices.expr.expr[0].type != Type.RANGE: # sparawdzenie wszytskich
            self.error(node.position, "array indices must be intnums")
            return
        if len(node.indices.expr.expr) != 2:
            self.error(node.position, "wrong dimensions.")
            return
        if node.indices.expr.expr[0].type == Type.RANGE:
            if node.indices.expr.expr[0].start.value >= sym.size[0] or node.indices.expr.expr[0].end.value > sym.size[0]:
                self.error(node.position, "wrong indices.")
                return
            if node.indices.expr.expr[1].start.value >= sym.size[1] or node.indices.expr.expr[1].end.value > sym.size[1]:
                self.error(node.position, "wrong indices.")
                return
        elif node.indices.expr.expr[0].value >= sym.size[0] or node.indices.expr.expr[1].value >= sym.size[1]:
            self.error(node.position, "wrong indices.")
            return
        node.type = Type.INTNUM

    def visit_BinExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)
        if node.op in ['<=', '>=', '!=', '==', '<', '>']:
            if node.left.type == node.right.type == Type.STRING and node.op == '==': 
                #porównywanie stringów
                node.type = Type.BOOLEAN
                return
            if not Type.is_numeric(node.left.type) or not Type.is_numeric(node.right.type):
                self.error(node.position, "operands in expression must be numeric.")
                node.type = Type.BOOLEAN
                return 
            node.type = Type.BOOLEAN
            return
        elif node.op in ['.+', '.-', '.*', './']:
            if node.left.type != Type.MATRIX or node.right.type != Type.MATRIX:
                self.error(node.position, "wrong operands.")
                return 
            if node.left.size != node.right.size:
                self.error(node.position, "matrices must have equal size.")
                return
            node.type = Type.MATRIX
            node.size = node.left.size
            return 
        elif node.op in ['+', '-', '*', '/']:
            if node.left.type == node.right.type == Type.STRING and node.op == '+':
                node.type = Type.STRING
                return
            if (node.left.type == Type.STRING and node.right.type == Type.INTNUM) or \
                (node.left.type == Type.INTNUM and node.right.type == Type.STRING) and node.op == '*':
                #string multiplication 
                node.type = Type.STRING
                return

            if  Type.is_numeric(node.left.type) and  Type.is_numeric(node.right.type):
                if node.left.type == Type.FLOATNUM or node.right.type == Type.FLOATNUM:
                    node.type = Type.FLOATNUM
                else:
                    node.type = Type.INTNUM
                return
            if (node.left.type == node.right.type == Type.MATRIX):
                if node.op in['+', '-']:
                    if node.left.size != node.right.size:
                        self.error(node.position, "matrices must have equal size.")
                        return 
                else:
                    if node.left.size[1] != node.right.size[0]:
                        self.error(node.position, "wrong matrix sizes.")
                        return
                node.type = Type.MATRIX
                node.size = (node.left.size[0], node.left.size[1])
                return
        
        self.error(node.position, "wrong operands")
        #BRAKUJE MNOZENIA MACIERZY

    def visit_AssignExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)

        if type(node.left) is AST.Variable:
            if node.right.type is Type.MATRIX:
                self.symbol_table.put(node.left.name, VariableSymbol(node.left.name, Type.MATRIX, node.right.size))
                return 
            self.symbol_table.put(node.left.name, VariableSymbol(node.left.name, node.right.type, None))
            return
        elif type(node.left) is AST.ArrayElement:
            if self.symbol_table.get(node.left.name) is None:
                self.error(node.position, "matrix not initialized.")
                return 
            
    def visit_UnaryExpr(self, node):
        self.visit(node.left)
        node.type = node.left.type
        node.size = node.size

    def visit_IfElseExpr(self, node):
        self.visit(node.cond)
        self.symbol_table = self.symbol_table.pushScope("if")
        self.visit(node.true)
        self.symbol_table = self.symbol_table.popScope()

        self.symbol_table = self.symbol_table.pushScope("else")
        self.visit(node.false)
        self.symbol_table = self.symbol_table.popScope()

    def visit_IfExpr(self, node):
        self.symbol_table = self.symbol_table.pushScope("if")
        self.visit(node.cond)
        self.symbol_table = self.symbol_table.popScope()
        self.visit(node.true)       

    def visit_WhileExpr(self, node):
        self.visit(node.cond)
        self.symbol_table = self.symbol_table.pushScope("loop")
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()

    def visit_ForExpr(self, node):
        self.visit(node.range)
        self.symbol_table = self.symbol_table.pushScope("loop")
        self.symbol_table.put(node.var, VariableSymbol(node.var, Type.INTNUM, None))
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()

    def visit_BreakStmt(self, node):
        if not self.symbol_table.is_loop():
            self.error(node.position, "break outside loop.")
        return
    
    def visit_ContinueStmt(self, node):
        if not self.symbol_table.is_loop():
            self.error(node.position, "continue outside loop.")
        return

    def visit_ReturnStmt(self, node):
        self.visit(node.expr)

    def visit_PrintStmt(self, node):
        self.visit(node.expr)

    def visit_CompoundStmt(self, node):
        self.visit(node.expr)
            
    def visit_RangeExpr(self, node):
        node.type = Type.RANGE
        self.visit(node.start)
        self.visit(node.end)

    def visit_ListExpr(self, node):
        for e in node.expr:
            self.visit(e)

    def visit_ListInstr(self, node):
        for i in node.instr:
            self.visit(i)

    def visit_MatrixCreate(self, node):
        self.visit(node.arg) 
        if node.arg.type != Type.VECTOR:
            self.error(node.position, "wrong arguments.")
            return 
        
        #print("TYPE:", node.type)
        if node.type == 'zeros' or node.type == 'ones':
            node.type = Type.MATRIX
            if node.arg.size == 2:
                node.size = (node.arg.expr.expr[0].value, node.arg.expr.expr[1].value)
                return
            elif node.arg.size == 1:
                node.size = (node.arg.expr.expr[0].value, node.arg.expr.expr[0].value)
                return
        elif node.type == 'eye':
            node.type = Type.MATRIX
            if node.arg.size == 1:
                node.size = (node.arg.expr.expr[0].value, node.arg.expr.expr[0].value)
                return
        
        node.size = (0,0)
        self.error(node.position, "wrong arguments.")
        return 
        #node.type = Type.MATRIX
        #node.size = (node.arg.value, node.arg.value)
            
    def visit_Transposition(self, node):
        self.visit(node.expr)
        if node.expr.type != Type.MATRIX:
            self.error(node.position, "operand must be a matrix.")
            return
        node.type = Type.MATRIX
        node.size = (node.expr.size[1], node.expr.size[0])

    def visit_List(self, node):
        self.visit(node.expr)
        if Type.is_numeric(node.expr.expr[0].type) or node.expr.expr[0].type == Type.RANGE:
            node.type = Type.VECTOR
            node.size = len(node.expr.expr)
        if node.expr.expr[0].type == Type.VECTOR:
            firstD = node.expr.expr[0].size
            for vec in node.expr.expr:
                if firstD != vec.size:
                    self.error(node.position, "wrong matrix dimensions.")
                    return         
            node.type = Type.MATRIX
            node.size = (len(node.expr.expr), node.expr.expr[0].size)
        
    def visit_String(self, node):
        node.type = Type.STRING

