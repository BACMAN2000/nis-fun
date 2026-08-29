# -*- coding: utf-8 -*-
"""Mete los cuatro renderers visuales en un engine/index.html.

Existe porque hay DOS copias del motor y no siempre van a la par:

    C:/Projects/nis-fun/engine/index.html            el repo del curso
    C:/Projects/nis-portal/nis-fun/engine/index.html la copia que se publica

El 29-ago-2026 la copia del portal iba 233 lineas POR DELANTE (otra sesion le
habia metido los ajustes de movil, el estado de carga y la accesibilidad).
Copiar un archivo encima del otro se lleva por delante ese trabajo, asi que
los cambios se aplican por ANCLA de texto, no por copia.

Es idempotente: si el motor ya tiene los renderers, no hace nada. Y si un
ancla no aparece, avisa y no toca el archivo — mejor no aplicar nada que
dejar un motor a medias que no carga.

    python tools/patch_engine_visual.py                       # las dos copias
    python tools/patch_engine_visual.py ruta/al/index.html    # una concreta
"""
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TROZOS = os.path.join(RAIZ, "tools", "visual")

POR_DEFECTO = [
    os.path.join(RAIZ, "engine", "index.html"),
    os.path.join(os.path.dirname(RAIZ), "nis-portal", "nis-fun", "engine", "index.html"),
]

MARCA = "label_people(act, el){"

# (nombre, ancla, donde va el trozo respecto al ancla)
PARCHES = [
    ("estilos.css",  "\n</style>",             "antes"),
    ("renderers.js", "\nconst RENDER = {\n",   "sustituye"),
    ("selfcheck.js",
     "    if (a.type === 'pairwork') puedo.push('I can talk about this topic with a partner.');",
     "despues"),
    ("limpia.js",
     "    cfg.entradas().forEach(i => { i.value = ''; i.className = ''; });",
     "sustituye"),
]


def trozo(nombre):
    return io.open(os.path.join(TROZOS, nombre), encoding="utf-8").read()


def aplica(ruta):
    if not os.path.exists(ruta):
        return "no existe"
    t = io.open(ruta, encoding="utf-8").read()
    if MARCA in t:
        return "ya lo tiene"

    # Primero se comprueban TODAS las anclas. Si falta una, no se escribe nada.
    for nombre, ancla, _ in PARCHES:
        if t.count(ancla) != 1:
            return "ancla de %s aparece %d veces (se esperaba 1) — no toco el archivo" % (
                nombre, t.count(ancla))

    for nombre, ancla, donde in PARCHES:
        pieza = trozo(nombre)
        if donde == "antes":
            t = t.replace(ancla, "\n" + pieza + ancla.lstrip("\n"), 1)
        elif donde == "despues":
            t = t.replace(ancla, ancla + "\n" + pieza.rstrip("\n"), 1)
        else:
            t = t.replace(ancla, pieza, 1)

    io.open(ruta, "w", encoding="utf-8").write(t)
    return "parcheado"


def main():
    rutas = sys.argv[1:] or POR_DEFECTO
    for r in rutas:
        print("%-58s %s" % (os.path.relpath(r, os.path.dirname(RAIZ)), aplica(r)))


if __name__ == "__main__":
    main()
