import ply.lex as lex
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'print' : 'PRINT',
    'return' : 'RETURN',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'eye' : 'EYE',
    'zeros' : 'ZEROS',
    'ones' : 'ONES',
}
literals = ['+', '-', '*', '/', '(', ')', '[', ']', '{', '}', '=', '<', '>', ':', ',', ';', '\'']
tokens = [
    'ID', 'INTNUM', 'FLOATNUM', 'STRING',
    'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
    'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
    'LE', 'GE', 'NE', 'EQ',
    'IF', 'ELSE', 'WHILE', 'PRINT', 'RETURN', 'BREAK', 'CONTINUE',
    'EYE', 'ZEROS', 'ONES',
]

t_DOTADD = r'.\+'
t_DOTSUB = r'.-'
t_DOTMUL = r'.\*'
t_DOTDIV = r'./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_LE = r'<='
t_GE = r'>='
t_NE = r'!='
t_EQ = r'=='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_FLOATNUM(t):
    r'[0-9]+\.[0-9]*|[0-9]*\.[0-9]+'
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t



def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_WHITE(t):
    r'[ \t]+'
    pass

# tokens = ('NUMBER', 'ID' )

# literals = [ '+','-','*','/','(',')' ]

# def t_NUMBER(t):
#     r'\d+'
#     t.value = int(t.value)
#     return t

# def t_ID(t):
#     r'[a-zA-Z_]\w*'
#     return t

t_ignore = '  \t'

# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)

def t_error(t) :
    print ("Illegal character '%s'" , t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()


