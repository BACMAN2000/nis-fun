# -*- coding: utf-8 -*-
"""Todo personaje tiene que tener fullbody.png.

El banner y la portada del nivel piden fullbody.png y, si no esta, caen a
pose-01.png con un onerror. Funciona, pero cada carga deja un 404 en la
consola y una peticion perdida: Pip, Luna y Kili nunca tuvieron fullbody y
se veian tres por pantalla.

Cuando el personaje no tiene una figura de cuerpo entero propia -dibujada
aparte y mas grande, como la de Ingrid- se copia su pose-01, que es
exactamente lo que el navegador acababa mostrando. No es un apano: Freya ya
estaba asi desde el principio, con las dos identicas.

Si algun dia se dibuja un fullbody de verdad, se guarda encima y este
script lo respeta: solo escribe donde falta.

    python tools/asegura_fullbody.py            dice que falta
    python tools/asegura_fullbody.py --arregla  lo copia
"""
import os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARS = os.path.join(ROOT, "assets", "characters")


def faltantes():
    for nivel in sorted(os.listdir(CHARS)):
        d = os.path.join(CHARS, nivel)
        if not os.path.isdir(d):
            continue
        for quien in sorted(os.listdir(d)):
            carpeta = os.path.join(d, quien)
            if not os.path.isdir(carpeta):
                continue
            full = os.path.join(carpeta, "fullbody.png")
            pose = os.path.join(carpeta, "pose-01.png")
            if not os.path.exists(full) and os.path.exists(pose):
                yield nivel, quien, pose, full


if __name__ == "__main__":
    arregla = "--arregla" in sys.argv
    n = 0
    for nivel, quien, pose, full in faltantes():
        n += 1
        if arregla:
            shutil.copyfile(pose, full)
        print("  %-9s %-11s %s" % (nivel, quien,
                                   "copiado de pose-01" if arregla else "sin fullbody"))
    if not n:
        print("  todos los personajes tienen fullbody")
    elif not arregla:
        print("")
        print("  %d sin fullbody (anade --arregla para copiarlos)" % n)
