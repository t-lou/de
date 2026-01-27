# ============================
#   AST NODES
# ============================


class Program:
    def __init__(self, functions):
        self.functions = functions


class FunctionDef:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class Block:
    def __init__(self, statements):
        self.statements = statements


class ConstDecl:
    def __init__(self, name, type_, value):
        self.name = name
        self.type = type_
        self.value = value


class Call:
    def __init__(self, func, args):
        self.func = func
        self.args = args


class StringLiteral:
    def __init__(self, value):
        self.value = value


class Variable:
    def __init__(self, name):
        self.name = name


class VarDecl:
    def __init__(self, name, type_, value):
        self.name = name
        self.type = type_
        self.value = value


class Assignment:
    def __init__(self, name, value):
        self.name = name
        self.value = value
