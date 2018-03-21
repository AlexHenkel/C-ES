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


class VarError(Exception):
    def __init__(self, variable, line):
        self.variable = variable
        self.line = line

    def __str__(self):
        return "{} en la linea {}".format(self.variable, self.line)


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
