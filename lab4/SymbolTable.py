from enum import Enum, auto

class Type(Enum):
    INTNUM = auto()
    FLOATNUM = auto()
    STRING = auto()
    LIST = auto()
    MATRIX = auto()
    BOOLEAN = auto()
    RANGE = auto()
    NULL = auto()
    UNKNOWN = auto()
    
    @staticmethod
    def is_numeric(mtype):
        return mtype in [Type.FLOATNUM, Type.INTNUM]

class Symbol:
    pass

class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type
    #


#link lista scopow
class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.scope = {}
        #pass
    #

    def print_scope(self):
        for k in self.scope:
            print(k, " type: ", self.scope[k].type)

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.scope[name] = symbol
        #pass
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        var_symbol = self.scope.get(name)
        if var_symbol is not None:
            return var_symbol
        if self.parent is not None:
            return self.parent.get(name)
        return None
    #

    # def getParentScope(self):
    #     return self.parent
    #     #pass
    #

    def pushScope(self, name):
        return SymbolTable(self, name)
        #pass
    #

    def popScope(self):
        return self.parent
        #pass
    #

