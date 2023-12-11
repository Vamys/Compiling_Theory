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
        
    # def visit_BinExpr(self, node):
    #                                       # alternative usage,
    #                                       # requires definition of accept method in class Node
    #     type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
    #     type2 = self.visit(node.right)    # type2 = node.right.accept(self)
    #     op    = node.op
    #     if type1 == type2 and type1 in ['int', 'float']:
    #         if op in ['+', '-', '*', '/']:
    #             return type1
    #         elif op in ['<', '>', '==', '!=']:
    #             return 'bool'
    #         else:
    #             print("Unsupported operator")
    #             return 'error'
    #     elif (type1 == "int" and type2 == "float") or (type1 == "float" and type2 == "int"):
    #         if op in ['+', '-', '*', '/']:
    #             return 'float'
    #         elif op in ['<', '>', '==', '!=']:
    #             return 'bool'
    #         else:
    #             print("Unsupported operator")
    #             return 'error'
    #     elif type1 == type2 and type1 in ['bool']:
    #         if op in ['==', '!=']:
    #             return 'bool'
    #         else:
    #             print("Unsupported operator")
    #             return 'error'
    #     elif type(type1) == type(type2) == tuple and type1[0] == type2[0] == 'list': #('list','int' or 'float', size x, sizy y)
    #         if op in ['.+', '.-', '.*', './']:
    #             if type1[2] != type2[2] or type1[3] != type2[3]:
    #                 print("Unsupported shape")
    #                 return 'error'
    #             elif type1[1] == type2[1]:
    #                 return type1
    #             return ('list', 'float', type1[2], type1[3])
    #         elif op == '*':
    #             if type1[2] != type2[3]:
    #                 print("Unsupported shape")
    #                 return 'error'
    #             elif type1[1] == type2[1]:
    #                 return ('list', type1[1], type1[2], type2[3])
    #             return ('list', 'float', type1[2], type2[3])
    #         elif op == '/':
    #             if type1[2] != type2[2] or type1[3] != type2[3]:
    #                 print("Unsupported shape")
    #                 return 'error'
    #             elif type1[1] == type2[1]:
    #                 return ('list', type1[1], type1[2], type1[3])
    #             return ('list', 'float', type1[2], type1[3])
    #     else:
    #         print("Unsupported type")
    #         return 'error'

    def error(self, position, desc):
        self.found_error = True
        print(f"Semantic error at [line: {position}]: {desc}")

    def visit_IntNum(self, node):
        node.type = Type.INTNUM
    
    def visit_FloatNum(self, node):
        node.type = Type.FLOATNUM

    def visit_Variable(self, node):
        node.type = Type.UNKNOWN
    
    def visit_ArrayElement(self, node):
        self.visit(node.indices)
        if node.indices.type != Type.LIST:
            self.error(node.position, "array indices must be list.")

        if node.indices.type != Type.INTNUM:
            self.error(node.position, "array indices must be a list of integers.")
        #Check if variable exist and type, return that type
        #return that type
        node.type = Type.INTNUM

    def visit_BinExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)
        # logic
        if node.op in ['LE', 'GE', 'NE', 'EQ', '<', '>']:
            if node.left.type != Type.BOOLEAN or node.right.type != Type.BOOLEAN:
                self.error(node.position, "operands in logic expression must be booleans.")
                return 
            node.type = Type.BOOLEAN
        elif node.op in ['DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV']:
            if node.left.type != Type.MATRIX or node.right.type != Type.MATRIX:
                self.error(node.position, "operands must be matrices.")
                return 
            #Check sizes types can  change if numeric
            node.type = Type.MATRIX
        elif node.op in ['+', '-', '*', '/']:
            if (not Type.is_numeric(node.left.type)) or (not Type.is_numeric(node.right.type)):
                self.error(node.position, "operands must be numeric.")
                return 
            if node.left.type == Type.FLOATNUM or node.right.type == Type.FLOATNUM:
                node.type = Type.FLOATNUM
            else:
                node.type = Type.INTNUM

    def visit_AssignExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)

        if type(node.left) is AST.Variable:
            self.symbol_table.put(node.left.name, VariableSymbol(node.left.name, node.right.type))
            return #mogloby zwracac typ
        elif type(node.left) is AST.ArrayElement:
            if self.symbol_table.get(node.left.name) is None:
                self.error(node.position, "matrix not initialized.")
                return 
            
    def visit_UnaryExpr(self, node):
        self.visit(node.left)

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
        self.visit(node.size)
            
    def visit_Transposition(self, node):
        self.visit(node.expr)

    def visit_List(self, node):
        self.visit(node.expr)
            

