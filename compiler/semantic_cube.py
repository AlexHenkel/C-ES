# Numeric codes for each type of the language
types = {'numero': 1, 'decimal': 2, 'texto': 3, 'binario': 4, 'lista de numero': 5,
         'lista de decimal': 6, 'lista de texto': 7, 'lista de binario': 8, 'void': 9}

# Short names used in semantic cube
short_types = {
    'numero': 'num', 'decimal': 'dec', 'texto': 'tex', 'binario': 'bin'
}

# Group codes for operations used in semantic cube
operation_groups = {
    '+': 'SUM', '-': 'ARI', '*': 'ARI', '/': 'ARI', '=': 'ASS', '<': 'NCO', '>': 'NCO',
    '<=': 'NCO', '>=': 'NCO', '==': 'COM', '!=': 'COM', 'AND': 'LCO', 'OR': 'LCO',
}

# Semantic cube to validate operations
semantic_cube = {
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
    'numASSnum': types['numero'],
    'decASSdec': types['decimal'],
    'texASStex': types['texto'],
    'binASSbin': types['binario'],

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
}


def get_semantic_result(type1, type2, operation):
    type1_short = short_types[type1]
    type2_short = short_types[type2]
    op_group = operation_groups[operation]
    return semantic_cube["{}{}{}".format(type1_short, type2_short, op_group)]
