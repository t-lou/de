# ============================
#   PARSER (SKELETON)
# ============================


import ast_nodes
from tokenizer import TokenType


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # -------------------------
    #   TOP LEVEL
    # -------------------------
    def parse_program(self):
        functions = []

        while not self._peek_type(TokenType.EOF):
            functions.append(self.parse_function())

        return ast_nodes.Program(functions)

    # -------------------------
    #   FUNCTION
    # -------------------------
    def parse_function(self):
        self._expect(TokenType.KEYWORD, "funktion")

        name = self._expect(TokenType.IDENTIFIER).value
        self._expect(TokenType.COLON)

        body = self.parse_block()

        self._expect(TokenType.KEYWORD, "funktionsende")
        end_name = self._expect(TokenType.IDENTIFIER).value

        if end_name != name:
            raise Exception(f"Funktionsende-Name stimmt nicht überein: {end_name} != {name}")

        return ast_nodes.FunctionDef(name, params=[], body=body)

    # -------------------------
    #   BLOCK
    # -------------------------
    def parse_block(self):
        statements = []

        while not self._peek_keyword("funktionsende"):
            statements.append(self.parse_statement())

        return ast_nodes.Block(statements)

    # -------------------------
    #   STATEMENTS
    # -------------------------
    def parse_statement(self):
        tok = self._peek()

        # konstante Zeichenkette hallo_welt = "Hallo Welt!".
        if tok.type == TokenType.KEYWORD and tok.value == "konstante":
            return self.parse_const_decl()

        if tok.type == TokenType.KEYWORD and tok.value == "variable":
            return self.parse_var_decl()

        if tok.type == TokenType.KEYWORD and tok.value == "In":
            return self.parse_container_mutation()

        # hallo_welt ausgeben.
        if tok.type == TokenType.IDENTIFIER:
            return self.parse_identifier_statement()

        raise Exception(f"Unerwartete Anweisung: {tok}")

    def parse_array_literal(self):
        self._expect(TokenType.LBRACKET)
        elements = []

        # empty array
        if self._peek().type == TokenType.RBRACKET:
            self._advance()
            return ast_nodes.ArrayLiteral(elements)

        # parse first element
        elements.append(self.parse_expression())

        # parse remaining elements
        while self._peek().type == TokenType.COMMA:
            self._advance()  # consume comma

            # allow trailing comma before }
            if self._peek().type == TokenType.RBRACE:
                break

            elements.append(self.parse_expression())

        self._expect(TokenType.RBRACKET)
        return ast_nodes.ArrayLiteral(elements)

    def parse_dict_literal(self):
        self._expect(TokenType.LBRACE)
        entries = []

        # leeres Wörterbuch
        if self._peek().type == TokenType.RBRACE:
            self._advance()
            return ast_nodes.DictLiteral(entries)

        # erstes Paar
        key = self.parse_expression()
        self._expect(TokenType.COLON)
        value = self.parse_expression()
        entries.append((key, value))

        # weitere Paare oder optionales trailing comma
        while self._peek().type == TokenType.COMMA:
            self._advance()  # Komma schlucken

            # trailing comma vor } erlauben
            if self._peek().type == TokenType.RBRACE:
                break

            key = self.parse_expression()
            self._expect(TokenType.COLON)
            value = self.parse_expression()
            entries.append((key, value))

        self._expect(TokenType.RBRACE)
        return ast_nodes.DictLiteral(entries)

    def parse_container_mutation(self):
        self._expect(TokenType.KEYWORD, "In")
        target = self._expect(TokenType.IDENTIFIER).value

        # append: In namen "Clara" hinzufügen.
        if self._peek().type == TokenType.STRING or self._peek().type in (
            TokenType.INT,
            TokenType.FLOAT,
            TokenType.LBRACKET,
            TokenType.LBRACE,
        ):
            value = self.parse_expression()
            self._expect(TokenType.KEYWORD, "hinzufügen")
            self._expect(TokenType.DOT)
            return ast_nodes.Append(target, value)

        # dict set: In karte wird 1 "drei" sein.
        self._expect(TokenType.KEYWORD, "wird")
        key = self.parse_expression()
        value = self.parse_expression()
        self._expect(TokenType.KEYWORD, "sein")
        self._expect(TokenType.DOT)
        return ast_nodes.DictSet(target, key, value)

    # -------------------------
    #   CONST DECL
    # -------------------------
    def parse_const_decl(self):
        self._expect(TokenType.KEYWORD, "konstante")

        type_name = self.parse_type()
        name = self._expect(TokenType.IDENTIFIER).value

        self._expect(TokenType.KEYWORD, "ist")
        value = self.parse_expression()

        self._expect(TokenType.DOT)

        return ast_nodes.ConstDecl(name, type_name, value)

    # -------------------------
    #   VAR DECL
    # -------------------------
    def parse_var_decl(self):
        self._expect(TokenType.KEYWORD, "variable")
        type_name = self.parse_type()
        name = self._expect(TokenType.IDENTIFIER).value
        self._expect(TokenType.KEYWORD, "ist")
        value = self.parse_expression()
        self._expect(TokenType.DOT)
        return ast_nodes.VarDecl(name, type_name, value)

    # -------------------------
    #   CALL
    # -------------------------
    def parse_call(self):
        var_name = self._expect(TokenType.IDENTIFIER).value

        func = self._expect(TokenType.KEYWORD).value  # e.g. "ausgeben"

        self._expect(TokenType.DOT)

        return ast_nodes.Call(func, [ast_nodes.Variable(var_name)])

    # -------------------------
    #   EXPRESSIONS
    # -------------------------
    def parse_expression(self):
        tok = self._peek()

        # string
        if tok.type == TokenType.STRING:
            self._advance()
            return ast_nodes.StringLiteral(tok.value)

        # int
        if tok.type == TokenType.INT:
            self._advance()
            return ast_nodes.IntLiteral(tok.value)

        # float
        if tok.type == TokenType.FLOAT:
            self._advance()
            return ast_nodes.FloatLiteral(tok.value)

        # array literal
        if tok.type == TokenType.LBRACKET:
            return self.parse_array_literal()

        # dictionary literal
        if tok.type == TokenType.LBRACE:
            return self.parse_dict_literal()

        # variable reference
        if tok.type == TokenType.IDENTIFIER:
            self._advance()
            return ast_nodes.Variable(tok.value)

        raise Exception(f"Unerwarteter Ausdruck: {tok}")

    def parse_type(self):
        tok = self._peek()

        # Types can start with IDENTIFIER (Ganzzahl32) or KEYWORD (Arrayvon)
        if tok.type not in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            raise Exception(f"Typ erwartet, bekam {tok}")

        base = tok.value
        self._advance()

        # simple type like "Ganzzahl32"
        if base not in {"Arrayvon", "Vektorvon", "Wörterbuchvon"}:
            return ast_nodes.Type(base)

        # -------------------------
        #   Arrayvon T
        # -------------------------
        if base == "Arrayvon":
            inner = self.parse_type()
            return ast_nodes.ArrayType(inner)

        # -------------------------
        #   Vektorvon T
        # -------------------------
        if base == "Vektorvon":
            inner = self.parse_type()
            return ast_nodes.VectorType(inner)

        # -------------------------
        #   Wörterbuchvon Schlüssel T zu Wert U
        # -------------------------
        if base == "Wörterbuchvon":
            self._expect(TokenType.KEYWORD, "Schlüssel")
            key_type = self.parse_type()
            self._expect(TokenType.KEYWORD, "zu")
            self._expect(TokenType.KEYWORD, "Wert")
            value_type = self.parse_type()
            return ast_nodes.DictType(key_type, value_type)

        raise Exception(f"Unbekannter Typ: {base}")

    def parse_identifier_statement(self):
        name_tok = self._expect(TokenType.IDENTIFIER)

        # assignment: <name> ist <expr>.
        if self._peek().type == TokenType.KEYWORD and self._peek().value == "ist":
            self._advance()  # consume "ist"
            value = self.parse_expression()
            self._expect(TokenType.DOT)
            return ast_nodes.Assignment(name_tok.value, value)

        # call: <name> ausgeben.
        func_tok = self._expect(TokenType.KEYWORD)
        self._expect(TokenType.DOT)
        return ast_nodes.Call(func_tok.value, [ast_nodes.Variable(name_tok.value)])

    # -------------------------
    #   HELPERS
    # -------------------------
    def _peek(self):
        return self.tokens[self.pos]

    def _peek_type(self, type_):
        return self._peek().type == type_

    def _peek_keyword(self, value):
        tok = self._peek()
        return tok.type == TokenType.KEYWORD and tok.value == value

    def _advance(self):
        self.pos += 1

    def _expect(self, type_, value=None):
        tok = self._peek()
        if tok.type != type_:
            raise Exception(f"Erwartet {type_}, bekam {tok}")
        if value is not None and tok.value != value:
            raise Exception(f"Erwartet {value}, bekam {tok.value}")
        self._advance()
        return tok
