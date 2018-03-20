import ply.yacc as yacc
from lex import tokens
from semantic_cube import types, get_semantic_result

# Define global helpers
current_scope = 'global'
current_var_type = None
current_id_or_number = None
global_variables_dict = {}
local_variables_dict = {}
function_dict = {}

# Define operations helpers
variables_stack = []
operators_stack = []
types_stack = []

##############################
# CUSTOM FUNCTIONS
##############################


def print_error(message, line):
    print("ERROR! {} en la linea {}".format(message, line))


def add_variable(p, id_position):
    if current_scope == 'global':
        if p[id_position] in global_variables_dict:
            print_error("{}: Variable global anteriormente declarada".format(
                p[id_position]), p.lineno(id_position))
        else:
            varType = types[current_var_type]
            if varType < 5:
                global_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': varType}
            else:
                global_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': varType, 'length': current_id_or_number}
    else:
        if p[id_position] in local_variables_dict:
            print_error("{}: Variable global anteriormente declarada".format(
                p[id_position]), p.lineno(id_position))
        else:
            varType = types[current_var_type]
            if varType < 5:
                local_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': varType}
            else:
                local_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': varType, 'length': current_id_or_number}

##############################
# GRAMMAR
##############################

# Main


def p_main(p):
    'main : PROGRAM variables_opt main_func block'


def p_variables_opt(p):
    '''variables_opt : empty
                     | variables'''
    global current_scope
    global current_var_type
    current_var_type = None
    current_scope = 'local'


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
    global current_var_type
    if len(p) > 2:
        current_var_type = "{} {} {}".format(p[1], p[2], current_var_type)


def p_var_id(p):
    'var_id : ID var_id_rec'
    add_variable(p, 1)


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


# Function
def p_function(p):
    'function : function_declaration "(" function_params ")" "{" function_variables_opt function_stm function_return "}"'
    global current_var_type
    current_var_type = None
    local_variables_dict.clear()


def p_function_declaration(p):
    'function_declaration : function_type FUNCTION ID'
    if p[3] in function_dict:
        print_error("{}: Funcion anteriormente declarada".format(
            p[3]), p.lineno(3))
    else:
        if current_var_type == None:
            function_dict[p[3]] = {'name': p[3], 'return': 9}
        else:
            varType = types[current_var_type]
            function_dict[p[3]] = {
                'name': p[3], 'return': varType}


def p_function_variables_opt(p):
    '''function_variables_opt : empty
                              | variables'''


def p_function_type(p):
    '''function_type : empty
                     | type'''


def p_function_params(p):
    '''function_params : empty
                       | type ID function_params_rec'''
    if len(p) > 2:
        add_variable(p, 2)


def p_function_params_rec(p):
    '''function_params_rec : empty
                           | "," function_params'''


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
    '''expr_params : empty
                   | expression expr_params_rec'''


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
    'random : RANDOM "(" FROM CONST_I "," TO CONST_I ")"'


# Expression
def p_expression(p):
    'expression : exp_comp expression_opt'


def p_expression_opt(p):
    '''expression_opt : empty
                      | logic_operators expression'''


def p_exp_comp(p):
    'exp_comp : exp_add exp_comp_opt'


def p_exp_comp_opt(p):
    '''exp_comp_opt : empty
                    | comp_operators exp_comp'''


def p_exp_add(p):
    'exp_add : exp_multiply exp_add_opt'


def p_exp_add_opt(p):
    '''exp_add_opt : empty
                   | add_operators exp_add'''


def p_exp_multiply(p):
    'exp_multiply : term exp_multiply_opt'


def p_exp_multiply_opt(p):
    '''exp_multiply_opt : empty
                        | multiply_operators exp_multiply'''


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
                     | "+"
                     | "-"'''
    if p[1] != None:
        operators_stack.append("{}u".format(p[1]))


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
    if p[1] != None:
        variables_stack.append(p[1])

# General rules


def p_type(p):
    '''type : base_type
            | ARRAY FROM base_type'''
    global current_var_type
    if len(p) > 2:
        current_var_type = "{} {} {}".format(p[1], p[2], current_var_type)


def p_id_or_number(p):
    '''id_or_number : ID
                    | CONST_I'''
    global current_id_or_number
    current_id_or_number = p[1]


def p_base_type(p):
    '''base_type : INT
                 | FLOAT
                 | STRING
                 | BOOLEAN'''
    global current_var_type
    current_var_type = p[1]


def p_logic_operators(p):
    '''logic_operators : AND
                        | OR'''
    operators_stack.append(p[1])


def p_comp_operators(p):
    '''comp_operators : "<"
                      | ">"
                      | EQ
                      | NEQ
                      | GTE
                      | LTE
                      '''
    operators_stack.append(p[1])


def p_multiply_operators(p):
    '''multiply_operators : "*"
                          | "/"'''
    operators_stack.append(p[1])


def p_add_operators(p):
    '''add_operators : "+"
                     | "-"'''
    operators_stack.append(p[1])

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
