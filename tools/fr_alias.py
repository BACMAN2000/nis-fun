# -*- coding: utf-8 -*-
"""Rehace el mapa fr->en de vocab-art.js con las 150 unidades.

El mapa estaba escrito a mano y tenia 38 entradas: con eso, de las 149
palabras del curso que tienen foto de verdad solo 31 llegaban a la version
francesa. Las otras 118 salian como dibujo plano o como emoji, y en la
clase de al lado el mismo alumno veia la foto.

No hace falta escribirlo a mano: fr_aplica.py traduce la wordlist EN SU
SITIO, asi que la palabra i del frances es la palabra i del ingles. El mapa
se saca comparando las 150 unidades por parejas.

    python tools/fr_alias.py            lo escribe
    python tools/fr_alias.py --contar   solo dice cuanto cubre
"""
import glob, io, json, os, re, sys, unicodedata
from collections import Counter, defaultdict

ROOT = r"C:\Projects\nis-portal\nis-fun"
JS = os.path.join(ROOT, "engine", "vocab-art.js")

# Las que estaban a mano y no salen de ninguna unidad (colores sueltos,
# numeros, saludos): se conservan.
A_MANO = {
    "bonjour": "hello", "salut": "hello", "au revoir": "goodbye",
    "les nombres": "numbers", "un": "one", "deux": "two", "trois": "three",
    "quatre": "four", "cinq": "five", "six": "six", "sept": "seven",
    "huit": "eight", "neuf": "nine", "dix": "ten",
    "cerf volant": "kite", "poupee": "doll", "ours en peluche": "teddy",
    "bleue": "blue", "verte": "green", "noire": "black",
}


def slug(k):
    k = "".join(c for c in unicodedata.normalize("NFD", str(k).lower())
                if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", k.replace("'", "")).strip("-")


def palabras(d):
    return (d.get("wordlist") or []) + (d.get("wordlist_extra") or [])


def construye():
    votos = defaultdict(Counter)
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*", "unit-*.json"))):
        g = f.replace(os.sep + "content" + os.sep, os.sep + "content-fr" + os.sep)
        if not os.path.exists(g):
            continue
        en = palabras(json.load(io.open(f, encoding="utf-8")))
        fr = palabras(json.load(io.open(g, encoding="utf-8")))
        if len(en) != len(fr):
            continue                     # sin pareja segura no se inventa
        for a, b in zip(en, fr):
            a, b = str(a).strip(), str(b).strip()
            if a and b and a.lower() != b.lower():
                votos[b.lower()][a.lower()] += 1

    # Si una palabra francesa traduce a dos inglesas distintas (hat / cap),
    # gana la que mas veces; da igual cual, las dos son dibujos validos.
    mapa = {fr: c.most_common(1)[0][0] for fr, c in votos.items()}
    mapa.update(A_MANO)

    # Solo interesa lo que lleva a algun dibujo: el mapa entero serian 1.800
    # entradas para 150 fotos, y el archivo lo lee el navegador.
    js = io.open(JS, encoding="utf-8", newline="").read()
    # Los SVG se escriben como A.ball = svg(...) o A['ice cream'] = svg(...)
    claves = set(re.findall(r"A\.([A-Za-z0-9_]+)\s*=", js))
    claves |= set(re.findall(r"A\[\s*'([^']+)'\s*\]\s*=", js))
    fotos = {os.path.splitext(x)[0]
             for x in os.listdir(os.path.join(ROOT, "assets", "vocab"))
             if x.endswith(".png")}
    util = {fr: en for fr, en in sorted(mapa.items())
            if slug(en) in fotos or en in claves or slug(en) in claves}
    return mapa, util


def escribe(util):
    js = io.open(JS, encoding="utf-8", newline="").read()
    crlf = "\r\n" in js
    t = js.replace("\r\n", "\n")
    # Desde el comentario, no desde el const: si no, cada pasada deja otra
    # copia del comentario encima de la anterior.
    i = t.index("  const ALIAS = {")
    marca = t.rfind("  /* fr -> en.", 0, i)
    if marca >= 0:
        i = marca
    j = t.index("};", i) + 2

    # El apostrofe va escapado en los dos lados: hay palabras inglesas con
    # apostrofe (chemist's) y sin escapar tumban el archivo entero.
    esc = lambda x: x.replace("\\", "").replace("'", "\\'")
    lineas, fila = [], []
    for fr, en in sorted(util.items()):
        fila.append("'%s':'%s'," % (esc(fr), esc(en)))
        if sum(len(x) for x in fila) > 66:
            lineas.append("    " + " ".join(fila))
            fila = []
    if fila:
        lineas.append("    " + " ".join(fila))
    cuerpo = "\n".join(lineas).rstrip(",")

    nuevo = ("  /* fr -> en. Lo genera tools/fr_alias.py comparando las 150\n"
             "     unidades por parejas: fr_aplica.py traduce la wordlist en su\n"
             "     sitio, asi que la palabra i del frances es la i del ingles.\n"
             "     Solo se listan las que llevan a un dibujo de verdad. */\n"
             "  const ALIAS = {\n" + cuerpo + "\n  };")
    t = t[:i] + nuevo + t[j:]
    io.open(JS, "w", encoding="utf-8",
            newline="\r\n" if crlf else "\n").write(t)


if __name__ == "__main__":
    mapa, util = construye()
    fotos = {os.path.splitext(x)[0]
             for x in os.listdir(os.path.join(ROOT, "assets", "vocab"))
             if x.endswith(".png")}
    print("parejas encontradas: %d | con dibujo: %d" % (len(mapa), len(util)))
    if "--contar" not in sys.argv:
        escribe(util)
        print("vocab-art.js reescrito")
