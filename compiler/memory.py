from semantic_cube import short_types

memory_dir = {
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


def get_memory_address(scope, curr_type, length=1):
    mem_key = "{}_{}".format(scope, short_types[curr_type])
    to_return_address = memory_dir[mem_key]
    memory_dir[mem_key] = to_return_address + length
    return to_return_address
