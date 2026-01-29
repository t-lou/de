# **de — eine kleine, spielerische, streng getypte Sprache**

**de** ist eine minimalistische, deutsch angehauchte Programmiersprache, die spielerische Syntax mit klarer Struktur verbindet.
Sie ist streng getypt, leicht zu lesen und so klein, dass sie sich eines Tages selbst interpretieren kann.

Der aktuelle Interpreter ist in Python geschrieben und dient als **Seed‑Interpreter**.
Sobald die Sprache reif genug ist, wird sie sich selbst neu implementieren — ganz im Sinne eines echten, selbst‑hostenden Systems.

---

## 🌱 Ziele der Sprache

- **spielerische Syntax**, inspiriert vom Deutschen
- **strikte Typen**, aber ohne unnötige Bürokratie
- **einfacher Interpreter**, der sich später selbst ersetzen kann
- **lesbare Programme**, die fast wie kleine Geschichten wirken
- **selbst‑hosting** als langfristiges Ziel

---

## 🧩 Beispiel: Hallo Welt

Datei: `hallo_welt.de`

```
funktion losgehen:

    konstante Zeichenkette hallo_welt = "Hallo Welt!".

    hallo_welt ausgeben.

funktionsende losgehen
```

---

## 🚀 Ausführen eines Programms

Der Interpreter heißt `de.py`.

```
python3 ./src/de.py pfad/zur/datei.de laufen
```

Beispiel:

```
python ./src/de.py ./beispiele/hallo_welt.de laufen
```

---

## 🧱 Architektur (kurz)

Der Interpreter besteht aus drei klar getrennten Komponenten:

### **Tokenizer**
Zerlegt den Quelltext in Tokens.
Unterstützt u. a.:

- Schlüsselwörter wie `funktion`, `funktionsende`, `ausgeben`
- alle deklinierten Formen von `konstant…`
- Zeichenketten `"..."`

### **Parser**
Erzeugt einen abstrakten Syntaxbaum (AST).
Aktuell unterstützt:

- Funktionsdefinitionen
- Konstantendeklarationen
- Funktionsaufrufe
- Zeichenketten & Variablen

### **Evaluator**
Führt den AST aus.
Unterstützt:

- Ausführen der Funktion `losgehen`
- Konstanten im lokalen Funktions‑Scope
- eingebaute Funktion `ausgeben`

---

## 📦 Projektstruktur

```
de/
 ├── de.py              # Kommandozeilen-Einstiegspunkt
 ├── tokenizer.py       # Tokenizer
 ├── parser.py          # Parser
 ├── evaluator.py       # Evaluator
 ├── ast_nodes.py       # AST-Klassen
 └── beispiele/
       └── hallo_welt.de
```

---

## 🛣️ Roadmap

### Kurzfristig
- Variablen (nicht nur Konstanten)
- Rückgabewerte (`zurück`)
- arithmetische Ausdrücke
- `wenn` / `sonst`
- `solange`

### Mittelfristig
- Module
- statische Typprüfung
- einfache Standardbibliothek

### Langfristig
- **Interpreter in „de“ selbst schreiben**
- Python‑Seed entfernen
- Bytecode‑ oder native Kompilierung
