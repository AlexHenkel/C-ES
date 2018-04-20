import glob
import copy
from optparse import OptionParser
import ply.yacc as yacc
from random import randint
from semantic_cube import types, short_types, get_semantic_result
from lex import tokens
from memory import get_memory_address, reset_local_addresses
from errors import *
from virtual_machine import executeVM

curr_func_local_vars_original = {'num': 0, 'dec': 0, 'tex': 0, 'bin': 0}
curr_func_temp_vars_original = {'num': 0, 'dec': 0, 'tex': 0, 'bin': 0}
return_address_original = {'address': None, 'length': 1}

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
curr_function_call_name = []
curr_function_call_param = []
return_address = copy.deepcopy(return_address_original)

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
jumps_else_if = []


##############################
# CUSTOM FUNCTIONS
##############################


def add_variable(p, id_position):
    global curr_func_local_vars
    if current_scope == 'global':
        if p[id_position] in global_variables_dict:
            raise VariableGlobalDuplicada(
                p[id_position], p.lineno(id_position))
        else:
            var_type = types[current_var_type]
            if var_type < 5:
                address = get_memory_address('glob', var_type)
                global_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': var_type, 'address': address}
                return [address]
            else:
                address = get_memory_address(
                    'glob', var_type, current_arr_length)
                global_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': var_type, 'length': current_arr_length,
                    'address': address}
                return [address, current_arr_length]
    else:
        if p[id_position] in local_variables_dict:
            raise VariableLocalDuplicada(
                p[id_position], p.lineno(id_position))
        else:
            var_type = types[current_var_type]
            if var_type < 5:
                address = get_memory_address('loc', var_type)
                local_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': var_type, 'address': address}
                if current_scope == 'functions':
                    curr_func_local_vars[short_types[var_type]] += 1
                return [address]
            else:
                address = get_memory_address(
                    'loc', var_type, current_arr_length)
                local_variables_dict[p[id_position]] = {
                    'name': p[id_position], 'type': var_type, 'length': current_arr_length,
                    'address': address}
                if current_scope == 'functions':
                    curr_func_local_vars[short_types[var_type]
                                         ] += current_arr_length
                return [address, current_arr_length]


def get_variable(p, id_position):
    if current_scope == 'global':
        if not p[id_position] in global_variables_dict:
            raise VariableGlobalNoDeclarada(
                p[id_position], p.lineno(id_position))
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


def get_variable_by_address(address):
    for var in local_variables_dict:
        if local_variables_dict[var]["address"] == address:
            return local_variables_dict[var]
    for var in global_variables_dict:
        if global_variables_dict[var]["address"] == address:
            return global_variables_dict[var]
    return {'length': current_arr_length}


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


def update_last_function_first():
    # Update functions directory
    function_dict[curr_func_name]['parameters'] = curr_param_list
    function_dict[curr_func_name]['start_p'] = jumps_stack.pop()
    function_dict[curr_func_name]['return_address'] = return_address


def update_last_function_second():
    global curr_func_name
    global curr_param_list
    global curr_func_local_vars
    global curr_func_temp_vars
    global current_var_type
    global curr_func_return_type
    global return_address
    # Update functions directory
    function_dict[curr_func_name]['local_count'] = curr_func_local_vars
    function_dict[curr_func_name]['temp_count'] = curr_func_temp_vars
    # Clear state
    curr_param_list = []
    curr_func_name = None
    curr_func_local_vars = copy.deepcopy(curr_func_local_vars_original)
    curr_func_temp_vars = copy.deepcopy(curr_func_temp_vars_original)
    return_address = copy.deepcopy(return_address_original)
    reset_local_addresses()
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


def verify_semantics(is_unary=False, with_length=False, with_name=False, no_save=False):
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

    # To set array length, change variable to an array containing address and length
    if type_1 >= types['lista de numero'] and with_length:
        curr_arr = get_variable_by_address(var_1)
        var_1 = [var_1, curr_arr["length"]]

    if type_2 >= types['lista de numero'] and with_length:
        curr_arr = get_variable_by_address(var_2)
        var_2 = [var_2, curr_arr["length"]]

    # Change variable address to array with address and name if necessary
    if with_name and type_1 > types['void']:
        curr_var = get_variable_by_address(var_1)
        var_1 = [var_1, curr_var["name"]]

    if with_name and type_2 > types['void']:
        curr_var = get_variable_by_address(var_2)
        var_2 = [var_2, curr_var["name"]]

    # Set result address in case operation create new result
    if result_type > types['void']:
        result_address = get_memory_address('temp', result_type)
        variables_stack.append(result_address)
        types_stack.append(result_type)
        curr_func_temp_vars[short_types[result_type]] += 1

    if not no_save:
        save_quad(operation, var_1, var_2, result_address)

    return [operation, var_1, var_2, result_address]


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
    'main : PROGRAM variables_opt save_main_quad main_func_opt fill_main_quad block'


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


def p_main_func_opt(p):
    '''main_func_opt : empty
                 | FUNCTIONS main_func_rec'''


def p_main_func_rec(p):
    '''main_func_rec : empty
                     | function main_func_rec'''

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
                 | function_call
                 | function_return'''

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
    if len(p) > 2:
        current_var_type = "{} {} {}".format(p[1], p[2], current_var_type)
        current_arr_length = p[5]


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
    while jumps_else_if[-1] != "(":
        to_change = jumps_else_if.pop()
        fill_quad_result(to_change, quad_count)
    # Remove fake end to stack
    jumps_else_if.pop()


def p_cond_if(p):
    'cond_if : IF HAPPENS "(" expression ")" verify_save_cond DO block'
    # Append a fake end in order to allow nested operations
    jumps_else_if.append('(')


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
    'cond_else_if : OR IF HAPPENS cond_else_if_save_goto save_pointer "(" expression ")" cond_else_if_verify_bool DO block'


def p_cond_else_if_save_goto(p):
    'cond_else_if_save_goto : empty'
    save_quad('GOTO', -1, -1, -1)
    jumps_else_if.append(quad_count - 1)


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
    'function : function_declaration "(" function_params ")" save_pointer function_update_first "{" function_variables_opt function_stm "}"'
    update_last_function_second()


def p_function_update_first(p):
    'function_update_first : empty'
    update_last_function_first()


def p_function_declaration(p):
    'function_declaration : function_type FUNCTION ID'
    add_function(p, 3)


def p_function_variables_opt(p):
    '''function_variables_opt : empty
                              | variables'''


def p_function_type(p):
    '''function_type : empty
                     | function_return_type'''


def p_function_return_type(p):
    '''function_return_type : base_type
                            | ARRAY FROM base_type FROM CONST_I'''
    global return_address
    global current_var_type
    global current_arr_length
    curr_length = 1

    if len(p) > 2:
        current_var_type = "{} {} {}".format(p[1], p[2], current_var_type)
        current_arr_length = p[5]
        curr_length = current_arr_length

    return_address['length'] = curr_length


def p_function_params(p):
    '''function_params : empty
                       | function_param_type function_params_save_id function_params_rec'''


def p_function_params_save_id(p):
    'function_params_save_id : ID'
    curr_info = [types[current_var_type]] + add_variable(p, 1)
    curr_param_list.append(curr_info)


def p_function_param_type(p):
    '''function_param_type : base_type
                           | ARRAY FROM base_type FROM CONST_I'''
    global current_var_type
    global current_arr_length
    if len(p) > 2:
        current_var_type = "{} {} {}".format(p[1], p[2], current_var_type)
        current_arr_length = p[5]


def p_function_params_rec(p):
    '''function_params_rec : empty
                           | "," function_params'''


def p_function_stm(p):
    '''function_stm : empty
                    | statement function_stm'''


def p_function_return(p):
    '''function_return : RETURN expression save_return'''


def p_save_return(p):
    'save_return : empty'
    global curr_func_temp_vars
    curr_type = types_stack.pop()
    curr_var = variables_stack.pop()
    if curr_type != curr_func_return_type:
        raise TiposErroneos('Retorno de funcion')
    # Verify type of return and if is an array, it's length
    if curr_type >= types['lista de numero']:
        curr_var_len = get_variable_by_address(curr_var)['length']
        if curr_var_len != return_address['length']:
            raise TiposErroneos('Retorno de funcion (longitud)')
    save_quad('RETURN', -1, curr_var, -1)
    save_quad('ENDFUNC', -1, -1, -1)


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
    verify_semantics(True, False, True)


def p_add_read_op(p):
    'add_read_op : empty'
    operators_stack.append('leer')


# Print
def p_print(p):
    'print : PRINT "(" print_params ")"'


def p_print_params(p):
    '''print_params : empty
                    | expression save_print_param print_params_rec'''


def p_save_print_param(p):
    'save_print_param : empty'
    operators_stack.append('imprimir')
    verify_semantics(True, True)


def p_print_params_rec(p):
    '''print_params_rec : empty
                       | "," print_params'''


# Local function call
def p_local_function(p):
    'local_function : ID local_funcion_generate_eva "(" expr_params ")"'
    global curr_func_temp_vars
    global curr_function_call_param
    global current_scope
    global curr_function_call_name
    curr_func = get_function(p, 1)
    if len(curr_func['parameters']) != curr_function_call_param[-1]:
        raise NumParametrosIncorrectos(curr_function_call_name[-1])
    result_address = -1
    is_array = curr_func['type'] >= types['lista de numero']
    # Verify if function returns value
    if curr_func['type'] > types['void']:
        # Verify if it's array so we get enough memory
        curr_len = 1
        if is_array:
            curr_len = curr_func['return_address']['length']
            # Set this variable to know length of array when accesing result of this funciton
            current_arr_length = curr_len
        # Request a temporary variable to store data
        result_address = get_memory_address(
            "temp", curr_func['type'], curr_len)
        # Push variable to stack to be accessible to other functions
        variables_stack.append(result_address)
        types_stack.append(curr_func['type'])
        curr_func_temp_vars[short_types[curr_func['type']]] += curr_len
        # If return variable is an array, add it's length
        if is_array:
            result_address = [result_address, curr_len]

    # Generate quad
    save_quad('GOSUB', curr_function_call_name[-1], result_address, -1)
    # Reset state
    curr_function_call_param.pop()
    curr_function_call_name.pop()


def p_local_funcion_generate_eva(p):
    'local_funcion_generate_eva : empty'
    global current_scope
    global curr_function_call_name
    current_scope = 'local_function'
    curr_function_call_param.append(0)
    curr_function_call_name.append(p[-1])
    save_quad('ERA', p[-1], -1, -1)


# Parameters
def p_expr_params(p):
    '''expr_params : empty
                   | expression check_func_param expr_params_rec'''


def p_check_func_param(p):
    'check_func_param : empty'
    global curr_function_call_param
    curr_func = function_dict[curr_function_call_name[-1]]
    curr_type = types_stack.pop()
    curr_param = variables_stack.pop()

    # Verify if it's trying to overflow parameters list
    if len(curr_func['parameters']) == curr_function_call_param[-1]:
        raise NumParametrosIncorrectos(curr_function_call_name[-1])

    curr_param_info = curr_func['parameters'][curr_function_call_param[-1]]
    # Verify if parameter is an array or atomic type
    if len(curr_param_info) == 3:
        # Verify types and length of array
        if curr_type != curr_param_info[0] or get_variable_by_address(curr_param)['length'] != curr_param_info[2]:
            raise TiposErroneos('Parametro (arreglo)')
        curr_param = [curr_param, curr_param_info[2]]
    else:
        if curr_type != curr_param_info[0]:
            raise TiposErroneos('Parametro')

    # Save QUAD in format (op, curr_address, target_address, param_number)
    save_quad('PARAM', curr_param,
              curr_param_info[1], curr_function_call_param[-1])
    curr_function_call_param[-1] = curr_function_call_param[-1] + 1


def p_expr_params_rec(p):
    '''expr_params_rec : empty
                       | "," expr_params'''


# List functions
def p_list_push(p):
    'list_push : PUSH TO add_list_push_sign "(" add_id "," expression "," id_or_number ")"'
    # Get index data, to allow semantic verification
    index_var = variables_stack.pop()
    index_type = types_stack.pop()
    # Verify insert type match array type
    [operation, var_1, var_2, _] = verify_semantics(False, True, False, True)
    save_quad(operation, var_1, [var_2, index_var], -1)


def p_add_list_push_sign(p):
    'add_list_push_sign : empty'
    operators_stack.append('agregar')


def p_list_pop(p):
    'list_pop : POP FROM add_list_pop_sign "(" add_id "," id_or_number ")"'
    verify_semantics(False, True)


def p_add_list_pop_sign(p):
    'add_list_pop_sign : empty'
    operators_stack.append('sacar')


def p_list_access(p):
    'list_access : ACCESS add_list_access_sign "(" add_id "," id_or_number ")"'
    verify_semantics(False, True)


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
                print(error.__class__.__name__ + ': ' + str(error))

        # Program finished
        print("***** " + name + " finished *****\n")

    print('********** TESTS FINISHED **********\n')
else:
    # Open and read input
    f = open("input.txt", "r")
    s = f.read()

    # Parse text if found
    if s: 
       try:
          print("Compiling code...")
          result = parser.parse(s)
          print("Compiling success!")
          executeVM(quads_list, global_variables_dict, function_dict,
                     constant_dict, curr_func_temp_vars)
          print("Program finished")
       except Exception as error:
          print(error.__class__.__name__ + ': ' + str(error))

    # Program finished
    # print("*")


def runParserWithFile(filename):
    # Define global helpers
    global current_scope
    global current_var_type
    global current_arr_length
    global quad_count
    global curr_param_list
    global curr_func_name
    global curr_func_return_type
    global curr_func_local_vars
    global curr_funct_temp_vars
    global curr_function_call_param

    # Define dictionaries
    global global_variables_dict
    global local_variables_dict
    global function_dict
    global constant_dict

    # Define operations stacks helpers
    global variables_stack
    global operators_stack
    global types_stack
    global jumps_stack
    global quads_list

    current_scope = 'global'
    current_var_type = None
    current_arr_length = None
    quad_count = 0
    curr_param_list = []
    curr_func_name = None
    curr_func_return_type = None
    curr_func_local_vars = 0
    curr_funct_temp_vars = 0
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

    # Open and read input
    f = open(filename, "r")
    s = f.read()
    f.close()

    # Parse text if found
    if s:
        #result = parser.parse(s)
        try:
            print("Compiling code...")
            result = parser.parse(s)
        except Exception as error:
            return 'Error: ' + str(error)

        executeVM(quads_list, global_variables_dict,
                  function_dict, constant_dict, curr_func_temp_vars)

    # Program finished
    print("runParserWithFile finished")

    result = ''
    for idx, val in enumerate(quads_list):
        result += '(' + str(idx) + ', ' + str(val) + ')\n'

    return result
