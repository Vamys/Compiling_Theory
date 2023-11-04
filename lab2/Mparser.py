#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
   ('nonassoc', 'IFX'),
   ('nonassoc', 'ELSE'),
   ('nonassoc', '!'),
   ("left", '+', '-'),
   ("left", '*', '/'),
   ("left", 'DOTMUL', 'DOTDIV'),
   ("left", 'DOTADD', 'DOTSUB'),
   ("left", '<', '>', "NE", "GE", "LE", "EQ", ':')
)

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

def p_program(p):
    """program : instructions_opt"""

def p_instructions_opt_1(p):
    """instructions_opt : instructions """

def p_instructions_opt_2(p):
    """instructions_opt : """

def p_instructions_1(p):
    """instructions : instructions instruction """

def p_instructions_2(p):
    """instructions : instruction """

# to finish the grammar
# ....

def p_instruction(p):
    """instruction : expression ';'
                   | assignment ';'
                   | if_statement 
                   | while_statement
                   | break_statement ';'
                   | continue_statement ';'
                   | return_statement ';'
                   | print_statement ';'
                   | for_statement
                   | compound_statement"""

def p_compound_statement(p):
   """compound_statement : '{' instructions_opt '}'"""
    
def p_expression(p):
        """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression
                  | expression LE expression
                  | expression GE expression
                  | expression NE expression
                  | expression EQ expression
                  | expression '<' expression
                  | expression '>' expression
                  | '(' expression ')'
                  | '[' expression_list ']'
                  | ZEROS '(' expression ')'
                  | ONES '(' expression ')'
                  | EYE '(' expression ')'
                  | '!' expression
                  | '-' expression
                  | ID
                  | ID '[' expression_list ']'
                  | INTNUM
                  | FLOATNUM
                  | STRING
                  | expression '\\''
                  """
    #if p[2] == '+'   : p[0] = p[1] + p[3]
    #if p[2] == '-'   : p[0] = p[1] - p[3]
    #if p[2] == '*'   : p[0] = p[1] * p[3]
    #if p[2] == '/'   : p[0] = p[1] / p[3]
    #if p[2] == '.+'   : p[0] = p[1] + p[3]

def p_assigment(p):
    """assignment : lvalue '=' expression
                  | lvalue ADDASSIGN expression
                  | lvalue SUBASSIGN expression
                  | lvalue MULASSIGN expression
                  | lvalue DIVASSIGN expression"""

def p_lvalue(p):
    """lvalue : ID 
              | ID '[' expression_list ']' """

def p_expression_list(p):
   """expression_list : expression
                      | expression_list ',' expression"""
   
def p_if_statement(p):
   """if_statement : IF '(' expression ')' instruction %prec IFX
                   | IF '(' expression ')' instruction ELSE instruction"""
   
def p_while_statement(p):
   """while_statement : WHILE '(' expression ')' instruction"""

def p_for_statement(p):
   """for_statement : FOR ID '=' expression ':' expression instruction"""

def p_break_statement(p):
   """break_statement : BREAK"""

def p_continue_statement(p):
   """continue_statement : CONTINUE"""

def p_return_statement(p):
   """return_statement : RETURN expression"""
   
def p_print_statement(p):
   """print_statement : PRINT expression_list"""

parser = yacc.yacc()
