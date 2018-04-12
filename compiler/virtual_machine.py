from memory import Memory


def executeVM(quadruples, global_variables_dict, function_dict, constant_dict):
    instructionPointer = 0
    quadruplesLen = len(quadruples)
    execution_memory = Memory(global_variables_dict, constant_dict)
    while instructionPointer < quadruplesLen:
        print(quadruples[instructionPointer])
        instructionPointer += 1
