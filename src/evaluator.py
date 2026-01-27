from ast_nodes import Block, Call, ConstDecl, FunctionDef, StringLiteral, Variable


class Evaluator:
    def __init__(self, program):
        self.program = program
        self.functions = {}
        self.env = {}

        # collect functions
        for fn in program.functions:
            self.functions[fn.name] = fn

    # -------------------------
    #   ENTRY POINT
    # -------------------------
    def run(self):
        if "Haupteingang" not in self.functions:
            raise Exception("Keine Funktion 'Haupteingang' gefunden.")

        self.eval_function(self.functions["Haupteingang"])

    # -------------------------
    #   FUNCTION CALL
    # -------------------------
    def eval_function(self, fn: FunctionDef):
        # new environment for this function
        old_env = self.env
        self.env = {}

        self.eval_block(fn.body)

        # restore outer environment
        self.env = old_env

    # -------------------------
    #   BLOCK
    # -------------------------
    def eval_block(self, block: Block):
        for stmt in block.statements:
            self.eval_statement(stmt)

    # -------------------------
    #   STATEMENTS
    # -------------------------
    def eval_statement(self, stmt):
        if isinstance(stmt, ConstDecl):
            value = self.eval_expression(stmt.value)
            self.env[stmt.name] = value
            return

        if isinstance(stmt, Call):
            self.eval_call(stmt)
            return

        raise Exception(f"Unbekannte Anweisung: {stmt}")

    # -------------------------
    #   CALL
    # -------------------------
    def eval_call(self, call: Call):
        # built-in: ausgeben
        if call.func == "ausgeben":
            args = [self.eval_expression(a) for a in call.args]
            print(args[0])
            return

        raise Exception(f"Unbekannte Funktion: {call.func}")

    # -------------------------
    #   EXPRESSIONS
    # -------------------------
    def eval_expression(self, expr):
        if isinstance(expr, StringLiteral):
            return expr.value

        if isinstance(expr, Variable):
            if expr.name not in self.env:
                raise Exception(f"Variable nicht definiert: {expr.name}")
            return self.env[expr.name]

        raise Exception(f"Unbekannter Ausdruck: {expr}")
