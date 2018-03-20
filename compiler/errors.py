class ErrorSintaxis(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "En la linea {}".format(self.line)


class VarError(Exception):
    """Base class for exceptions in this module."""

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
