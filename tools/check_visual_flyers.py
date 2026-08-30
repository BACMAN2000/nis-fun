# -*- coding: utf-8 -*-
"""Revisa las tareas visuales generadas antes de que las vea un alumno.

Lo que se comprueba no es el gusto sino lo que rompe una clase:

  - que el personaje este en la biblia (content/cast-flyers.json)
  - que la POSE exista en disco, no solo en el JSON: una pose inventada es
    un 404 y en la lamina queda un hueco
  - que el escenario exista (jpg o png)
  - que la respuesta este entre las opciones, y que las opciones no se repitan
  - que la respuesta se oiga: tiene que aparecer literal en el guion
  - que todas las palabras dibujadas tengan dibujo (propio o emoji)
  - que la historia tenga tres vinetas en tres sitios distintos y que el
    modelo quepa en las 20-25 palabras que pide el benchmark de 5.o
  - que cada actividad diga a que clase de G5 sirve (kpi)

    python tools/check_visual_flyers.py
"""
import glob
import io
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

import gen_visual_flyers as G   # reaprovecha limpia(), hay_dibujo() y el reparto

NIVEL = "flyers"
VISUALES = set(G.NUEVOS)
fallos = []
avisos = []


def falla(u, code, msg):
    fallos.append("u%-2d %s  %s" % (u, code, msg))


def avisa(u, code, msg):
    avisos.append("u%-2d %s  %s" % (u, code, msg))


def valor(o):
    """Lo que identifica a una opcion. Las de objeto se identifican por la
    palabra; las de relacion (hora, frecuencia, cantidad, dueno, accion) por su
    campo v, porque en ellas la respuesta no es un sustantivo."""
    return o.get("v") or o.get("word")


def se_oye(respuesta, guion):
    """La respuesta tiene que decirse en el audio. Con las de relacion no basta
    con buscar la cadena entera: 'twice a week' se dice tal cual, pero un 3 de
    cantidad se dice 'three'. Se acepta el numero escrito con letra."""
    g = (guion or "").lower()
    r = str(respuesta).lower()
    if r in g:
        return True
    letras = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five"}
    return r in letras and letras[r] in g


def revisa_imagen(u, code, o, donde):
    """Cada opcion tiene que poder dibujarse. Cada modo se comprueba a su
    manera: la de objeto necesita dibujo; la de pose, que la pose exista en
    disco; la de hora, que sea una hora de verdad."""
    k = o.get("k", "word")
    if k in ("word", "count", "owner"):
        w = o.get("word")
        if not w or not G.hay_dibujo(w):
            falla(u, code, "%s: sin dibujo para %s" % (donde, w))
    if k in ("pose", "owner"):
        # sin default: si la opcion no declara pose, el motor pinta una que el
        # personaje puede no tener y sale la imagen rota. Paso justo eso.
        if o.get("pose") is None:
            falla(u, code, "%s: opcion %s sin pose declarada" % (donde, k))
        else:
            revisa_persona(u, code, {"slug": o.get("slug"), "pose": o["pose"]})
    if k == "clock":
        if not (0 <= int(o.get("h", -1)) <= 23 and 0 <= int(o.get("m", -1)) <= 59):
            falla(u, code, "%s: hora imposible %s:%s" % (donde, o.get("h"), o.get("m")))
    if k == "freq":
        if not (0 <= int(o.get("dias", -1)) <= 7):
            falla(u, code, "%s: %s dias en una semana" % (donde, o.get("dias")))
    if k == "count":
        if not (1 <= int(o.get("n", 0)) <= 8):
            falla(u, code, "%s: cantidad %s fuera de rango" % (donde, o.get("n")))


def hay_pose(slug, pose):
    return os.path.exists(os.path.join(
        RAIZ, "assets", "characters", NIVEL, slug, "pose-%02d.png" % int(pose)))


def hay_escena(s):
    base = os.path.join(RAIZ, "assets", "scenes", s)
    return os.path.exists(base + ".jpg") or os.path.exists(base + ".png")


def revisa_persona(u, code, p):
    slug = p.get("slug")
    if slug not in G.PERS:
        falla(u, code, "personaje fuera de la biblia: %s" % slug)
        return
    if p.get("figura"):
        # adulto dibujado con una figura del banco: no tiene pose que comprobar,
        # pero el archivo si tiene que estar
        f = os.path.join(RAIZ, "assets", "vocab", p["figura"] + ".png")
        if not os.path.exists(f):
            falla(u, code, "falta la figura del banco %s.png" % p["figura"])
        if G.PERS[slug].get("figura") != p["figura"]:
            falla(u, code, "%s usa una figura que el reparto no le asigna" % slug)
        return
    pose = p.get("pose", 1)
    if pose not in G.PERS[slug]["poses"]:
        falla(u, code, "%s no tiene la pose %s segun el reparto" % (slug, pose))
    if not hay_pose(slug, pose):
        falla(u, code, "falta el archivo %s/pose-%02d.png" % (slug, int(pose)))


def main():
    n = {t: 0 for t in VISUALES}
    for ruta in sorted(glob.glob(os.path.join(RAIZ, "content", NIVEL, "unit-*.json"))):
        d = json.load(io.open(ruta, encoding="utf-8"))
        u = d["number"]
        for a in d.get("activities", []):
            t = a.get("type")
            if t not in VISUALES:
                continue
            n[t] += 1
            code = a.get("code", "?")
            dd = a.get("data", {})
            guion = (dd.get("script") or "").lower()

            if not a.get("kpi", {}).get("clase"):
                falla(u, code, "%s sin kpi: no se sabe a que clase sirve" % t)

            if t == "label_people":
                if not hay_escena(dd.get("scene", "")):
                    falla(u, code, "falta la escena %s" % dd.get("scene"))
                nombres = [p["name"] for p in dd["people"]]
                if len(set(nombres)) != len(nombres):
                    falla(u, code, "dos personas con el mismo nombre: %s" % nombres)
                for p in dd["people"]:
                    revisa_persona(u, code, p)
                    if p["name"] not in dd["names"]:
                        falla(u, code, "%s no esta en el banco de nombres" % p["name"])
                    if p["name"].lower() not in guion:
                        falla(u, code, "%s no se oye en el guion" % p["name"])
                    if p["clue"].lower() not in guion:
                        falla(u, code, "la pista de %s no se oye en el guion" % p["name"])
                if len(dd["names"]) <= len(nombres):
                    avisa(u, code, "el banco no tiene nombres de sobra")

            elif t == "picture_mc":
                for i, q in enumerate(dd["questions"]):
                    ops = [valor(o) for o in q["options"]]
                    if q["answer"] not in ops:
                        falla(u, code, "P%d: la respuesta no esta entre las opciones" % (i + 1))
                    if len(set(ops)) != len(ops):
                        falla(u, code, "P%d: opciones repetidas %s" % (i + 1, ops))
                    if len(ops) != 3:
                        falla(u, code, "P%d: %d opciones en vez de 3" % (i + 1, len(ops)))
                    for o in q["options"]:
                        revisa_imagen(u, code, o, "P%d" % (i + 1))
                    if not se_oye(q["answer"], q.get("script")):
                        falla(u, code, "P%d: la respuesta no se dice en el audio" % (i + 1))

            elif t == "match_pictures":
                letras = [p["id"] for p in dd["pictures"]]
                if len(set(letras)) != len(letras):
                    falla(u, code, "letras repetidas en la galeria")
                for p in dd["pictures"]:
                    revisa_imagen(u, code, p, "galeria")
                usadas = []
                for p in dd["people"]:
                    revisa_persona(u, code, p)
                    l = dd["answers"].get(p["name"])
                    if not l:
                        falla(u, code, "%s no tiene respuesta" % p["name"])
                    elif l not in letras:
                        falla(u, code, "%s apunta a la letra %s, que no existe" % (p["name"], l))
                    else:
                        usadas.append(l)
                    if p["name"].lower() not in guion:
                        falla(u, code, "%s no se oye en el guion" % p["name"])
                if len(set(usadas)) != len(usadas):
                    falla(u, code, "dos personas con la misma foto: %s" % usadas)
                if len(dd["pictures"]) <= len(dd["people"]):
                    avisa(u, code, "no sobra ninguna foto")

            elif t == "picture_story":
                marcos = dd["frames"]
                if len(marcos) != 3:
                    falla(u, code, "%d vinetas en vez de 3" % len(marcos))
                sitios = [f["scene"] for f in marcos]
                if len(set(sitios)) != len(sitios):
                    avisa(u, code, "vinetas en el mismo sitio: %s" % sitios)
                for f in marcos:
                    if not hay_escena(f["scene"]):
                        falla(u, code, "falta la escena %s" % f["scene"])
                    for p in f.get("people", []):
                        revisa_persona(u, code, p)
                    if not f.get("hint"):
                        falla(u, code, "vineta %s sin pista" % f.get("n"))
                pal = len((dd.get("model") or "").split())
                if not (dd["min_words"] <= pal <= dd["max_words"]):
                    avisa(u, code, "el modelo tiene %d palabras y se piden %d-%d"
                          % (pal, dd["min_words"], dd["max_words"]))

    print("Revisadas: " + ", ".join("%s %d" % (t, n[t]) for t in sorted(n)))
    print()
    if fallos:
        print("FALLOS (%d):" % len(fallos))
        for f in fallos:
            print("  " + f)
    else:
        print("Sin fallos.")
    if avisos:
        print("\nAvisos (%d) — no rompen nada, pero conviene mirarlos:" % len(avisos))
        for a in avisos[:40]:
            print("  " + a)
        if len(avisos) > 40:
            print("  ... y %d mas" % (len(avisos) - 40))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
