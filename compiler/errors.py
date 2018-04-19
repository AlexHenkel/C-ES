class ErrorSintaxis(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "En la linea {}".format(self.line)


class TiposErroneos(Exception):
    def __init__(self, operation):
        self.operation = operation

    def __str__(self):
        return "Para la operacion {}".format(self.operation)


class FueraDeLimite(Exception):
    def __init__(self, index, size):
        self.index = index
        self.size = size

    def __str__(self):
        return "El indice {} esta fuera del limite del arreglo de tamano {}".format(self.index, self.size)


class NumParametrosIncorrectos(Exception):
    def __init__(self, function):
        self.function = function

    def __str__(self):
        return "En la funcion {}".format(self.function)


class VarError(Exception):
    def __init__(self, variable, line):
        self.variable = variable
        self.line = line

    def __str__(self):
        return "{} en la linea {}".format(self.variable, self.line)


class VariableVacia(Exception):
    def __init__(self, operation):
        self.operation = operation

    def __str__(self):
        return "En la operacion '{}' una variable esta vacia".format(self.operation)


class VariableGlobalDuplicada(VarError):
    pass


class VariableLocalDuplicada(VarError):
    pass


class VariableGlobalNoDeclarada(VarError):
    pass


class VariableLocallNoDeclarada(VarError):
    pass


class FuncionNoDeclarada(VarError):
    pass


class FuncionDuplicada(VarError):
    pass
