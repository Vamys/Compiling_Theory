#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
   # to fill ...
   ("left", '+', '-'),
   ("left", '*', '/'),
   # to fill ...
)

# def p_expression_binop(p):
# """expression  : expression ADD_OP expression
#                | expression MUL_OP expression"""
#     if p[2] == '+'   : p[0] = p[1] + p[3]
#     elif p[2] == '-' : p[0] = p[1] - p[3]               
#     elif p[2] == '*' : p[0] = p[1] * p[3]                         
#     elif p[2] == '/' : p[0] = p[1] / p[3]  
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
    """instruction : expression NEWLINE
                   | assignment NEWLINE
                   | if_statement
                   | while_statement
                   | break_statement
                   | continue_statement
                   | return_statement
                   | print_statement
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
                  | '[' expresion_list ']'
                  | ZEROS '(' expression ')'
                  | ONES '(' expression ')'
                  | EYE '(' expression ')'
                  | expression 
                  | !expression
                  | '-' expression
                  | ID '[' expression_list ']'
                  | ID
                  | INTNUM
                  | FLOATNUM
                  | STRING
                  """
    if p[2] == '+'   : p[0] = p[1] + p[3]
    if p[2] == '-'   : p[0] = p[1] - p[3]
    if p[2] == '*'   : p[0] = p[1] * p[3]
    if p[2] == '/'   : p[0] = p[1] / p[3]
    if p[2] == '.+'   : p[0] = p[1] + p[3]

    
def p_assigment(p):
    """assignment : ID '=' expression
                  | ID ADDASSIGN expression
                  | ID SUBASSIGN expression
                  | ID MULASSIGN expression
                  | ID DIVASSIGN expression
                  | ID '=' zeros_statement"""
def p_expression_list(p):
    """expression_list : expression
                       | expression_list ',' expression"""
def p_if_statement(p):
    """if_statement : IF '(' expression ')' instruction %prec IFX
                    | IF '(' expression ')' instruction ELSE instruction"""
def p_while_statement(p):
    """while_statement : WHILE '(' expression ')' instruction"""
def p_for_statement(p):
    """for_statement : FOR ID '=' expression ':' expression"""
def p_break_statement(p):
    """break_statement : BREAK"""
def p_continue_statement(p):
    """continue_statement : CONTINUE"""
def p_return_statement(p):
    """return_statement : RETURN expression"""
def p_print_statement(p):
    """print_statement : PRINT expression_list"""

parser = yacc.yacc()
