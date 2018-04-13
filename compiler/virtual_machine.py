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
        curr_rigth_op = curr_quad[2]
        curr_result = curr_quad[3]

        # GOTO OPERATION
        if curr_operation == 'GOTO':
            # print instructionPointer
            # instructionPointer = curr_result - 1
            pass
        # SUM OPERATION
        elif curr_operation == '+':
            pass
        # ASSIGN OPERATION
        elif curr_operation == '=':
            [context_left, _, _] = execution_memory.get_address_context(
                curr_left_op)
            [_, _, value_right] = execution_memory.get_address_context(
                curr_rigth_op)
            # execution_memory.set_value_from_context_address(
            #     context_left, curr_left_op, value_right)
        instructionPointer += 1
