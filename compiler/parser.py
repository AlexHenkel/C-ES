import glob
import copy
from optparse import OptionParser
import ply.yacc as yacc
from lex import tokens
from random import randint
from semantic_cube import types, short_types, get_semantic_result
from memory import get_memory_address
from errors import *
from virtual_machine import executeVM

curr_func_local_vars_original = {'num': 0, 'dec': 0, 'tex': 0, 'bin': 0}
curr_func_temp_vars_original = {'num': 0, 'dec': 0, 'tex': 0, 'bin': 0}

# Define global helpers
current_scope = 'global'
current_var_type = None
current_arr_length = None
quad_count = 0
curr_param_list = []
curr_func_name = None
curr_func_return_type = None
curr_func_local_vars = copy.deepcopy(curr_func_local_vars_original)
curr_func_temp_vars = copy.deepcopy(curr_func_temp_vars_original)
curr_function_call_param = 0

# Define dictionaries
global_variables_dict = {}
local_variables_dict = {}
function_dict = {}
constant_dict = {}


# Define operations stacks helpers
variables_stack = []
operators_stack = []
types_stack = []
jumps_stack = []
quads_list = []


##############################
# CUSTOM FUNCTIONS
##############################


def add_variable(p, id_position):
    if current_scope == 'global':
        if p[id_position] in global_variables_dict:
            raise VariableGlobalDuplicada(
                p[id_position], p.lineno(id_position))
        else:
            var_type = types[current_var_type]
            if var_type < 5:
                global_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': var_type, 'address': get_memory_address('glob', var_type)}
            else:
                global_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': var_type, 'length': current_arr_length,
                    'address': get_memory_address('glob', var_type, current_arr_length)}
    else:
        if p[id_position] in local_variables_dict:
            raise VariableLocalDuplicada(
                p[id_position], p.lineno(id_position))
            pass
        else:
            var_type = types[current_var_type]
            if var_type < 5:
                local_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': var_type, 'address': get_memory_address('loc', var_type)}
            else:
                local_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': var_type, 'length': current_arr_length,
                    'address': get_memory_address('loc', var_type, current_arr_length)}


def get_variable(p, id_position):
    if current_scope == 'global':
        if not p[id_position] in global_variables_dict:
            raise VariableGlobalNoDeclarada(
                p[id_position], p.lineno(id_position))
            pass
        else:
            return global_variables_dict[p[id_position]]
    else:
        if p[id_position] in local_variables_dict:
            return local_variables_dict[p[id_position]]
        elif p[id_position] in global_variables_dict:
            return global_variables_dict[p[id_position]]
        else:
            raise VariableLocallNoDeclarada(
                p[id_position], p.lineno(id_position))
            pass


def add_function(p, id_position):
    global curr_func_name
    global curr_func_return_type
    if p[id_position] in function_dict:
        raise FuncionDuplicada(p[id_position], p.lineno(id_position))
    else:
        name = p[id_position]
        curr_func_return_type = types['void']
        if current_var_type != None:
            curr_func_return_type = types[current_var_type]
        function_dict[name] = {'name': name, 'type': curr_func_return_type}
        curr_func_name = name


def update_last_function():
    global curr_func_name
    global curr_param_list
    global curr_func_local_vars
    global curr_func_temp_vars
    global current_var_type
    global curr_func_return_type
    name = curr_func_name
    # Update functions directory
    function_dict[name]['parameters'] = curr_param_list
    function_dict[name]['local_count'] = curr_func_local_vars
    function_dict[name]['temp_count'] = curr_func_temp_vars
    function_dict[name]['start_p'] = jumps_stack.pop()
    # Clear state
    curr_param_list = []
    curr_func_name = None
    curr_func_local_vars = copy.deepcopy(curr_func_local_vars_original)
    curr_func_temp_vars = copy.deepcopy(curr_func_temp_vars_original)
    current_var_type = None
    curr_func_return_type = None
    local_variables_dict.clear()
    save_quad('ENDFUNC', -1, -1, -1)


def get_function(p, id_position):
    if not p[id_position] in function_dict:
        raise FuncionNoDeclarada(
            p[id_position], p.lineno(id_position))
        pass
    else:
        return function_dict[p[id_position]]


def add_const(curr_type, value):
    global constant_dict
    curr_type = types[curr_type]
    curr_address = get_memory_address('const', curr_type)
    constant_dict[curr_address] = {'value': value,
                                   'type': curr_type, 'address': curr_address}
    variables_stack.append(curr_address)
    types_stack.append(curr_type)


def add_id(p, id_position):
    curr_var = get_variable(p, id_position)
    variables_stack.append(curr_var['address'])
    types_stack.append(curr_var['type'])


def verify_semantics(is_unary=False):
    global curr_func_temp_vars
    operation = operators_stack.pop()
    var_2 = variables_stack.pop()
    type_2 = types_stack.pop()
    if is_unary:
        var_1 = -1
        type_1 = types['void']
    else:
        var_1 = variables_stack.pop()
        type_1 = types_stack.pop()
    result_type = get_semantic_result(type_1, type_2, operation)
    result_address = -1
    if result_type > types['void']:
        result_address = get_memory_address('temp', result_type)
        variables_stack.append(result_address)
        types_stack.append(result_type)
        curr_func_temp_vars[short_types[result_type]] += 1
    save_quad(operation, var_1, var_2, result_address)


def save_quad(op, var_1, var_2, result):
    global quad_count
    quads_list.append([op, var_1, var_2, result])
    quad_count = quad_count + 1


def fill_quad_result(index, result):
    quads_list[index][3] = result

##############################
# GRAMMAR
##############################

# Main


def p_main(p):
    'main : PROGRAM variables_opt save_main_quad main_func fill_main_quad block'


def p_save_main_quad(p):
    'save_main_quad : empty'
    save_quad('GOTO', -1, -1, -1)
    jumps_stack.append(quad_count - 1)


def p_fill_main_quad(p):
    'fill_main_quad : empty'
    global current_scope
    main = jumps_stack.pop()
    fill_quad_result(main, quad_count)
    current_scope = 'main'


def p_variables_opt(p):
    '''variables_opt : empty
                     | variables'''
    global current_scope
    global current_var_type
    current_var_type = None
    current_scope = 'functions'


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
# TODO: Check when function call returns a value, but it won't be reassinged
# and need to be removed from variables_stack
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
                | ARRAY FROM base_type FROM CONST_I'''
    global current_var_type
    global current_arr_length
    global curr_func_local_vars
    if len(p) > 2:
        current_var_type = "{} {} {}".format(p[1], p[2], current_var_type)
        current_arr_length = p[5]
        if current_scope == 'functions':
            curr_func_local_vars[short_types[types[current_var_type]]
                                 ] += current_arr_length
    else:
        if current_scope == 'functions':
            curr_func_local_vars[short_types[types[current_var_type]]] += 1


def p_var_id(p):
    'var_id : ID var_id_rec'
    add_variable(p, 1)


def p_var_id_rec(p):
    '''var_id_rec : empty
                  | "," var_id'''


# Assignation
def p_assignation(p):
    'assignation : add_id "=" add_assignation_sign expression'
    verify_semantics()


def p_add_assignation_sign(p):
    'add_assignation_sign : empty'
    operators_stack.append('=')


# Condition
def p_condition(p):
    'condition : cond_if cond_else_if_opt cond_else_opt'
    end = jumps_stack.pop()
    fill_quad_result(end, quad_count)


def p_cond_if(p):
    'cond_if : IF HAPPENS "(" expression ")" verify_save_cond DO block'


def p_verify_save_cond(p):
    'verify_save_cond : empty'
    curr_type = types_stack.pop()
    cond_result = variables_stack.pop()
    if curr_type != types['binario']:
        raise TiposErroneos('if')
    else:
        save_quad('GOTOF', -1, cond_result, -1)
        jumps_stack.append(quad_count - 1)


def p_cond_else_if_opt(p):
    '''cond_else_if_opt : empty
                        | cond_else_if cond_else_if_opt'''


def p_cond_else_if(p):
    'cond_else_if : OR IF HAPPENS save_pointer "(" expression ")" cond_else_if_verify_bool DO block'


def p_save_pointer(p):
    'save_pointer : empty'
    jumps_stack.append(quad_count)


def p_cond_else_if_verify_bool(p):
    'cond_else_if_verify_bool : empty'
    curr_type = types_stack.pop()
    cond_result = variables_stack.pop()
    if curr_type != types['binario']:
        raise TiposErroneos('if')
    else:
        start_cond = jumps_stack.pop()
        last_if = jumps_stack.pop()
        save_quad('GOTOF', -1, cond_result, -1)
        jumps_stack.append(quad_count - 1)
        fill_quad_result(last_if, start_cond)


def p_cond_else_opt(p):
    '''cond_else_opt : empty
                     | ELSE HAPPENS cond_else_fill_goto block'''


def p_cond_else_fill_goto(p):
    'cond_else_fill_goto : empty'
    save_quad('GOTO', -1, -1, -1)
    last_false = jumps_stack.pop()
    jumps_stack.append(quad_count - 1)
    fill_quad_result(last_false, quad_count)


# Iteration
def p_iteration(p):
    'iteration : WHILE HAPPENS save_pointer "(" expression ")" verify_save_cond DO block'
    end_cond = jumps_stack.pop()
    start_cond = jumps_stack.pop()
    save_quad('GOTO', -1, -1, start_cond)
    fill_quad_result(end_cond, quad_count)


# Function
def p_function(p):
    'function : function_declaration "(" function_params ")" save_pointer "{" function_variables_opt function_stm function_return "}"'
    update_last_function()


def p_function_declaration(p):
    'function_declaration : function_type FUNCTION ID'
    add_function(p, 3)


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
        curr_param_list.append(types[current_var_type])


def p_function_params_rec(p):
    '''function_params_rec : empty
                           | "," function_params'''


def p_function_stm(p):
    '''function_stm : empty
                    | statement function_stm'''


def p_function_return(p):
    '''function_return : empty
                       | RETURN expression save_return'''


def p_save_return(p):
    'save_return : empty'
    curr_type = types_stack.pop()
    curr_var = variables_stack.pop()
    if curr_type != curr_func_return_type:
        raise TiposErroneos('Retorno de funcion')
    save_quad('RETURN', -1, curr_var, -1)


# Function call
def p_function_call(p):
    '''function_call : read
                     | print
                     | local_function
                     | list_push
                     | list_pop'''


# Read
def p_read(p):
    'read : READ add_read_op "(" add_id ")"'
    verify_semantics(True)


def p_add_read_op(p):
    'add_read_op : empty'
    operators_stack.append('leer')


# Print
def p_print(p):
    'print : PRINT add_print_op "(" expr_params ")"'
    verify_semantics(True)


def p_add_print_op(p):
    'add_print_op : empty'
    operators_stack.append('imprimir')


# Parameters
def p_expr_params(p):
    '''expr_params : empty
                   | expression check_func_param expr_params_rec'''


def p_check_func_param(p):
    'check_func_param : empty'
    if current_scope == 'local_function':
        global curr_function_call_param
        curr_func = function_dict[curr_func_name]
        curr_type = types_stack.pop()
        curr_param = variables_stack.pop()
        if len(curr_func['parameters']) == curr_function_call_param:
            raise NumParametrosIncorrectos(curr_func_name)
        if curr_type != curr_func['parameters'][curr_function_call_param]:
            raise TiposErroneos('Parametro')
        save_quad('PARAM', -1, curr_param, curr_function_call_param)
        curr_function_call_param = curr_function_call_param + 1


def p_expr_params_rec(p):
    '''expr_params_rec : empty
                       | "," expr_params'''


# Local function call
def p_local_function(p):
    'local_function : ID local_funcion_generate_eva "(" expr_params ")"'
    global curr_func_temp_vars
    global curr_function_call_param
    global current_scope
    global curr_func_name
    curr_func = function_dict[curr_func_name]
    if len(curr_func['parameters']) != curr_function_call_param:
        raise NumParametrosIncorrectos(curr_func_name)
    # Generate quad
    save_quad('GOSUB', curr_func_name, -1, -1)
    # Reset state
    curr_function_call_param = 0
    current_scope = 'main'
    curr_func_name = None
    # Verify semantics and get result
    curr_func = get_function(p, 1)
    func_type = curr_func['type']
    # TODO: Get function result from memory
    if (curr_func['type'] > types['void']):
        curr_func_temp_vars[short_types[func_type]] += 1


def p_local_funcion_generate_eva(p):
    'local_funcion_generate_eva : empty'
    global current_scope
    global curr_func_name
    current_scope = 'local_function'
    curr_func_name = p[-1]
    save_quad('EVA', p[-1], -1, -1)


# List functions
def p_list_push(p):
    'list_push : PUSH TO add_list_push_sign add_id "(" expression ")"'
    verify_semantics()


def p_add_list_push_sign(p):
    'add_list_push_sign : empty'
    operators_stack.append('agregar')


def p_list_pop(p):
    'list_pop : POP LAST add_list_pop_sign FROM add_id "(" ")"'
    verify_semantics(True)


def p_add_list_pop_sign(p):
    'add_list_pop_sign : empty'
    operators_stack.append('sacar')


def p_list_access(p):
    'list_access : ACCESS add_list_access_sign "(" add_id "," id_or_number ")"'
    verify_semantics()


def p_add_list_access_sign(p):
    'add_list_access_sign : empty'
    operators_stack.append('accesar')


# Random number
def p_random(p):
    'random : RANDOM add_random_sign "(" FROM id_or_number "," TO id_or_number ")"'
    verify_semantics()


def p_add_random_sign(p):
    'add_random_sign : empty'
    operators_stack.append('aleatorio')


# Expression
def p_expression(p):
    'expression : exp_comp expression_opt'
    if len(operators_stack) and operators_stack[-1] in ['y', 'o']:
        verify_semantics()


def p_expression_opt(p):
    '''expression_opt : empty
                      | logic_operators expression'''


def p_exp_comp(p):
    'exp_comp : exp_add exp_comp_opt'
    if len(operators_stack) and operators_stack[-1] in ['<', '>', '==', '!=', '<=', '>=']:
        verify_semantics()


def p_exp_comp_opt(p):
    '''exp_comp_opt : empty
                    | comp_operators exp_comp'''


def p_exp_add(p):
    'exp_add : exp_multiply exp_add_opt'
    if len(operators_stack) and operators_stack[-1] in ['+', '-']:
        verify_semantics()


def p_exp_add_opt(p):
    '''exp_add_opt : empty
                   | add_operators exp_add'''


def p_exp_multiply(p):
    'exp_multiply : term exp_multiply_opt'
    if len(operators_stack) and operators_stack[-1] in ['*', '/']:
        verify_semantics()


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
    '''term_body : term_body_opt
                 | term_body_types'''


def p_term_body_opt(p):
    'term_body_opt : term_body_opt_signs term_body_types'
    verify_semantics(True)


def p_term_body_opt_signs(p):
    '''term_body_opt_signs : "+"
                           | "-"'''
    operators_stack.append("{}u".format(p[1]))


def p_term_body_types(p):
    '''term_body_types : add_id
                       | term_body_types_rest'''


def p_term_body_types_rest(p):
    '''term_body_types_rest : add_int_const
                            | add_float_const
                            | add_string_const
                            | add_bool_const
                            | random
                            | list_access
                            | function_call'''


def p_add_id(p):
    'add_id : ID'
    add_id(p, 1)


def p_add_int_const(p):
    'add_int_const : CONST_I'
    add_const('numero', p[1])


def p_add_float_const(p):
    'add_float_const : CONST_F'
    add_const('decimal', p[1])


def p_add_string_const(p):
    'add_string_const : CONST_S'
    add_const('texto', p[1])


def p_add_bool_const(p):
    '''add_bool_const : TRUE
                      | FALSE'''
    add_const('binario', p[1])

# General rules


def p_type(p):
    '''type : base_type
            | ARRAY FROM base_type'''
    global current_var_type
    if len(p) > 2:
        current_var_type = "{} {} {}".format(p[1], p[2], current_var_type)


def p_id_or_number(p):
    '''id_or_number : add_id
                    | add_int_const'''


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
    raise ErrorSintaxis(p.lineno)


# Empty rule

def p_empty(p):
    'empty :'


# Build the parser
parser = yacc.yacc()

# Setup command line parser
cmd_parser = OptionParser()
cmd_parser.add_option("-t", "--tests", action="store_true",
                      dest="tests", default=False, help="execute tests")

(options, args) = cmd_parser.parse_args()

if options.tests:
    test_files = glob.glob("./tests/test*.txt")
    print('\n********** EXECUTING TESTS **********\n')
    test_files.sort()

    for file_name in test_files:
        f = open(file_name, "r")
        name = file_name[8:-4]
        description = f.readline()
        print('***** ' + name + ': ' + description[3:-1] + '  *****')

        s = f.read()

        if s:
            try:
                result = parser.parse(s)
            except Exception as error:
                print('Error: ' + str(error))

        # Program finished
        print("***** " + name + " finished *****\n")

    print('********** TESTS FINISHED **********\n')
else:
    # Open and read input
    f = open("input.txt", "r")
    s = f.read()
    f.close()

    # Parse text if found
    if s:
        print("Compiling code...")
        result = parser.parse(s)

        executeVM(quads_list, global_variables_dict,
                  function_dict, constant_dict)

    # Program finished
    print("Program finished")
