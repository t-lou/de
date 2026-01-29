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


class Type:
    def __init__(self, name):
        self.name = name


class ArrayType:
    def __init__(self, inner):
        self.inner = inner


class VectorType:
    def __init__(self, inner):
        self.inner = inner


class DictType:
    def __init__(self, key_type, value_type):
        self.key_type = key_type
        self.value_type = value_type


class IntLiteral:
    def __init__(self, value):
        self.value = value


class FloatLiteral:
    def __init__(self, value):
        self.value = value


class ArrayLiteral:
    def __init__(self, elements):
        self.elements = elements


class DictLiteral:
    def __init__(self, entries):
        self.entries = entries


class Append:
    def __init__(self, target, value):
        self.target = target
        self.value = value


class DictSet:
    def __init__(self, target, key, value):
        self.target = target
        self.key = key
        self.value = value
