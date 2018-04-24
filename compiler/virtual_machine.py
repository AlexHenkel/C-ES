from random import randint
from memory import Memory
from errors import VariableVacia, TiposErroneos, FueraDeLimite
from utils import is_float, is_boolean, cast_bool, cast_bool_inverse


def binaryRegularOperation(execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation):
    [value_left, _, _, _] = execution_memory.get_address_context(curr_left_op)
    [value_right, _, _, _] = execution_memory.get_address_context(
        curr_right_op)
    [_, _, result_context,
        result_calc_index] = execution_memory.get_address_context(curr_result)
    if value_left == None or value_right == None:
        raise VariableVacia(curr_operation)
    return [value_left, value_right, result_context, result_calc_index]


def unaryRegularOperation(execution_memory, curr_right_op, curr_result, curr_operation):
    [value, _, _, _] = execution_memory.get_address_context(
        curr_right_op)
    [_, result_type, result_context, result_calc_index] = execution_memory.get_address_context(
        curr_result)
    if value == None:
        raise VariableVacia(curr_operation)
    return [value, result_type, result_context, result_calc_index]


def operationlessAction(execution_memory, curr_op, curr_operation):
    [value, value_type, _, _] = execution_memory.get_address_context(curr_op)
    if value == None:
        raise VariableVacia(curr_operation)
    return [value, value_type]


def verifyArrayBounds(execution_memory, index_address, arr_len):
    [index_value, _, _, _] = execution_memory.get_address_context(
        index_address)
    if index_value >= arr_len:
        raise FueraDeLimite(index_value, arr_len)
    return index_value


def executeVM(quadruples, global_variables_dict, function_dict, constant_dict, curr_func_temp_vars):
    instructionPointer = 0
    quadruplesLen = len(quadruples)
    execution_memory = Memory(global_variables_dict,
                              constant_dict, curr_func_temp_vars)

    # Start executing quadruples
    while instructionPointer < quadruplesLen:
        curr_quad = quadruples[instructionPointer]
        # print instructionPointer, curr_quad
        curr_operation = curr_quad[0]
        curr_left_op = curr_quad[1]
        curr_right_op = curr_quad[2]
        curr_result = curr_quad[3]

        # GOTO OPERATION
        if curr_operation == 'GOTO':
            instructionPointer = curr_result - 1

        # GOTOF OPERATION
        elif curr_operation == 'GOTOF':
            [value, _, _, _] = execution_memory.get_address_context(
                curr_right_op)
            if value == 'falso':
                instructionPointer = curr_result - 1

        # SUM OPERATION
        elif curr_operation == '+':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left + value_right)

        # SUBTRACT OPERATION
        elif curr_operation == '-':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left - value_right)

        # MULTIPLICATION OPERATION
        elif curr_operation == '*':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left * value_right)

        # DIVISION OPERATION
        elif curr_operation == '/':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left / value_right)

        # LESS THAN OPERATION
        elif curr_operation == '<':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, cast_bool(value_left < value_right))

        # LESS OR EQUAL THAN OPERATION
        elif curr_operation == '<=':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, cast_bool(value_left <= value_right))

        # GREATER THAN OPERATION
        elif curr_operation == '>':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, cast_bool(value_left > value_right))

        # GREATER OR EQUAL THAN OPERATION
        elif curr_operation == '>=':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, cast_bool(value_left >= value_right))

        # EQUAL OPERATION
        elif curr_operation == '==':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, cast_bool(value_left == value_right))

        # NOT EQUAL OPERATION
        elif curr_operation == '!=':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, cast_bool(value_left != value_right))

        # AND OPERATION
        elif curr_operation == 'y':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, cast_bool(cast_bool_inverse(value_left) and cast_bool_inverse(value_right)))

        # OR OPERATION
        elif curr_operation == 'o':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, cast_bool(cast_bool_inverse(value_left) or cast_bool_inverse(value_right)))

        # ASSIGN OPERATION
        elif curr_operation == '=':
            [value, result_type, result_context, result_calc_index] = unaryRegularOperation(
                execution_memory, curr_right_op, curr_left_op, curr_operation)
            if result_type == 'num':
                value = int(value)
            elif result_type == 'dec':
                value = float(value)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value)

        # NEGATIVE UNARY OPERATION
        elif curr_operation == '-u':
            [value, _, result_context, result_calc_index] = unaryRegularOperation(
                execution_memory, curr_right_op, curr_result, curr_operation)
            [value, _, _, _] = execution_memory.get_address_context(
                curr_right_op)
            [_, _, result_context, result_calc_index] = execution_memory.get_address_context(
                curr_result)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value * -1)

        # POSITIVE UNARY OPERATION
        elif curr_operation == '+u':
            [value, _, result_context, result_calc_index] = unaryRegularOperation(
                execution_memory, curr_right_op, curr_result, curr_operation)
            if value < 0:
                value *= -1
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value)

        # RANDOM OPERATION
        elif curr_operation == 'aleatorio':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            if (value_left > value_right):
                [value_right, value_left] = [value_left, value_right]
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, randint(value_left, value_right))

        # PRINT COMMAND
        elif curr_operation == 'imprimir':
            params = []
            for param in curr_right_op:
                # Print arrays
                if isinstance(param, list):
                    base_address = param[0]
                    arr_len = param[1]
                    array_values = []
                    i = 0
                    while i < arr_len:
                        [value, _, _, _] = execution_memory.get_address_context(
                            base_address + i)
                        if value == None:
                            array_values.append("Nulo")
                        else:
                            array_values.append(value)
                        i += 1
                    params.append(array_values)
                else:
                    [value, _] = operationlessAction(
                        execution_memory, param, curr_operation)
                    params.append(value)
            print "".join(map(str, params))

        # READ COMMAND
        elif curr_operation == 'leer':
            curr_address = curr_right_op[0]
            curr_name = curr_right_op[1]
            [_, result_type, result_context, result_calc_index] = execution_memory.get_address_context(
                curr_address)
            user_input = raw_input(
                "Inserta valor para variable {}: \n".format(curr_name))

            if result_type == 'num':
                user_input = is_float(user_input)
                if not user_input:
                    raise TiposErroneos('leer')
                user_input = int(user_input)
            elif result_type == 'dec':
                user_input = is_float(user_input)
                if not user_input:
                    raise TiposErroneos('leer')
            elif result_type == 'tex':
                user_input = str(data).rstrip()
            elif result_type == 'bin':
                user_input = is_boolean(user_input)
                if not user_input:
                    raise TiposErroneos('leer')

            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, user_input)

        # ARRAY PUSH OPERATION
        elif curr_operation == 'agregar':
            arr_base_address = curr_left_op[0]
            arr_len = curr_left_op[1]
            value_address = curr_right_op[0]
            index_address = curr_right_op[1]

            index_value = verifyArrayBounds(
                execution_memory, index_address, arr_len)
            # Get value and context to save
            [value, _, _, _] = execution_memory.get_address_context(
                value_address)
            [_, _, result_context, result_calc_index] = execution_memory.get_address_context(
                arr_base_address + index_value)

            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value)

        # ARRAY ACCESS OPERATION
        elif curr_operation == 'accesar':
            arr_base_address = curr_left_op[0]
            arr_len = curr_left_op[1]

            [_, _, result_context, result_calc_index] = execution_memory.get_address_context(
                curr_result)
            index_value = verifyArrayBounds(
                execution_memory, curr_right_op, arr_len)
            [value, _, _, _] = execution_memory.get_address_context(
                arr_base_address + index_value)

            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value)

        # ARRAY POP OPERATION
        elif curr_operation == 'sacar':
            arr_base_address = curr_left_op[0]
            arr_len = curr_left_op[1]

            # Get context for temporary var that will hold poped value
            [_, _, result_context, result_calc_index] = execution_memory.get_address_context(
                curr_result)
            index_value = verifyArrayBounds(
                execution_memory, curr_right_op, arr_len)
            # Get current value of array position, and store it's context
            [value, _, to_delete_context, to_delete_calc_index] = execution_memory.get_address_context(
                arr_base_address + index_value)

            # Clear position in array
            execution_memory.set_value_from_context_address(
                to_delete_context, to_delete_calc_index, None)
            # Set previous value in temporary variable
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value)

        # ERA OPERATION
        elif curr_operation == 'ERA':
            curr_func = function_dict[curr_left_op]
            execution_memory.initFunction(
                curr_func['local_count'], curr_func['temp_count'])

        # PARAM OPERATION
        elif curr_operation == 'PARAM':
            # Verify if param is an array, to copy all values into memory
            if isinstance(curr_left_op, list):
                for i in range(0, curr_left_op[1]):
                    [value, _, _, _] = execution_memory.get_address_context(
                        curr_left_op[0] + i)
                    [_, _, value_context, value_calc_index] = execution_memory.get_address_context(
                        curr_right_op + i)
                    execution_memory.set_value_from_context_address(
                        "temp_{}".format(value_context), value_calc_index, value)
            # Get current value of parameter and copy it to it's assigned address by function
            else:
                [value, _, _, _] = execution_memory.get_address_context(
                    curr_left_op)
                [_, _, value_context, value_calc_index] = execution_memory.get_address_context(
                    curr_right_op)
                execution_memory.set_value_from_context_address(
                    "temp_{}".format(value_context), value_calc_index, value)

        # GOSUB OPERATION
        elif curr_operation == 'GOSUB':
            curr_func_name = curr_left_op
            curr_return_address = curr_right_op
            execution_memory.save_memory()
            execution_memory.push_return_address(curr_return_address)
            execution_memory.push_instruction_pointer(instructionPointer)
            instructionPointer = function_dict[curr_func_name]['start_p'] - 1

        elif curr_operation == 'RETURN':
            execution_memory.set_base_return_address(curr_right_op)

        # ENDFUNC OPERATION
        elif curr_operation == 'ENDFUNC':
            target_return_address = execution_memory.pop_return_address()
            instructionPointer = execution_memory.pop_instruction_pointer()
            result = None
            if target_return_address != -1:
                is_array = isinstance(target_return_address, list)
                return_len = 1
                if is_array:
                    return_len = target_return_address[1]
                    target_return_address = target_return_address[0]
                result = execution_memory.get_return_values(
                    is_array, return_len)

            execution_memory.recovery_memory()
            if target_return_address != -1:
                [_, _, result_context, result_calc_index] = execution_memory.get_address_context(
                    target_return_address)
                if isinstance(result, list):
                    for i in range(0, len(result)):
                        execution_memory.set_value_from_context_address(
                            result_context, result_calc_index + i, result[i])
                else:
                    execution_memory.set_value_from_context_address(
                        result_context, result_calc_index, result)

        # Advance instructor pointer
        instructionPointer += 1
