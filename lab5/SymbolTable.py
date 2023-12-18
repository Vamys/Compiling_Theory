from enum import Enum, auto

class Type(Enum):
    INTNUM = auto()
    FLOATNUM = auto()
    STRING = auto()
    VECTOR = auto()
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
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size

class SymbolTable(object):

    def __init__(self, parent, name): 
        self.parent = parent
        self.name = name
        self.scope = {}

    def print_scope(self):
        for k in self.scope:
            print(k, " type: ", self.scope[k].type, " size: ", self.scope[k].size)

    def put(self, name, symbol):
        self.scope[name] = symbol

    def get(self, name): 
        var_symbol = self.scope.get(name)
        if var_symbol is not None:
            return var_symbol
        if self.parent is not None:
            return self.parent.get(name)
        return None

    def is_loop(self):
        if self.name == "loop":
            return True
        if self.parent == None:
            return False
        return self.parent.is_loop()

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent


