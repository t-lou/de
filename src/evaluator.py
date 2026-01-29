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
            # self.eval_assignment(stmt)
            value = self.eval_expression(stmt.value)
            self.env[stmt.name] = value
            return

        if isinstance(stmt, ast_nodes.Call):
            self.eval_call(stmt)
            return

        if isinstance(stmt, ast_nodes.Append):
            container = self.env[stmt.target]
            value = self.eval_expression(stmt.value)

            if not isinstance(container, list):
                raise Exception(f"Kann nicht zu {stmt.target} hinzufügen: kein Vektor/Array")

            container.append(value)
            return

        if isinstance(stmt, ast_nodes.DictSet):
            container = self.env[stmt.target]
            key = self.eval_expression(stmt.key)
            value = self.eval_expression(stmt.value)

            if not isinstance(container, dict):
                raise Exception(f"Kann keinen Schlüssel in {stmt.target} setzen: kein Wörterbuch")

            container[key] = value
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
        # integer literal
        if isinstance(expr, ast_nodes.IntLiteral):
            return expr.value

        # float literal
        if isinstance(expr, ast_nodes.FloatLiteral):
            return expr.value

        # string literal
        if isinstance(expr, ast_nodes.StringLiteral):
            return expr.value

        # variable reference
        if isinstance(expr, ast_nodes.Variable):
            return self.env[expr.name]

        # array literal
        if isinstance(expr, ast_nodes.ArrayLiteral):
            return [self.eval_expression(e) for e in expr.elements]

        # dictionary literal
        if isinstance(expr, ast_nodes.DictLiteral):
            return {self.eval_expression(k): self.eval_expression(v) for (k, v) in expr.entries}

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
