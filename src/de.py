#!/usr/bin/env python3
import sys

from evaluator import Evaluator
from parser import Parser
from tokenizer import Tokenizer


def main():
    if len(sys.argv) < 3:
        print("Benutzung: de.py <datei.de> laufen")
        sys.exit(1)

    filename = sys.argv[1]
    command = sys.argv[2]

    if command != "laufen":
        print(f"Unbekannter Befehl: {command}")
        sys.exit(1)

    # --- read source code ---
    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()

    # --- tokenize ---
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()

    # --- parse ---
    parser = Parser(tokens)
    program = parser.parse_program()

    # --- evaluate ---
    evaluator = Evaluator(program)
    evaluator.run()


if __name__ == "__main__":
    main()
