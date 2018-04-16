from memory import Memory


def executeVM(quadruples, global_variables_dict, function_dict, constant_dict, curr_func_temp_vars):
    instructionPointer = 0
    quadruplesLen = len(quadruples)
    execution_memory = Memory(global_variables_dict,
                              constant_dict, curr_func_temp_vars)

    # Start executing quadruples
    while instructionPointer < quadruplesLen:
        curr_quad = quadruples[instructionPointer]
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
            [value_left, _, _, _] = execution_memory.get_address_context(
                curr_left_op)
            [value_right, _, _, _] = execution_memory.get_address_context(
                curr_right_op)
            [_, _, result_context, result_calc_index] = execution_memory.get_address_context(
                curr_result)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left + value_right)
        # SUBTRACT OPERATION
        elif curr_operation == '-':
            [value_left, _, _, _] = execution_memory.get_address_context(
                curr_left_op)
            [value_right, _, _, _] = execution_memory.get_address_context(
                curr_right_op)
            [_, _, result_context, result_calc_index] = execution_memory.get_address_context(
                curr_result)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left - value_right)

        # MULTIPLICATION OPERATION
        elif curr_operation == '*':
            [value_left, _, _, _] = execution_memory.get_address_context(
                curr_left_op)
            [value_right, _, _, _] = execution_memory.get_address_context(
                curr_right_op)
            [_, _, result_context, result_calc_index] = execution_memory.get_address_context(
                curr_result)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left * value_right)

        # DIVISION OPERATION
        elif curr_operation == '/':
            [value_left, _, _, _] = execution_memory.get_address_context(
                curr_left_op)
            [value_right, _, _, _] = execution_memory.get_address_context(
                curr_right_op)
            [_, _, result_context, result_calc_index] = execution_memory.get_address_context(
                curr_result)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value_left / value_right)

            # ASSIGN OPERATION
        elif curr_operation == '=':
            [_, result_type, result_context, result_calc_index] = execution_memory.get_address_context(
                curr_left_op)
            [value, _, _, _] = execution_memory.get_address_context(
                curr_right_op)
            if result_type == 'num':
                value = int(value)
            elif result_type == 'dec':
                value = float(value)
            execution_memory.set_value_from_context_address(
                result_context, result_calc_index, value)
        instructionPointer += 1
