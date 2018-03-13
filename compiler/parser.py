import ply.yacc as yacc
from lex import tokens

# Define all rules

# Main


def p_main(p):
    'main : PROGRAM variables_opt main_func block'


def p_variables_opt(p):
    '''variables_opt : empty
                     | variables'''


def p_main_func(p):
    '''main_func : empty
                 | function main_func'''

# Block


def p_block(p):
    'block : "{" block_stm_opt "}"'


def p_block_stm_opt(p):
    '''block_stm_opt : empty
                     | statement block_stm_opt'''


# Statement
def p_statement(p):
    '''statement : assignation
                 | condition
                 | iteration
                 | function_call'''

# Variables


def p_variables(p):
    'variables : VARIABLE ":" var_body'


def p_var_body(p):
    'var_body : var_opts var_id ";" var_body_rec'


def p_var_body_rec(p):
    '''var_body_rec : empty
                    | var_body'''


def p_var_opts(p):
    '''var_opts : base_type
                | ARRAY FROM base_type FROM id_or_number'''


def p_var_id(p):
    'var_id : ID var_id_rec'


def p_var_id_rec(p):
    '''var_id_rec : empty
                  | "," var_id'''


# Assignation
def p_assignation(p):
    'assignation : ID "=" expression'


# Condition
def p_condition(p):
    'condition : cond_if cond_else_if_opt cond_else_opt'


def p_cond_if(p):
    'cond_if : IF HAPPENS "(" expression ")" DO block'


def p_cond_else_if_opt(p):
    '''cond_else_if_opt : empty
                        | cond_else_if cond_else_if_opt'''


def p_cond_else_if(p):
    'cond_else_if : OR IF HAPPENS "(" expression ")" DO block'


def p_cond_else_opt(p):
    '''cond_else_opt : empty
                     | ELSE HAPPENS block'''


# Iteration
def p_iteration(p):
    'iteration : iteration_opts ")" DO block'


def p_iteration_opts(p):
    '''iteration_opts : WHILE HAPPENS "(" expression
                       | FOR "(" id_or_number'''


# Condition
def p_function(p):
    'function : function_type FUNCTION ID "(" function_params ")" "{" variables_opt function_stm function_return "}"'


def p_function_type(p):
    '''function_type : empty
                     | type'''


def p_function_params(p):
    'function_params : type ID function_params_rec'


def p_function_params_rec(p):
    '''function_params_rec : empty
                           | function_params'''


def p_function_stm(p):
    '''function_stm : empty
                    | statement function_stm'''


def p_function_return(p):
    '''function_return : empty
                       | RETURN expression'''


# Function call
def p_function_call(p):
    '''function_call : read
                     | print
                     | local_function
                     | list_push
                     | list_pop'''


# Read
def p_read(p):
    'read : READ "(" base_type ID ")"'


# Print
def p_print(p):
    'print : PRINT "(" expr_params ")"'


# Parameters
def p_expr_params(p):
    'expr_params : expression expr_params_rec'


def p_expr_params_rec(p):
    '''expr_params_rec : empty
                       | "," expr_params'''


# Local function call
def p_local_function(p):
    'local_function : ID "(" expr_params ")"'


# List functions
def p_list_push(p):
    'list_push : PUSH TO ID "(" expression ")"'


def p_list_pop(p):
    'list_pop : POP LAST FROM ID "(" ")"'


def p_list_access(p):
    'list_access : ID "[" id_or_number "]"'


# Random number
def p_random(p):
    'random : RANDOM "(" FROM id_or_number "," TO id_or_number ")"'


# Expression
def p_expression(p):
    'expression : exp_comp expression_opt'


def p_expression_opt(p):
    '''expression_opt : empty
                       | binary_operators exp_comp'''


def p_exp_comp(p):
    'exp_comp : exp_add exp_comp_opt'


def p_exp_comp_opt(p):
    '''exp_comp_opt : empty
                    | comp_operators exp_add'''


def p_exp_add(p):
    'exp_add : exp_multiply exp_add_opt'


def p_exp_add_opt(p):
    '''exp_add_opt : empty
                   | add_operators exp_multiply'''


def p_exp_multiply(p):
    'exp_multiply : term exp_multiply_opt'


def p_exp_multiply_opt(p):
    '''exp_multiply_opt : empty
                        | multiply_operators term'''


# Term
def p_term(p):
    '''term : term_nested
            | term_body'''


def p_term_nested(p):
    'term_nested : "(" expression ")"'


def p_term_body(p):
    'term_body : term_body_opt term_body_types'


def p_term_body_opt(p):
    '''term_body_opt : empty
                     | add_operators'''


def p_term_body_types(p):
    '''term_body_types : ID
                     | CONST_I
                     | CONST_F
                     | CONST_S
                     | TRUE
                     | FALSE
                     | random
                     | list_access
                     | function_call'''

# General rules


def p_type(p):
    '''type : base_type
            | ARRAY FROM base_type'''


def p_id_or_number(p):
    '''id_or_number : ID
                    | CONST_I'''


def p_base_type(p):
    '''base_type : INT
                 | FLOAT
                 | STRING
                 | BOOLEAN'''


def p_binary_operators(p):
    '''binary_operators : AND
                        | OR'''


def p_comp_operators(p):
    '''comp_operators : "<"
                      | ">"
                      | EQ
                      | NEQ
                      | GTE
                      | LTE
                      '''


def p_multiply_operators(p):
    '''multiply_operators : "*"
                          | "/"'''


def p_add_operators(p):
    '''add_operators : "+"
                     | "-"'''

# Error rule for syntax errors


def p_error(p):
    print("Syntax error in input!")


# Empty rule

def p_empty(p):
    'empty :'


# Build the parser
parser = yacc.yacc()

# Open and read input
f = open("input.txt", "r")
s = f.read()
# Parse text if found
if s:
    result = parser.parse(s)
# Program finished
print("Program finished")
