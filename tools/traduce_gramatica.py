# -*- coding: utf-8 -*-
"""Pasa a ingles las etiquetas de gramatica que seguian en castellano.

Se ven en el libro ("Grammar: ...") y en la app, y el curso es todo en
ingles. Ademas The Magic Box reconoce la unidad por esta etiqueta, asi que
en castellano no encontraba la familia y la unidad se quedaba sin
explicacion ilustrada.
"""
import io, json, glob, os, re, sys

ROOT = r"C:\Projects\nis-fun"

TRADUCE = {
    "present perfect with just / already / yet (repaso)":
        "present perfect with just / already / yet (review)",
    "frases de postal + past simple": "postcard phrases + past simple",
    "colocaciones con make y do": "collocations with make and do",
    "adverbios de opinión + presente": "opinion adverbs + present simple",
    "superlativos: the best, the biggest, the most…":
        "superlatives: the best, the biggest, the most…",
    "comparativos + than (repaso profundo)": "comparatives + than (deep review)",
    "frases de teléfono + can/could": "telephone phrases + can / could",
    "pasado simple: repaso de irregulares": "past simple: irregular verbs review",
    "preposiciones + instrucciones de mapa": "prepositions + map directions",
    "primera condicional (if + presente, will)":
        "first conditional (if + present, will)",
    "oraciones relativas: who, which, where": "relative clauses: who, which, where",
    "adverbios de modo: -ly, well, fast": "adverbs of manner: -ly, well, fast",
    "preguntas personales (repaso Speaking)": "personal questions (Speaking review)",
    "repaso general de vocabulario": "general vocabulary review",
    "estrategias para el paper de Listening": "Listening paper strategies",
    "estrategias para Reading & Writing": "Reading & Writing paper strategies",
    "repaso general del curso": "whole course review",
    "on + día / preguntas con When": "on + day / questions with When",
    "adjetivos + have got (descripciones)": "adjectives + have got (describing people)",
    "pasado regular: -ed": "past simple: regular verbs with -ed",
    "pasado irregular: went, saw, had, got, came":
        "past simple: irregular verbs — went, saw, had, got, came",
    "pasado: historia con secuencia": "past simple: telling a story in order",
    "comparativos con -er + than": "comparatives with -er + than",
    "superlativos con -est / the best": "superlatives with -est / the best",
    "números 20-100 + How many": "numbers 20-100 + How many",
    "presente continuo (escena en vivo)": "present continuous (what is happening now)",
    "imperativos: Do… / Don't…": "imperatives: Do… / Don't…",
    "adjetivos + presente": "adjectives + present simple",
    "presente + descripciones": "present simple + describing",
    "instrucciones de lugar (giros y pasos)": "directions: turns and steps",
    "frases de carta + presente": "letter phrases + present simple",
    "pasado + when I was little": "past simple + when I was little",
    "repaso de vocabulario Movers": "Movers vocabulary review",
    "estrategias para el examen Movers": "Movers exam strategies",
    "There is… + colores": "There is… + colours",
    "plurales + colores": "plurals + colours",
    "adjetivos básicos": "basic adjectives",
    "imperativos de acción": "action imperatives",
    "presente continuo (mirar y decir)": "present continuous (look and say)",
    "seguridad vial + imperativos": "road safety + imperatives",
    "presente + playa": "present simple + at the beach",
    "can + animales (repaso)": "can + animals (review)",
    "números 11-20": "numbers 11-20",
    "el abecedario": "the alphabet",
    "repaso de vocabulario Starters": "Starters vocabulary review",
    "past simple en biografías":
        "past simple in biographies",
    "should / shouldn't (introducción)":
        "should / shouldn't (first look)",
    "on + día":
        "on + day",
    "There is / are + comida":
        "There is / are + food",
    "TPR: toca, mueve, levanta":
        "action words: touch, move, lift",
}

ES = re.compile(r"\b(de|los|las|el|la|una|un|con|para|acci[oó]n|colores|imperativos|"
                r"presente|pasado|futuro|comparativos|superlativos|preposiciones|repaso|"
                r"adjetivos|verbos|sustantivos|plurales?|gram[aá]tica|frases|oraciones|"
                r"n[uú]meros|abecedario|playa|animales|seguridad)\b", re.I)

if __name__ == "__main__":
    cambiadas, quedan = 0, []
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*", "unit-*.json"))):
        d = json.load(io.open(f, encoding="utf-8"))
        g = d.get("grammar") or ""
        if g in TRADUCE:
            d["grammar"] = TRADUCE[g]
            io.open(f, "w", encoding="utf-8", newline="\n").write(
                json.dumps(d, ensure_ascii=False, indent=1) + "\n")
            cambiadas += 1
        elif ES.search(g):
            quedan.append((os.path.basename(f), g))
    print("%d unidades pasadas a ingles" % cambiadas)
    if quedan:
        print("todavia en castellano: %d" % len(quedan))
        for n, g in quedan[:10]:
            print("   %-16s %s" % (n, g))
    else:
        print("no queda ninguna etiqueta de gramatica en castellano")
