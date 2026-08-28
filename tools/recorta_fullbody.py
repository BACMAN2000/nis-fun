# -*- coding: utf-8 -*-
"""Deja lista como asset una figura de cuerpo completo recien generada.

El generador devuelve la figura sobre fondo blanco y en JPG, y el curso los
quiere en PNG con fondo transparente y recortados al contenido. Esto es lo
que hace este script, ademas de avisar si la imagen viene con menos
resolucion de la que la portada necesita.

El fondo se borra desde fuera hacia dentro: solo desaparece el blanco que se
alcanza desde el borde de la imagen. El blanco de los ojos, de unas
zapatillas o de una camiseta esta rodeado de dibujo y se queda. El borde de
la figura se suaviza con una rampa entre los dos umbrales, que es lo que
evita el halo blanco que se veia en la portada con el mar detras.

    python tools/recorta_fullbody.py <imagen> <nivel> <slug>
    python tools/recorta_fullbody.py descarga.jpg starters freya

    --mira      no escribe nada, solo dice como quedaria
    --pose NN   guarda como pose-NN.png en vez de fullbody.png
"""
import os
import sys
from collections import deque

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARS = os.path.join(ROOT, "assets", "characters")

BLANCO = 246        # a partir de aqui es fondo del todo
CASI = 224          # por debajo de aqui es figura; en medio, rampa de alpha
ALTO_MINIMO = 800   # la portada pinta a 200 CSS px, y en pantalla retina son 400


def sin_fondo(im):
    """Devuelve la imagen con el fondo blanco exterior en transparente."""
    im = im.convert("RGBA")
    a = np.array(im)
    claro = a[:, :, :3].min(axis=2)           # cuanto le falta al pixel para ser blanco
    alcanzable = claro >= CASI                # candidatos a fondo
    alto, ancho = claro.shape

    # inundacion desde el borde: solo se borra el blanco que comunica con fuera
    fuera = np.zeros((alto, ancho), dtype=bool)
    cola = deque()
    for x in range(ancho):
        for y in (0, alto - 1):
            if alcanzable[y, x] and not fuera[y, x]:
                fuera[y, x] = True; cola.append((y, x))
    for y in range(alto):
        for x in (0, ancho - 1):
            if alcanzable[y, x] and not fuera[y, x]:
                fuera[y, x] = True; cola.append((y, x))
    while cola:
        y, x = cola.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < alto and 0 <= nx < ancho and alcanzable[ny, nx] and not fuera[ny, nx]:
                fuera[ny, nx] = True; cola.append((ny, nx))

    # rampa: blanco del todo -> invisible; a medio camino -> medio transparente
    rampa = np.clip((BLANCO - claro.astype(np.int16)) * 255 // (BLANCO - CASI), 0, 255)
    alpha = a[:, :, 3].astype(np.int16)
    alpha[fuera] = np.minimum(alpha[fuera], rampa[fuera])
    a[:, :, 3] = alpha.astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def recorta(im):
    caja = im.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox()
    return im.crop(caja) if caja else im


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    solo_mira = "--mira" in sys.argv
    pose = None
    if "--pose" in sys.argv:
        pose = sys.argv[sys.argv.index("--pose") + 1]
    if len(args) < 3:
        print(__doc__)
        return 2
    origen, nivel, slug = args[0], args[1], args[2]

    im = Image.open(origen)
    entra = im.size
    im = recorta(sin_fondo(im))

    nombre = "fullbody.png" if pose is None else "pose-%s.png" % str(pose).zfill(2)
    destino = os.path.join(CHARS, nivel, slug, nombre)
    if not os.path.isdir(os.path.dirname(destino)):
        print("no existe %s — ¿nivel o slug mal escrito?" % os.path.dirname(destino))
        return 1

    aviso = ""
    if im.height < ALTO_MINIMO:
        aviso = "  <-- BAJO: la portada quiere %d px de alto o mas" % ALTO_MINIMO
    print("%s  %dx%d  ->  %dx%d%s" % (os.path.basename(origen), entra[0], entra[1],
                                      im.width, im.height, aviso))

    if solo_mira:
        print("(--mira: no se ha escrito nada)")
        return 0
    if os.path.exists(destino):
        viejo = Image.open(destino)
        print("reemplaza %s (%dx%d)" % (destino, viejo.width, viejo.height))
    im.save(destino)
    print("guardado en %s" % destino)
    return 0


if __name__ == "__main__":
    sys.exit(main())
