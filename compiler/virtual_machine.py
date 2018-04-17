from memory import Memory
from errors import VariableVacia, TiposErroneos
from utils import is_float, is_boolean


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


def executeVM(quadruples, global_variables_dict, function_dict, constant_dict, curr_func_temp_vars):
    instructionPointer = 0
    quadruplesLen = len(quadruples)
    execution_memory = Memory(global_variables_dict,
                              constant_dict, curr_func_temp_vars)

    # Start executing quadruples
    while instructionPointer < quadruplesLen:
        curr_quad = quadruples[instructionPointer]
        # print curr_quad
        curr_operation = curr_quad[0]
        curr_left_op = curr_quad[1]
        curr_right_op = curr_quad[2]
        curr_result = curr_quad[3]

        # GOTO OPERATION
        if curr_operation == 'GOTO':
            # print instructionPointer
            # instructionPointer = curr_result - 1
            pass

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
                result_context, result_calc_index, value_left < value_right)

        # LESS OR EQUAL THAN OPERATION
        elif curr_operation == '<=':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left <= value_right)

        # GREATER THAN OPERATION
        elif curr_operation == '>':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left > value_right)

        # GREATER OR EQUAL THAN OPERATION
        elif curr_operation == '>=':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left >= value_right)

        # EQUAL OPERATION
        elif curr_operation == '==':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left == value_right)

        # NOT EQUAL OPERATION
        elif curr_operation == '!=':
            [value_left, value_right, result_context, result_calc_index] = binaryRegularOperation(
                execution_memory, curr_left_op, curr_right_op, curr_result, curr_operation)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left != value_right)

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

        # PRINT COMMAND
        elif curr_operation == 'imprimir':
            # Print arrays
            if isinstance(curr_right_op, list):
                base_address = curr_right_op[0]
                arr_len = curr_right_op[1]
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
                print array_values
            else:
                [value, _] = operationlessAction(
                    execution_memory, curr_right_op, curr_operation)
                print value

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

        # Advance instructor pointer
        instructionPointer += 1
