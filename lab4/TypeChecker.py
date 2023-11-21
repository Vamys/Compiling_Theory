from TreePrinter import addToClass
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

@addToClass(AST.Node)
def accept(self, visitor):
    return visitor.visit(self)


class TypeChecker(NodeVisitor):

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op
        if type1 == type2 and type1 in ['int', 'float']:
            if op in ['+', '-', '*', '/']:
                return type1
            elif op in ['<', '>', '==', '!=']:
                return 'bool'
            else:
                print("Unsupported operator")
                return 'error'
        elif (type1 == "int" and type2 == "float") or (type1 == "float" and type2 == "int"):
            if op in ['+', '-', '*', '/']:
                return 'float'
            elif op in ['<', '>', '==', '!=']:
                return 'bool'
            else:
                print("Unsupported operator")
                return 'error'
        elif type1 == type2 and type1 in ['bool']:
            if op in ['==', '!=']:
                return 'bool'
            else:
                print("Unsupported operator")
                return 'error'
        elif type(type1) == type(type2) == tuple and type1[0] == type2[0] == 'list': #('list','int' or 'float', size x, sizy y)
            if op in ['.+', '.-', '.*', './']:
                if type1[2] != type2[2] or type1[3] != type2[3]:
                    print("Unsupported shape")
                    return 'error'
                elif type1[1] == type2[1]:
                    return type1
                return ('list', 'float', type1[2], type1[3])
            elif op == '*':
                if type1[2] != type2[3]:
                    print("Unsupported shape")
                    return 'error'
                elif type1[1] == type2[1]:
                    return ('list', type1[1], type1[2], type2[3])
                return ('list', 'float', type1[2], type2[3])
            elif op == '/':
                if type1[2] != type2[2] or type1[3] != type2[3]:
                    print("Unsupported shape")
                    return 'error'
                elif type1[1] == type2[1]:
                    return ('list', type1[1], type1[2], type1[3])
                return ('list', 'float', type1[2], type1[3])
        else:
            print("Unsupported type")
            return 'error'

    def visit_Variable(self, node):
        pass
        

