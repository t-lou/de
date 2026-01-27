import ast_nodes


class Evaluator:
    def __init__(self, program: ast_nodes.Program):
        self.program = program
        self.functions = {}
        self.env = {}
        self.constants = set()

        # Funktionen einsammeln
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
    #   FUNCTION
    # -------------------------
    def eval_function(self, fn: ast_nodes.FunctionDef):
        old_env = self.env
        self.env = {}

        self.eval_block(fn.body)

        self.env = old_env

    # -------------------------
    #   BLOCK
    # -------------------------
    def eval_block(self, block: ast_nodes.Block):
        for stmt in block.statements:
            self.eval_statement(stmt)

    # -------------------------
    #   STATEMENTS
    # -------------------------
    def eval_statement(self, stmt):
        if isinstance(stmt, ast_nodes.ConstDecl):
            value = self.eval_expression(stmt.value)
            self.env[stmt.name] = value
            self.constants.add(stmt.name)
            return

        if isinstance(stmt, ast_nodes.VarDecl):
            value = self.eval_expression(stmt.value)
            self.env[stmt.name] = value
            return

        if isinstance(stmt, ast_nodes.Assignment):
            self.eval_assignment(stmt)
            return

        if isinstance(stmt, ast_nodes.Call):
            self.eval_call(stmt)
            return

        raise Exception(f"Unbekannte Anweisung: {stmt}")

    # -------------------------
    #   CALL
    # -------------------------
    def eval_call(self, call: ast_nodes.Call):
        if call.func == "ausgeben":
            args = [self.eval_expression(a) for a in call.args]
            print(args[0])
            return

        raise Exception(f"Unbekannte Funktion: {call.func}")

    # -------------------------
    #   EXPRESSIONS
    # -------------------------
    def eval_expression(self, expr):
        if isinstance(expr, ast_nodes.StringLiteral):
            return expr.value

        if isinstance(expr, ast_nodes.Variable):
            if expr.name not in self.env:
                raise Exception(f"Variable nicht definiert: {expr.name}")
            return self.env[expr.name]

        raise Exception(f"Unbekannter Ausdruck: {expr}")

    # -------------------------
    #   ASSIGNMENT
    # -------------------------
    def eval_assignment(self, node: ast_nodes.Assignment):
        name = node.name
        if name in self.constants:
            raise Exception(f"Konstante '{name}' kann nicht geändert werden.")
        if name not in self.env:
            raise Exception(f"Variable '{name}' ist nicht definiert.")
        self.env[name] = self.eval_expression(node.value)
