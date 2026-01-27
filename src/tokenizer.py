# ============================
#   TOKENS
# ============================


class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    STRING = "STRING"
    COLON = "COLON"
    DOT = "DOT"
    EQUALS = "EQUALS"
    EOF = "EOF"


class Token:
    def __init__(self, type_, value, position=None):
        self.type = type_
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


# ============================
#   TOKENIZER
# ============================


class Tokenizer:
    KEYWORDS = {
        "funktion",
        "funktionsende",
        "ist",
        "ausgeben",
    }

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def tokenize(self):
        tokens = []
        while not self._end():
            ch = self._peek()

            if ch.isspace():
                self._advance()
                continue

            if ch.isalpha() or ch == "_":
                tokens.append(self._read_identifier_or_keyword())
                continue

            if ch == '"':
                tokens.append(self._read_string())
                continue

            if ch == ":":
                tokens.append(Token(TokenType.COLON, ":"))
                self._advance()
                continue

            if ch == ".":
                tokens.append(Token(TokenType.DOT, "."))
                self._advance()
                continue

            if ch == "=":
                tokens.append(Token(TokenType.EQUALS, "="))
                self._advance()
                continue

            raise Exception(f"Unexpected character: {ch}")

        tokens.append(Token(TokenType.EOF, None))
        return tokens

    # --- helpers ---

    def _end(self):
        return self.pos >= len(self.text)

    def _peek(self):
        return self.text[self.pos]

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

        if word in self.KEYWORDS:
            return Token(TokenType.KEYWORD, word)

        return Token(TokenType.IDENTIFIER, word)

    def _read_string(self):
        self._advance()  # skip opening "
        start = self.pos
        while not self._end() and self._peek() != '"':
            self._advance()
        value = self.text[start : self.pos]
        self._advance()  # skip closing "
        return Token(TokenType.STRING, value)
