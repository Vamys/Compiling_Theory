import AST
from SymbolTable import Type, SymbolTable, VariableSymbol

class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
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

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)

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
        if node.indices.type != Type.VECTOR:
            self.error(node.position, "array indices must be list.")
        if node.indices.type != Type.INTNUM:
            self.error(node.position, "array indices must be a list of integers.")
        node.type = Type.INTNUM

    def visit_BinExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)
        if node.op in ['<=', '>=', '!=', '==', '<', '>']:
            if not Type.is_numeric(node.left.type) or not Type.is_numeric(node.right.type):
                self.error(node.position, "operands in expression must be numeric.")
                node.type = Type.BOOLEAN
                return 
            node.type = Type.BOOLEAN
        elif node.op in ['.+', '.-', '.*', './']:
            if node.left.type != Type.MATRIX or node.right.type != Type.MATRIX:
                self.error(node.position, "operands must be matrices.")
                return 
            if node.left.size != node.right.size:
                self.error(node.position, "matrices must have equal size.")
                return
            node.type = Type.MATRIX
            node.size = node.left.size
        elif node.op in ['+', '-', '*', '/']:
            if (not Type.is_numeric(node.left.type)) or (not Type.is_numeric(node.right.type)):
                self.error(node.position, "operands must be numeric.")
                return 
            if node.left.type == Type.FLOATNUM or node.right.type == Type.FLOATNUM:
                node.type = Type.FLOATNUM
            else:
                node.type = Type.INTNUM
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

    def visit_IfElseExpr(self, node):
        self.visit(node.cond)
        self.visit(node.true)
        self.visit(node.false)

    def visit_IfExpr(self, node):
        self.visit(node.cond)
        self.visit(node.true)       

    def visit_WhileExpr(self, node):
        self.visit(node.cond)
        self.visit(node.body)

    def visit_ForExpr(self, node):
        self.visit(node.var)
        self.visit(node.range)
        self.visit(node.body)

    def visit_BreakStmt(self, node):
        return
    
    def visit_ContinueStmt(self, node):
        pass

    def visit_ReturnStmt(self, node):
        self.visit(node.expr)

    def visit_PrintStmt(self, node):
        self.visit(node.expr)

    def visit_CompoundStmt(self, node):
        self.visit(node.expr)
            
    def visit_RangeExpr(self, node):
        self.visit(node.start)
        self.visit(node.end)

    def visit_ListExpr(self, node):
        for e in node.expr:
            self.visit(e)

    def visit_ListInstr(self, node):
        for i in node.instr:
            self.visit(i)

    def visit_MatrixCreate(self, node):
        self.visit(node.arg) #OTHER NAME
        node.type = Type.MATRIX
        node.size = (node.arg.value, node.arg.value)
            
    def visit_Transposition(self, node):
        self.visit(node.expr)

    def visit_List(self, node):
        self.visit(node.expr)
        #checks to do
        if Type.is_numeric(node.expr.expr[0].type):
            node.type = Type.VECTOR
            node.size = len(node.expr.expr)
        if node.expr.expr[0].type == Type.VECTOR:
            node.type = Type.MATRIX
            node.size = (len(node.expr.expr), node.expr.expr[0].size)
            

