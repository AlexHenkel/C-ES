import ply.lex as lex

reserved = {
    'a': 'TO',
    'o': 'OR',
    'si': 'IF',
    'y': 'AND',
    'de': 'FROM',
    'no': 'ELSE',
    'falso': 'FALSE',
    'lista': 'ARRAY',
    'texto': 'STRING',
    'numero': 'INT',
    'sucede': 'HAPPENS',
    'random': 'RANDOM',
    'quitar': 'POP',
    'ultimo': 'LAST',
    'binario': 'BOOLEAN',
    'decimal': 'FLOAT',
    'funcion': 'FUNCTION',
    'agregar': 'PUSH',
    'realiza': 'DO',
    'repetir': 'FOR',
    'devolver': 'RETURN',
    'mientras': 'WHILE',
    'variables': 'VAR',
    'verdadero': 'TRUE',
}

literals = [
    '[',
    ']',
    '(',
    ')',
    '{',
    '}',
    '+',
    '-',
    '/',
    '*',
    '=',
    '>',
    '<',
]

tokens_initial = [
    'NEQ',
    'EQ',
    'GTE',
    'LTE',
    'CONST_S',
    'CONST_I',
    'CONST_F',
    'ID',
]

tokens = tokens_initial + list(reserved.values())

t_NEQ = r'!='
t_EQ = r'=='
t_GTE = r'\>='
t_LTE = r'\<='


def t_CONST_S(t):
    r'\".*\"'
    return t


def t_CONST_F(t):
    r'[0-9]+\.[0-9]+'
    return t


def t_CONST_I(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9\_\$]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

# Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
