# -*- coding: utf-8 -*-
"""Comprueba que el curso solo usa personajes de la biblia.

La biblia (characters/bible.md) es la lista cerrada de quien puede salir en
Fun for Nordic. Si un texto se inventa un companero o un tio, el alumno se
encuentra con alguien que no tiene cara, no tiene dibujo y no vuelve a
aparecer — y cuando se le pide arte a una IA, esta se lo inventa distinto
cada vez. Por eso la regla: quien no esta en la biblia, no sale.

Aqui se leen los nombres de persona que usan los textos y se contrastan con
la biblia. Se buscan donde son inequivocos:

    Freya: ...            quien habla en un dialogo
    I'm Nora / This is …  presentaciones
    Uncle Tom, Aunt Nora, Grandpa Sven

Tambien se revisa que cada personaje de la biblia tenga su carpeta de arte,
y al reves: que no haya arte de alguien que la biblia no reconoce.

    python tools/check_elenco.py
"""
import glob, io, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIBLIA = os.path.join(ROOT, "characters", "bible.md")
CHARS = os.path.join(ROOT, "assets", "characters")
CONTENT = os.path.join(ROOT, "content")

# Palabras que empiezan por mayuscula y no son nombres de persona.
NO_SON = {
    "the", "this", "that", "then", "now", "look", "read", "write", "listen",
    "match", "choose", "find", "say", "draw", "speaking", "exam", "here",
    "hello", "yes", "no", "and", "but", "she", "they", "you", "are", "can",
    "have", "his", "her", "one", "two", "three", "four", "five", "six",
    "seven", "eight", "nine", "ten", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday", "january", "february",
    "march", "april", "may", "june", "july", "august", "september",
    "october", "november", "december", "english", "nordic", "student",
    "first", "second", "third", "your", "voces", "radio", "hold", "let",
    "peru", "japan", "egypt", "brazil", "canada", "norway", "china",
    "spain", "france", "italy", "africa", "europe", "asia", "america",
    "mum", "dad", "grandpa", "grandma", "mother", "father", "sister",
    "brother", "baby", "aunt", "uncle", "cousin", "teacher", "miss", "mr",
    "mrs", "how", "what", "where", "when", "who", "why", "there", "these",
    "those", "some", "many", "much", "very", "well", "good", "great",
    # "Careful: there are three names you do not need." -- empieza instruccion
    # de las laminas, no es nadie
    "careful",
    "sorry", "please", "thanks", "thank", "welcome", "goodbye", "bye",
    "wow", "oops", "shhh", "woof", "meow", "roar", "choo",
    # etiquetas de las fichas de actividad, no personas
    "ask", "use", "bonus", "example", "goal", "mission", "next", "report",
    "survey", "today", "breakfast", "lunch", "dinner", "everyone", "tpr",
    "task", "tip", "note", "answer", "extra", "warm", "round", "part",
    # terminos de lengua: van seguidos de dos puntos igual que un hablante
    # en un dialogo, y el patron los tomaba por nombres de persona
    "adjective", "adjectives", "article", "articles", "comparative",
    "comparatives", "superlative", "superlatives", "conjunction",
    "conjunctions", "imperative", "imperatives", "question", "questions",
    "will", "would", "preposition", "prepositions", "pronoun", "pronouns",
    "adverb", "adverbs", "plural", "plurals", "grammar", "vocabulary",
    "example", "examples", "structure", "form", "forms", "tense", "tenses",
}

PATRONES = [
    re.compile(r'(?:^|[.…\\n"])\s*([A-Z][a-zA-Zá-úÁ-Ú]{2,11})\s*:'),      # dialogo
    re.compile(r"\b(?:I'm|I am|This is|My name is)\s+([A-Z][a-zA-Zá-úÁ-Ú]{2,11})\b"),
    re.compile(r"\b(?:Uncle|Aunt|Grandpa|Grandma|Cousin)\s+([A-Z][a-zA-Zá-úÁ-Ú]{2,11})\b"),
]


def pelado(t):
    """sin tildes y en minuscula: 'Tomás' y 'Tomas' son la misma persona"""
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower()


def de_la_biblia():
    """Los slugs de la tabla de personajes y los nombres de la lista blanca."""
    if not os.path.exists(BIBLIA):
        return set(), set()
    txt = io.open(BIBLIA, encoding="utf-8").read()
    slugs, nombres = set(), set()
    for fila in re.findall(r"^\|\s*([a-z][a-z0-9-]+)\s*\|\s*([^|]+)\|", txt, re.M):
        if fila[0].strip() == "slug":          # la cabecera de la tabla
            continue
        slugs.add(fila[0].strip())
        nombres.add(pelado(fila[1].strip()))
    # nombres extra reconocidos, uno por linea de la seccion de secundarios
    for n in re.findall(r"^-\s*\*\*([A-Z][^*]+)\*\*", txt, re.M):
        for parte in re.split(r"[,/(]", n):
            parte = parte.strip()
            if parte:
                nombres.add(pelado(parte))
    return slugs, nombres


def nombres_en_los_textos():
    visto = {}
    for f in sorted(glob.glob(os.path.join(CONTENT, "*", "unit-*.json"))):
        txt = io.open(f, encoding="utf-8").read()
        for pat in PATRONES:
            for n in pat.findall(txt):
                if pelado(n) in NO_SON:
                    continue
                visto.setdefault(pelado(n), (n, os.path.basename(os.path.dirname(f)),
                                             os.path.basename(f)))
    return visto


if __name__ == "__main__":
    slugs, nombres = de_la_biblia()
    if not slugs:
        raise SystemExit("no se pudo leer la biblia en " + BIBLIA)

    usados = nombres_en_los_textos()
    intrusos = {k: v for k, v in usados.items() if k not in nombres and k not in slugs}

    print("  biblia: %d personajes con ficha" % len(slugs))
    if intrusos:
        print("\n  %d nombres usados en los textos que la biblia no reconoce:" % len(intrusos))
        for k in sorted(intrusos):
            n, lvl, f = intrusos[k]
            print("   %-12s aparece en %s/%s" % (n, lvl, f))
    else:
        print("  todos los nombres de los textos estan en la biblia")

    # arte: que cada ficha tenga carpeta y que no sobre ninguna
    carpetas = set()
    for lvl in sorted(os.listdir(CHARS)):
        d = os.path.join(CHARS, lvl)
        if os.path.isdir(d):
            carpetas |= set(os.listdir(d))
    # los secundarios se dibujan con las figuras del banco (columna
    # "Figura del banco"), asi que no les toca carpeta propia
    del_banco = set(re.findall(r"^\|\s*([a-z][a-z0-9-]+)\s*\|[^|]+\|[^|]+\|\s*`",
                               io.open(BIBLIA, encoding="utf-8").read(), re.M))
    pendientes = set(re.findall(r"^\|\s*([a-z][a-z0-9-]+)\s*\|[^|]+\|\s*\d+\s*\|",
                                io.open(BIBLIA, encoding="utf-8").read(), re.M))
    sin_arte = sorted(s for s in slugs if s not in carpetas
                      and s not in del_banco and s not in pendientes)
    sin_ficha = sorted(c for c in carpetas if c not in slugs)
    if sin_arte:
        print("\n  en la biblia pero sin carpeta de arte: " + ", ".join(sin_arte))
    if sin_ficha:
        print("  con arte pero sin ficha en la biblia: " + ", ".join(sin_ficha))
    if not sin_arte and not sin_ficha:
        print("  el arte y la biblia coinciden")

    raise SystemExit(1 if (intrusos or sin_ficha) else 0)
