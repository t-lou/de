# ============================
#   PARSER (SKELETON)
# ============================


from ast_nodes import Block, Call, ConstDecl, FunctionDef, Program, StringLiteral, Variable
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

        return Program(functions)

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

        return FunctionDef(name, params=[], body=body)

    # -------------------------
    #   BLOCK
    # -------------------------
    def parse_block(self):
        statements = []

        while not self._peek_keyword("funktionsende"):
            statements.append(self.parse_statement())

        return Block(statements)

    # -------------------------
    #   STATEMENTS
    # -------------------------
    def parse_statement(self):
        tok = self._peek()

        # konstante Zeichenkette hallo_welt = "Hallo Welt!".
        if tok.type == TokenType.KEYWORD and tok.value == "konstante":
            return self.parse_const_decl()

        # hallo_welt ausgeben.
        if tok.type == TokenType.IDENTIFIER:
            return self.parse_call()

        raise Exception(f"Unerwartete Anweisung: {tok}")

    # -------------------------
    #   CONST DECL
    # -------------------------
    def parse_const_decl(self):
        self._expect(TokenType.KEYWORD, "konstante")

        type_name = self._expect(TokenType.IDENTIFIER).value
        name = self._expect(TokenType.IDENTIFIER).value

        self._expect(TokenType.EQUALS)
        value = self.parse_expression()

        self._expect(TokenType.DOT)

        return ConstDecl(name, type_name, value)

    # -------------------------
    #   CALL
    # -------------------------
    def parse_call(self):
        var_name = self._expect(TokenType.IDENTIFIER).value

        func = self._expect(TokenType.KEYWORD).value  # e.g. "ausgeben"

        self._expect(TokenType.DOT)

        return Call(func, [Variable(var_name)])

    # -------------------------
    #   EXPRESSIONS
    # -------------------------
    def parse_expression(self):
        tok = self._peek()

        if tok.type == TokenType.STRING:
            self._advance()
            return StringLiteral(tok.value)

        raise Exception(f"Unerwarteter Ausdruck: {tok}")

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
