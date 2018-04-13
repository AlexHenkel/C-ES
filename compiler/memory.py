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

initial_addresses = [1000, 2500, 5000, 7500, 10000, 12500, 15000,
                     17500, 20000, 22500, 25000, 27500, 30000, 32500, 35000, 37500]
ordered_contexts = ['glob_num', 'glob_dec', 'glob_tex', 'glob_bin', 'loc_num', 'loc_dec', 'loc_tex', 'loc_bin',
                    'temp_num', 'temp_dec', 'temp_tex', 'temp_bin', 'const_num', 'const_dec', 'const_tex', 'const_bin']


def get_memory_address(scope, curr_type, length=1):
    mem_key = "{}_{}".format(scope, short_types[curr_type])
    to_return_address = memory_addresses[mem_key]
    memory_addresses[mem_key] = to_return_address + length
    return to_return_address


class Memory:
    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        return setattr(self, name, value)

    def __init__(self, global_variables_dict, constant_dict):
        self.glob_num = []
        self.glob_dec = []
        self.glob_tex = []
        self.glob_bin = []
        self.loc_num = []
        self.loc_dec = []
        self.loc_tex = []
        self.loc_bin = []
        self.temp_num = []
        self.temp_dec = []
        self.temp_tex = []
        self.temp_bin = []
        self.const_num = []
        self.const_dec = []
        self.const_tex = []
        self.const_bin = []

        for var in global_variables_dict:
            curr_var = global_variables_dict[var]
            curr_type = short_types[curr_var['type']]
            offset = 1
            if 'length' in curr_var:
                offset = curr_var['length']

            if curr_type == 'num':
                self.glob_num += [None] * offset
            elif curr_type == 'dec':
                self.glob_dec += [None] * offset
            elif curr_type == 'tex':
                self.glob_tex += [None] * offset
            elif curr_type == 'bin':
                self.glob_bin += [None] * offset

        for const in constant_dict:
            curr_const = constant_dict[const]
            curr_type = short_types[curr_const['type']]
            curr_value = curr_const['value']

            if curr_type == 'num':
                self.const_num.append(curr_value)
            elif curr_type == 'dec':
                self.const_dec.append(curr_value)
            elif curr_type == 'tex':
                self.const_tex.append(curr_value)
            elif curr_type == 'bin':
                self.const_bin.append(curr_value)

    def get_value_from_add(self, address):
        pass

    def get_address_context(self, address):
        curr_context = None
        curr_context_index = 0
        curr_value = None
        for index, limit in enumerate(initial_addresses):
            if address >= limit:
                curr_context = ordered_contexts[index]
                curr_context_index = index
            else:
                break
        calc_index = address - initial_addresses[curr_context_index]
        if len(self[curr_context]) > calc_index:
            curr_value = self[curr_context][calc_index]
        return [curr_context, curr_context.split("_")[1], curr_value]

    def set_value_from_context_address(self, context, address, value):
        self[context][address][value]
