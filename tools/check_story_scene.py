# -*- coding: utf-8 -*-
"""Comprueba que la ilustracion de una unidad ensena lo que cuenta su historia.

En Starters 1 la historia dice "three little cars" y en el dibujo habia un
solo coche. El alumno mira la imagen mientras lee, asi que cada cosa que
nombra el texto tiene que estar, y en la cantidad que dice.

Se leen las dos piezas de texto de la unidad:
  scene.intro    la historia de apertura
  scene.bubble   lo que dice el personaje en su bocadillo

De ahi se sacan los objetos del vocabulario que se nombran y con cuantos
("a red ball" = 1, "three little cars" = 3), y se compara con lo que el
generador de escenas coloca de verdad.

Solo mira las unidades con texto escrito a mano: las demas llevan una
introduccion de plantilla que no nombra objetos concretos, asi que no puede
contradecir al dibujo.

    python tools/check_story_scene.py
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
sys.path.insert(0, os.path.join(ROOT, "tools"))

NUMEROS = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
           "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}

# plural -> singular, lo justo para el vocabulario de estos libros
def singular(p):
    if p.endswith("ies"):
        return p[:-3] + "y"
    if p.endswith("es") and p[:-2].endswith(("sh", "ch", "x", "s")):
        return p[:-2]
    if p.endswith("s") and not p.endswith("ss"):
        return p[:-1]
    return p


def menciones(texto, vocabulario):
    """{objeto: cuantos} segun lo que dice el texto."""
    pide = {}
    palabras = re.findall(r"[A-Za-z']+", texto.lower())
    for i, p in enumerate(palabras):
        base = singular(p)
        if base not in vocabulario:
            continue
        # el numero es la ultima palabra contable de las tres anteriores
        cuantos = 1
        for atras in palabras[max(0, i - 3):i][::-1]:
            if atras in NUMEROS:
                cuantos = NUMEROS[atras]
                break
        pide[base] = max(pide.get(base, 0), cuantos)
    return pide


def dibujables():
    """Lo que se puede poner en una escena: hay dibujo 3D para ello."""
    d = os.path.join(ROOT, "assets", "vocab")
    return {f[:-4] for f in os.listdir(d) if f.endswith(".png")}


def revisa(escenas):
    """escenas = {'nivel/n': (fondo, [(objeto,x,y,s), ...])}"""
    problemas, sin_escena = [], []
    hay_dibujo = dibujables()
    for lvl in ("starters", "movers", "flyers"):
        carpeta = os.path.join(CONTENT, lvl)
        if not os.path.isdir(carpeta):
            continue
        for f in sorted(os.listdir(carpeta)):
            if not f.startswith("unit-"):
                continue
            d = json.load(io.open(os.path.join(carpeta, f), encoding="utf-8"))
            esc = d.get("scene") or {}
            texto = " ".join(x for x in (esc.get("intro"), esc.get("bubble")) if x)
            if not texto:
                continue
            vocab = set()
            for w in d.get("wordlist", []):
                vocab.add((w if isinstance(w, str) else w.get("w", "")).lower())
            # solo lo que se PUEDE dibujar: de los verbos y los adjetivos
            # del wordlist no hay figura, y no tiene sentido exigirlos
            pide = {k: v for k, v in menciones(texto, vocab).items() if k in hay_dibujo}
            if not pide:
                continue

            clave = "%s/%d" % (lvl, d["number"])
            if clave not in escenas:
                sin_escena.append((clave, sorted(pide)))
                continue
            puestos = {}
            for nombre, *_ in (escenas.get(clave) or ("", []))[1]:
                puestos[nombre] = puestos.get(nombre, 0) + 1

            for obj, cuantos in sorted(pide.items()):
                hay = puestos.get(obj, 0)
                if hay == 0:
                    problemas.append((clave, obj, cuantos, 0, "no esta en el dibujo"))
                elif hay != cuantos:
                    problemas.append((clave, obj, cuantos, hay, "cantidad distinta"))
    return problemas, sin_escena


if __name__ == "__main__":
    import build_unit_scenes as B
    fallos, sin_escena = revisa(B.ESCENAS)
    if not fallos:
        print("  todo cuadra: lo que cuenta cada historia esta en su dibujo")
    else:
        print("  %d desajustes entre la historia y el dibujo:" % len(fallos))
        for clave, obj, pide, hay, que in fallos:
            print("   %-12s %-10s la historia dice %d, el dibujo tiene %d  (%s)"
                  % (clave, obj, pide, hay, que))
    if sin_escena:
        print("")
        print("  %d unidades nombran cosas que si se pueden dibujar pero"
              " todavia no tienen escena propia:" % len(sin_escena))
        for clave, objs in sin_escena[:14]:
            print("   %-12s %s" % (clave, ", ".join(objs)))
        if len(sin_escena) > 14:
            print("   ... y %d mas" % (len(sin_escena) - 14))
    raise SystemExit(1 if fallos else 0)
