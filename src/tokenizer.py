from enum import Enum, auto

# ============================
#   TOKENS
# ============================


class TokenType(Enum):
    IDENTIFIER = auto()
    KEYWORD = auto()
    STRING = auto()
    INT = auto()
    FLOAT = auto()
    COLON = auto()
    DOT = auto()
    COMMA = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    EOF = auto()


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is None:
            return f"Token({self.type})"
        return f"Token({self.type}, {self.value})"


KEYWORDS = {
    "funktion",
    "funktionsende",
    "konstante",
    "variable",
    "ist",
    "ausgeben",
    "In",
    "hinzufügen",
    "wird",
    "sein",
    "Schlüssel",
    "Wert",
    "Arrayvon",
    "Vektorvon",
    "Wörterbuchvon",
    "zu",
}

# ============================
#   TOKENIZER
# ============================


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def tokenize(self):
        tokens = []

        while not self._end():
            ch = self._peek()

            # whitespace
            if ch.isspace():
                self._advance()
                continue

            # string literal
            if ch == '"':
                tokens.append(self._read_string())
                continue

            # number literal (int or float with comma)
            if ch.isdigit():
                tokens.append(self._number())
                continue

            # identifier or keyword
            if ch.isalpha() or ch == "_":
                tokens.append(self._identifier_or_keyword())
                continue

            # punctuation
            if ch == ".":
                tokens.append(Token(TokenType.DOT, "."))
                self._advance()
                continue

            if ch == ",":
                tokens.append(Token(TokenType.COMMA, ","))
                self._advance()
                continue

            if ch == ":":
                tokens.append(Token(TokenType.COLON, ":"))
                self._advance()
                continue

            if ch == "[":
                tokens.append(Token(TokenType.LBRACKET, "["))
                self._advance()
                continue

            if ch == "]":
                tokens.append(Token(TokenType.RBRACKET, "]"))
                self._advance()
                continue

            if ch == "{":
                tokens.append(Token(TokenType.LBRACE, "{"))
                self._advance()
                continue

            if ch == "}":
                tokens.append(Token(TokenType.RBRACE, "}"))
                self._advance()
                continue

            raise Exception(f"Unerwartetes Zeichen: {ch}")

        tokens.append(Token(TokenType.EOF))
        return tokens

    # --- helpers ---

    def _end(self):
        return self.pos >= len(self.text)

    def _peek(self):
        return self.text[self.pos]

    def _peek_next(self):
        if self.pos + 1 >= len(self.text):
            return "\0"
        return self.text[self.pos + 1]

    def _advance(self):
        self.pos += 1

    def _read_identifier_or_keyword(self):
        start = self.pos
        while not self._end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()
        word = self.text[start : self.pos]

        # declension-aware keyword: "konstant..."
        if word.startswith("konstant"):
            return Token(TokenType.KEYWORD, "konstante")

        if word in KEYWORDS:
            return Token(TokenType.KEYWORD, word)

        return Token(TokenType.IDENTIFIER, word)

    def _read_string(self):
        self._advance()  # skip opening "
        start = self.pos

        while not self._end() and self._peek() != '"':
            self._advance()

        if self._end():
            raise Exception("Unbeendeter String")

        value = self.text[start : self.pos]
        self._advance()  # skip closing "
        return Token(TokenType.STRING, value)

    def _number(self):
        start = self.pos

        # read integer part
        while not self._end() and self._peek().isdigit():
            self._advance()

        # float with comma
        if not self._end() and self._peek() == "," and self._peek_next().isdigit():
            self._advance()  # consume comma
            decimal_start = self.pos

            while not self._end() and self._peek().isdigit():
                self._advance()

            int_part = self.text[start : decimal_start - 1]
            frac_part = self.text[decimal_start : self.pos]
            value = float(int_part + "." + frac_part)
            return Token(TokenType.FLOAT, value)

        # integer
        value = int(self.text[start : self.pos])
        return Token(TokenType.INT, value)

    def _identifier_or_keyword(self):
        start = self.pos

        while not self._end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()

        text = self.text[start : self.pos]

        if text in KEYWORDS:
            return Token(TokenType.KEYWORD, text)

        return Token(TokenType.IDENTIFIER, text)
