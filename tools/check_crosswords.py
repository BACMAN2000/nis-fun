# -*- coding: utf-8 -*-
"""Audita los crucigramas: numeracion, cruces y solapamientos.

Reproduce la misma numeracion que el motor (orden de lectura sobre las
casillas de inicio) y comprueba tres cosas:

  * que cada numero de la rejilla corresponde al inicio de alguna palabra;
  * que las letras que comparten dos palabras coinciden (si no, el
    crucigrama no tiene solucion);
  * que no hay dos palabras distintas ocupando la misma casilla en la
    misma direccion.

    python tools/check_crosswords.py            # las 6 unidades de la demo
    python tools/check_crosswords.py todo       # las 150
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO = [("starters", [1, 2]), ("movers", [1, 2]), ("flyers", [1, 2])]


def celdas(w):
    return [(w["row"] + (i if w["dir"] == "down" else 0),
             w["col"] + (i if w["dir"] == "across" else 0))
            for i in range(len(w["word"]))]


def audita(words):
    """Devuelve (numeracion, problemas)."""
    problemas = []
    rejilla = {}
    for w in words:
        for (r, c), ch in zip(celdas(w), w["word"].upper()):
            if (r, c) in rejilla and rejilla[(r, c)] != ch:
                problemas.append("cruce imposible en (%d,%d): '%s' vs '%s'"
                                 % (r, c, rejilla[(r, c)], ch))
            rejilla[(r, c)] = ch

    inicios = sorted({(w["row"], w["col"]) for w in words})
    num = {p: i + 1 for i, p in enumerate(inicios)}

    # cada palabra tiene numero, y dos palabras que arrancan igual lo comparten
    for w in words:
        p = (w["row"], w["col"])
        if p not in num:
            problemas.append("la palabra %s no tiene numero" % w["word"])

    # un numero por casilla de inicio: si dos van en la misma direccion, choca
    porpos = {}
    for w in words:
        k = (w["row"], w["col"], w["dir"])
        if k in porpos:
            problemas.append("dos palabras en (%d,%d) %s: %s y %s"
                             % (w["row"], w["col"], w["dir"], porpos[k], w["word"]))
        porpos[k] = w["word"]
    return num, problemas


def main():
    todo = len(sys.argv) > 1 and sys.argv[1] == "todo"
    objetivo = []
    for lvl in ("starters", "movers", "flyers"):
        idx = json.load(open(os.path.join(ROOT, "content", lvl, "index.json"),
                             encoding="utf-8"))
        ns = [u["n"] for u in idx["units"]] if todo else [1, 2]
        objetivo.append((lvl, ns))

    total = 0
    for lvl, ns in objetivo:
        for n in ns:
            ud = json.load(open(os.path.join(ROOT, "content", lvl,
                                             "unit-%02d.json" % n), encoding="utf-8"))
            for a in ud.get("activities", []):
                if a.get("type") != "crossword":
                    continue
                words = a["data"]["words"]
                if "row" not in words[0]:
                    print("  %s u%02d %s: se diagrama en el navegador, no se audita aqui"
                          % (lvl, n, a.get("code")))
                    continue
                num, probs = audita(words)
                total += len(probs)
                marca = "OK" if not probs else "%d PROBLEMAS" % len(probs)
                print("  %-9s u%02d %s  %2d palabras, %2d numeros  %s"
                      % (lvl, n, a.get("code"), len(words), len(num), marca))
                for pr in probs:
                    print("        - " + pr)
    print("\n%d problemas en total" % total)


if __name__ == "__main__":
    main()
