import copy
from semantic_cube import short_types

memory_addresses = {
    'glob_num': 1000,
    'glob_dec': 2500,
    'glob_tex': 5000,
    'glob_bin': 7500,
    'loc_num': 10000,
    'loc_dec': 12500,
    'loc_tex': 15000,
    'loc_bin': 17500,
    'temp_num': 20000,
    'temp_dec': 22500,
    'temp_tex': 25000,
    'temp_bin': 27500,
    'const_num': 30000,
    'const_dec': 32500,
    'const_tex': 35000,
    'const_bin': 37500,
}

initial_addresses = copy.deepcopy(memory_addresses)


def get_memory_address(scope, curr_type, length=1):
    mem_key = "{}_{}".format(scope, short_types[curr_type])
    to_return_address = memory_addresses[mem_key]
    memory_addresses[mem_key] = to_return_address + length
    return to_return_address


class Memory:
    def __init__(self, global_variables_dict, constant_dict):
        self.globalIntVars = []
        self.globalFloatVars = []
        self.globalTextVars = []
        self.globalBoolVars = []

        self.constIntVars = []
        self.constFloatVars = []
        self.constTextVars = []
        self.constBoolVars = []

        for var in global_variables_dict:
            curr_var = global_variables_dict[var]
            curr_type = short_types[curr_var['type']]
            offset = 1
            if 'length' in curr_var:
                offset = curr_var['length']

            if curr_type == 'num':
                self.globalIntVars += [None] * offset
            elif curr_type == 'dec':
                self.globalFloatVars += [None] * offset
            elif curr_type == 'tex':
                self.globalTextVars += [None] * offset
            elif curr_type == 'bin':
                self.globalBoolVars += [None] * offset

        for const in constant_dict:
            curr_const = constant_dict[const]
            curr_type = short_types[curr_const['type']]
            curr_value = curr_const['value']

            if curr_type == 'num':
                self.constIntVars.append(curr_value)
            elif curr_type == 'dec':
                self.constFloatVars.append(curr_value)
            elif curr_type == 'tex':
                self.constTextVars.append(curr_value)
            elif curr_type == 'bin':
                self.constBoolVars.append(curr_value)
