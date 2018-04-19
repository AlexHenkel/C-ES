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

initial_addresses = [1000, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000,
                     22500, 25000, 27500, 30000, 32500, 35000, 37500]
ordered_contexts = ['glob_num', 'glob_dec', 'glob_tex', 'glob_bin', 'loc_num', 'loc_dec', 'loc_tex', 'loc_bin',
                    'temp_num', 'temp_dec', 'temp_tex', 'temp_bin', 'const_num', 'const_dec', 'const_tex', 'const_bin']


def get_memory_address(scope, curr_type, length=1):
    mem_key = "{}_{}".format(scope, short_types[curr_type])
    to_return_address = memory_addresses[mem_key]
    memory_addresses[mem_key] = to_return_address + length
    return to_return_address


def reset_local_addresses():
    memory_addresses['loc_num'] = 10000
    memory_addresses['loc_dec'] = 12500
    memory_addresses['loc_tex'] = 15000
    memory_addresses['loc_bin'] = 17500
    memory_addresses['temp_num'] = 20000
    memory_addresses['temp_dec'] = 22500
    memory_addresses['temp_tex'] = 25000
    memory_addresses['temp_bin'] = 27500


class Memory:
    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        return setattr(self, name, value)

    def __init__(self, global_variables_dict, constant_dict, curr_func_temp_vars):
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

        self.temp_loc_num = []
        self.temp_loc_dec = []
        self.temp_loc_tex = []
        self.temp_loc_bin = []
        self.temp_temp_num = []
        self.temp_temp_dec = []
        self.temp_temp_tex = []
        self.temp_temp_bin = []

        self.return_stack = []
        self.pointer_stack = []
        self.memory_stack = []
        self.base_return_address = None

        for var in global_variables_dict:
            curr_var = global_variables_dict[var]
            curr_type = short_types[curr_var['type']]
            offset = 1
            if 'length' in curr_var:
                offset = curr_var['length']

            self["glob_{}".format(curr_type)] += [None] * offset

        for const in constant_dict:
            curr_const = constant_dict[const]
            curr_type = short_types[curr_const['type']]
            curr_value = curr_const['value']

            self["const_{}".format(curr_type)].append(curr_value)

        for temp in curr_func_temp_vars:
            self["temp_{}".format(temp)] += [None] * curr_func_temp_vars[temp]

    def initFunction(self, local_count, temp_count):
        for curr_type in local_count:
            self["temp_loc_{}".format(
                curr_type)] += [None] * local_count[curr_type]

        for curr_type in temp_count:
            self["temp_temp_{}".format(curr_type)] += [None] * \
                temp_count[curr_type]

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
        return [curr_value, curr_context.split("_")[1], curr_context, calc_index]

    def save_memory(self):
        self.memory_stack.append([self.loc_num, self.loc_dec, self.loc_tex, self.loc_bin,
                                  self.temp_num, self.temp_dec, self.temp_tex, self.temp_bin])
        # Put temp function memory in current memory
        self.loc_num = self.temp_loc_num
        self.loc_dec = self.temp_loc_dec
        self.loc_tex = self.temp_loc_tex
        self.loc_bin = self.temp_loc_bin
        self.temp_num = self.temp_temp_num
        self.temp_dec = self.temp_temp_dec
        self.temp_tex = self.temp_temp_tex
        self.temp_bin = self.temp_temp_bin

        # Reset temp funciton memory
        self.temp_loc_num = []
        self.temp_loc_dec = []
        self.temp_loc_tex = []
        self.temp_loc_bin = []
        self.temp_temp_num = []
        self.temp_temp_dec = []
        self.temp_temp_tex = []
        self.temp_temp_bin = []

    def recovery_memory(self):
        recovered_memory = self.memory_stack.pop()

        # Put back recovered memory
        self.loc_num = recovered_memory[0]
        self.loc_dec = recovered_memory[1]
        self.loc_tex = recovered_memory[2]
        self.loc_bin = recovered_memory[3]
        self.temp_num = recovered_memory[4]
        self.temp_dec = recovered_memory[5]
        self.temp_tex = recovered_memory[6]
        self.temp_bin = recovered_memory[7]

    def set_value_from_context_address(self, context, index, value):
        self[context][index] = value

    def push_return_address(self, return_address):
        self.return_stack.append(return_address)

    def pop_return_address(self):
        return self.return_stack.pop()

    def push_instruction_pointer(self, instruction_pointer):
        self.pointer_stack.append(instruction_pointer)

    def pop_instruction_pointer(self):
        return self.pointer_stack.pop()

    def set_base_return_address(self, address):
        self.base_return_address = address

    def get_return_values(self, is_array=False, length=1):
        result = None
        if is_array:
            result = []
            for i in range(0, length):
                result.append(self.get_address_context(
                    self.base_return_address + i)[0])
        else:
            result = self.get_address_context(self.base_return_address)[0]
        self.base_return_address = None
        return result
