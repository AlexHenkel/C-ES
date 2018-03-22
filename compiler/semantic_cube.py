from errors import TiposErroneos

# Numeric codes for each type of the language
types = {'void': 0, 'numero': 1, 'decimal': 2, 'texto': 3, 'binario': 4, 'lista de numero': 5,
         'lista de decimal': 6, 'lista de texto': 7, 'lista de binario': 8}

# Short names used in semantic cube
short_types = ['', 'num', 'dec', 'tex', 'bin', 'num', 'dec', 'tex', 'bin']

# Group codes for operations used in semantic cube
operation_groups = {
    '': '', '+': 'SUM', '-': 'ARI', '+u': 'UAR', '-u': 'UAR', '*': 'ARI', '/': 'ARI',
    '=': 'ASS', '<': 'NCO', '>': 'NCO', '<=': 'NCO', '>=': 'NCO', '==': 'COM', '!=': 'COM',
    'y': 'LCO', 'o': 'LCO', 'leer': 'UVO', 'imprimir': 'UVO', 'sacar': 'UVO', 'agregar': 'PUS',
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
    'decASSdec': types['void'],
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

    # Unary VOid operations results -> leer, imprimir, pop
    'UVOnum': types['void'],
    'UVOdec': types['void'],
    'UVOtex': types['void'],
    'UVObin': types['void'],

    # PUSh list operations results -> push
    'numPUSnum': types['void'],
    'decPUSdec': types['void'],
    'texPUStex': types['void'],
    'binPUSbin': types['void'],

    # ACCess list operations results -> accesar
    'numACCnum': types['numero'],
    'decACCdec': types['decimal'],
    'texACCtex': types['texto'],
    'binACCbin': types['binario'],
}


def get_semantic_result(type_1, type_2, operation):
    type_1_short = short_types[type_1]
    type_2_short = short_types[type_2]
    op_group = operation_groups[operation]
    result_key = "{}{}{}".format(type_1_short, op_group, type_2_short)
    if not result_key in semantic_cube:
        raise TiposErroneos(operation)
    else:
        return semantic_cube[result_key]
