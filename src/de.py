#!/usr/bin/env python3
import re
import sys

from evaluator import Evaluator
from parser import Parser
from tokenizer import Tokenizer


def preprocess(source: str) -> str:
    # 1. Alle Zeilen zusammenführen
    merged = source.replace("\n", " ")

    # 2. Tabs entfernen
    merged = merged.replace("\t", " ")

    # 3. Mehrere Whitespaces zu einem einzigen reduzieren
    merged = re.sub(r"\s+", " ", merged)

    # 4. Leading/trailing whitespace entfernen
    merged = merged.strip()

    return merged


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

    source = preprocess(source)

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
