from errors import TiposErroneos

# Numeric codes for each type of the language
types = {'void': 0, 'numero': 1, 'decimal': 2, 'texto': 3, 'binario': 4, 'lista de numero': 5,
         'lista de decimal': 6, 'lista de texto': 7, 'lista de binario': 8}

# Short names used in semantic cube
short_types = ['', 'num', 'dec', 'tex', 'bin', 'num', 'dec', 'tex', 'bin']
short_types_complete = ['', 'num', 'dec', 'tex',
                        'bin', 'list_num', 'list_dec', 'list_tex', 'list_bin']

# Group codes for operations used in semantic cube
operation_groups = {
    '': '', '+': 'SUM', '-': 'ARI', '+u': 'UAR', '-u': 'UAR', '*': 'ARI', '/': 'ARI',
    '=': 'ASS', '<': 'NCO', '>': 'NCO', '<=': 'NCO', '>=': 'NCO', '==': 'COM', '!=': 'COM',
    'y': 'LCO', 'o': 'LCO', 'leer': 'UVO', 'imprimir': 'UVA', 'sacar': 'ACC', 'agregar': 'PUS',
    'accesar': 'ACC', 'aleatorio': 'RAN'
}

# Semantic cube to validate operations
semantic_cube = {
    # RANdom operations results -> random
    'numRANnum': types['numero'],

    # Unary ARitmetic operations results -> + -
    'UARnum': types['numero'],
    'UARdec': types['decimal'],

    # SUM operations results -> +
    'numSUMnum': types['numero'],
    'numSUMdec': types['decimal'],
    'decSUMnum': types['decimal'],
    'decSUMdec': types['decimal'],
    'texSUMtex': types['texto'],

    # ARItmetic operations results -> - * /
    'numARInum': types['numero'],
    'numARIdec': types['decimal'],
    'decARInum': types['decimal'],
    'decARIdec': types['decimal'],

    # ASSignation operations results -> =
    'numASSnum': types['void'],
    'numASSdec': types['void'],
    'decASSdec': types['void'],
    'decASSnum': types['void'],
    'texASStex': types['void'],
    'binASSbin': types['void'],

    # Numeric COmparison operations results -> < > <= >=
    'numNCOnum': types['binario'],
    'numNCOdec': types['binario'],
    'decNCOnum': types['binario'],
    'decNCOdec': types['binario'],
    'texNCOtex': types['binario'],

    # COMparison operations results -> != ==
    'numCOMnum': types['binario'],
    'numCOMdec': types['binario'],
    'decCOMnum': types['binario'],
    'decCOMdec': types['binario'],
    'binCOMbin': types['binario'],
    'texCOMtex': types['binario'],

    # Logical COmparison operations results -> AND OR
    'binLCObin': types['binario'],

    # Unary VOid operations results -> leer
    'UVOnum': types['void'],
    'UVOdec': types['void'],
    'UVOtex': types['void'],
    'UVObin': types['void'],

    # Unary Void Augmented operations results -> imprimir
    'UVAnum': types['void'],
    'UVAdec': types['void'],
    'UVAtex': types['void'],
    'UVAbin': types['void'],
    'UVAlist_num': types['void'],
    'UVAlist_dec': types['void'],
    'UVAlist_tex': types['void'],
    'UVAlist_bin': types['void'],

    # PUSh list operations results -> push
    'list_numPUSnum': types['void'],
    'list_decPUSdec': types['void'],
    'list_texPUStex': types['void'],
    'list_binPUSbin': types['void'],

    # ACCess list operations results -> accesar, pop
    'list_numACCnum': types['numero'],
    'list_decACCnum': types['decimal'],
    'list_texACCnum': types['texto'],
    'list_binACCnum': types['binario'],
}


def get_semantic_result(type_1, type_2, operation):
    type_1_short = short_types_complete[type_1]
    type_2_short = short_types_complete[type_2]
    op_group = operation_groups[operation]
    result_key = "{}{}{}".format(type_1_short, op_group, type_2_short)
    if not result_key in semantic_cube:
        raise TiposErroneos(operation)
    else:
        return semantic_cube[result_key]
