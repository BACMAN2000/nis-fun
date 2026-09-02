# -*- coding: utf-8 -*-
"""Busca lo que sigue en ingles en la version francesa.

Tres sitios distintos, tres problemas distintos:
  contenido  - una cadena que se quedo sin traducir en content-fr
  motor      - texto que el motor pinta directamente, sin pasar por T()
  readers    - los cuentos de la pantalla de lectura, que son otro contenido

Detectar "ingles" sin diccionario da falsos positivos (train, orange, six son
palabras de los dos idiomas), asi que se buscan palabras que SOLO existen en
ingles y son muy frecuentes: the, and, you, with, what...
"""
import glob, io, json, os, re, sys

ROOT = r"C:\Projects\nis-portal\nis-fun"

# Palabras que en frances no existen (o no con esa forma) y que delatan una
# frase inglesa entera. Se piden dos o mas para no marcar un nombre propio.
DELATORAS = r"\b(the|and|you|your|with|what|which|when|where|there|this|that|" \
            r"they|have|has|are|is|was|were|will|would|can't|don't|doesn't|" \
            r"write|read|listen|choose|match|draw|look|answer|about|from|" \
            r"because|but|for|not|his|her|their|our|my|it's|i'm)\b"


# Y las de la otra orilla: si aparecen, la frase es francesa aunque lleve una
# palabra que tambien exista en ingles.
FRANCESAS = r"\b(le|la|les|des|une|un|du|de|et|est|sont|avec|dans|pour|sur|" \
            r"que|qui|quoi|ton|ta|tes|mon|ma|mes|son|sa|ses|nous|vous|ils|" \
            r"elle|elles|tu|je|au|aux|chez|tres|tres|oui|non|puis|alors|" \
            r"ecris|ecoute|regarde|touche|choisis|associe|colorie|dessine|" \
            r"complete|entoure|coche|relie|trouve|lis|parle)\b"


def ingles(t, minimo=2):
    if not isinstance(t, str) or len(t) < 6:
        return False
    b = t.lower()
    if len(re.findall(DELATORAS, b)) < minimo:
        return False
    # "Le grand match de la recre" lleva match, pero tambien le, la y de:
    # es frances con una palabra que se escribe igual en los dos idiomas.
    return not re.search(FRANCESAS, b)


def recorre(o, ruta=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from recorre(v, f"{ruta}.{k}" if ruta else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from recorre(v, f"{ruta}[{i}]")
    elif isinstance(o, str):
        yield ruta, o


def audita_contenido():
    malas = []
    for f in sorted(glob.glob(os.path.join(ROOT, "content-fr", "*", "*.json"))):
        d = json.load(io.open(f, encoding="utf-8"))
        for ruta, t in recorre(d):
            if ruta.endswith(("nota",)):      # la nota del scope va en castellano a proposito
                continue
            if ingles(t):
                malas.append((os.path.relpath(f, ROOT), ruta, t[:90]))
    return malas


def audita_motor():
    """El motor: lo hace fr_motor.py, que sabe leer JavaScript.

    Aqui vivia una version a base de expresiones regulares que se dejaba
    "Start learning" y "Play with sound" —no llevan ninguna palabra que
    solo exista en ingles— y que no miraba fuera de index.html, que es
    donde estaba casi todo. No tiene sentido mantener dos.
    """
    import fr_motor
    fuera = []
    for f in fr_motor.ARCHIVOS:
        for t in fr_motor.audita(f):
            fuera.append(os.path.basename(f) + ": " + t)
    return fuera


def audita_readers():
    """Los cuentos franceses: el texto de cada pagina y el de la actividad."""
    malas = []
    for f in sorted(glob.glob(os.path.join(ROOT, "readers", "data-fr", "*.json"))):
        d = json.load(io.open(f, encoding="utf-8"))
        for ruta, t in recorre(d):
            if ruta.split(".")[-1].split("[")[0] in ("id", "img", "portada", "lang", "grado"):
                continue
            if ingles(t):
                malas.append((os.path.relpath(f, ROOT), ruta, t[:90]))
    return malas


if __name__ == "__main__":
    c = audita_contenido()
    print(f"CONTENIDO: {len(c)} cadenas sospechosas de seguir en ingles")
    for f, r, t in c[:15]:
        print(f"   {f} {r}\n      {t}")
    m = audita_motor()
    print(f"\nMOTOR: {len(m)} textos que no pasan por T()")
    for t in m[:40]:
        print("   ", t)
    r = audita_readers()
    print(f"\nREADERS (cuentos): {len(r)} cadenas sospechosas de seguir en ingles")
    for f, ru, t in r[:15]:
        print(f"   {f} {ru}\n      {t}")
