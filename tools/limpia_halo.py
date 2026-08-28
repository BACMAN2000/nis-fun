# -*- coding: utf-8 -*-
"""Quita el fondo blanco que quedo pegado al recortar los personajes.

Algunos PNG de cuerpo completo salieron del recorte con restos del fondo
blanco: en la portada, con el mar detras, se ven como parches alrededor de
los brazos. Aqui se borra ese blanco, pero solo el que llega desde fuera de
la figura: el blanco de los ojos, de los calcetines o de una camiseta
blanca esta rodeado de dibujo, no toca el borde, y se queda.

Se avisa antes de tocar nada y no se pisa un archivo si el recorte se lleva
mas de un tercio de la figura, que seria senal de que algo salio mal.

    python tools/limpia_halo.py                 mira todos y dice cuales
    python tools/limpia_halo.py --arregla       ademas los corrige
"""
import os, sys
from collections import deque

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB = os.path.join(ROOT, "assets", "vocab")
CHARS = os.path.join(ROOT, "assets", "characters")

CLARO = 214          # a partir de aqui se considera "fondo blanco"
GRIS = 18            # y ademas casi sin color: el suelo que quedo pegado
                     # bajo los pies es gris claro, no blanco puro
ISLA_MIN = 120       # por debajo de esto es un brillo del ojo, no fondo
ISLA_LISA = 6.5      # el fondo original es liso; la ropa tiene sombreado
AVISO = 0.5          # a partir de este % de la figura, se avisa


def limpia(ruta):
    im = Image.open(ruta).convert("RGBA")
    a = np.array(im)
    alto, ancho = a.shape[:2]
    rgb = a[..., :3].astype(np.int16)
    alfa = a[..., 3]

    # candidato a fondo: casi blanco, o ya transparente
    claro = rgb.min(axis=2) >= CLARO
    sin_color = (rgb.max(axis=2) - rgb.min(axis=2)) <= GRIS
    blanco = (claro & sin_color) | (alfa < 24)
    fuera = np.zeros((alto, ancho), bool)

    cola = deque()
    for x in range(ancho):
        for y in (0, alto - 1):
            if blanco[y, x] and not fuera[y, x]:
                fuera[y, x] = True; cola.append((y, x))
    for y in range(alto):
        for x in (0, ancho - 1):
            if blanco[y, x] and not fuera[y, x]:
                fuera[y, x] = True; cola.append((y, x))

    while cola:
        y, x = cola.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < alto and 0 <= nx < ancho and blanco[ny, nx] and not fuera[ny, nx]:
                fuera[ny, nx] = True
                cola.append((ny, nx))

    # Quedan trozos de fondo ENCERRADOS: el hueco entre el brazo levantado y
    # el torso esta cerrado por la figura, asi que el relleno de fuera no
    # llega. Se buscan aparte, y solo se borran si son planos de verdad: el
    # fondo original es blanco liso, mientras que una camiseta blanca o unas
    # zapatillas tienen sombreado y no pasan el filtro.
    isla = blanco & ~fuera
    visto = np.zeros((alto, ancho), bool)
    for y0 in range(alto):
        for x0 in range(ancho):
            if not isla[y0, x0] or visto[y0, x0]:
                continue
            grupo, cola2 = [], deque([(y0, x0)])
            visto[y0, x0] = True
            while cola2:
                y, x = cola2.popleft()
                grupo.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < alto and 0 <= nx < ancho and isla[ny, nx] and not visto[ny, nx]:
                        visto[ny, nx] = True
                        cola2.append((ny, nx))
            if len(grupo) < ISLA_MIN:
                continue                       # brillos de los ojos, dientes
            ys = np.array([g[0] for g in grupo]); xs = np.array([g[1] for g in grupo])
            if rgb[ys, xs].std() > ISLA_LISA:
                continue                       # tiene sombreado: es ropa
            fuera[ys, xs] = True

    tenia = (alfa > 24)
    quita = fuera & tenia                     # lo que de verdad se borra
    if not quita.any():
        return None, 0.0

    prop = quita.sum() / max(1, tenia.sum())
    a[..., 3] = np.where(fuera, 0, alfa)
    return Image.fromarray(a, "RGBA"), prop


def dibujos():
    """Todo lo que se pega sobre una escena: los personajes y el banco de
    vocabulario. El banco entra aqui porque sus recortes se usan igual —en
    el zoo los animales van sobre la hierba— y el borde blanco que traen se
    nota tanto o mas que en un personaje."""
    for lvl in sorted(os.listdir(CHARS)):
        for quien in sorted(os.listdir(os.path.join(CHARS, lvl))):
            p = os.path.join(CHARS, lvl, quien, "fullbody.png")
            if os.path.exists(p):
                yield lvl, quien, p
    if os.path.isdir(VOCAB):
        for f in sorted(os.listdir(VOCAB)):
            if f.endswith(".png"):
                yield "vocab", f[:-4], os.path.join(VOCAB, f)


if __name__ == "__main__":
    arregla = "--arregla" in sys.argv
    for lvl, quien, p in dibujos():
        im, prop = limpia(p)
        if im is None:
            continue
        marca = ""
        if prop > 1 / 3:
            marca = "  <-- se lleva demasiado, NO se toca"
        elif arregla:
            im.save(p)
            marca = "  corregido"
        if prop * 100 >= AVISO or marca:
            print("  %-9s %-11s fondo blanco pegado: %4.1f%%%s"
                  % (lvl, quien, prop * 100, marca))
    if not arregla:
        print("")
        print("(nada se ha modificado: anade --arregla)")
