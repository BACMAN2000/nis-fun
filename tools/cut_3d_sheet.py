# -*- coding: utf-8 -*-
"""Trocea una hoja 3D de Gemini en PNG sueltos con fondo transparente.

Gemini devuelve los objetos en una rejilla sobre fondo blanco. Este script
la parte en celdas, recorta cada objeto a su contenido, quita el blanco y
descarta los restos del vecino que se cuelan en el borde de la celda.

    python tools/cut_3d_sheet.py hoja.jpg 5 2 bat dolphin kangaroo ... whale
"""
import os, sys
import numpy as np
from PIL import Image
from collections import deque

DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "vocab")


def slug(w):
    import re
    return re.sub(r"[^a-z0-9]+", "-", w.lower().replace("'", "")).strip("-")


def mayor_isla(alpha):
    """Mascara de la mancha mas grande. Sin scipy, con BFS sobre rejilla rala."""
    h, w = alpha.shape
    solido = alpha > 40
    vis = np.zeros((h, w), bool)
    mejor, mejor_tam = None, 0
    for sy in range(0, h, 3):
        for sx in range(0, w, 3):
            if not solido[sy, sx] or vis[sy, sx]:
                continue
            q = deque([(sy, sx)]); vis[sy, sx] = True; pts = []
            while q:
                y, x = q.popleft(); pts.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and solido[ny, nx] and not vis[ny, nx]:
                        vis[ny, nx] = True; q.append((ny, nx))
            if len(pts) > mejor_tam:
                mejor_tam, mejor = len(pts), pts
    m = np.zeros((h, w), bool)
    if mejor:
        ys, xs = zip(*mejor); m[list(ys), list(xs)] = True
    return m


def cortar(src, cols, filas, nombres, destino=DST, lado=320, previo=360):
    os.makedirs(destino, exist_ok=True)
    im = Image.open(src).convert("RGB")
    W, H = im.size
    tinta = np.array(im.convert("L")) < 232
    # area util: se recorta el marco que Gemini deja alrededor
    ys, xs = np.where(tinta)
    X0, X1 = max(0, xs.min() - 8), min(W, xs.max() + 8)
    Y0, Y1 = max(0, ys.min() - 8), min(H, ys.max() + 8)
    cw, ch = (X1 - X0) / cols, (Y1 - Y0) / filas

    hechos = []
    for idx, nombre in enumerate(nombres):
        if not nombre:                       # celda que no interesa
            continue
        f, c = divmod(idx, cols)
        x0, x1 = int(X0 + c * cw), int(X0 + (c + 1) * cw)
        y0, y1 = int(Y0 + f * ch), int(Y0 + (f + 1) * ch)
        sub = tinta[y0:y1, x0:x1]
        yy, xx = np.where(sub)
        if len(xx) == 0:
            print("  %-14s celda vacia" % nombre); continue
        m = 12
        a0 = max(0, xx.min() - m); a1 = min(sub.shape[1], xx.max() + m)
        b0 = max(0, yy.min() - m); b1 = min(sub.shape[0], yy.max() + m)
        crop = im.crop((x0 + a0, y0 + b0, x0 + a1, y0 + b1)).convert("RGBA")
        # Se reduce antes de limpiar el fondo porque la deteccion de islas
        # va pixel a pixel. Para un icono de vocabulario 360 sobra; una
        # figura de cuerpo entero necesita mas o sale a media resolucion.
        crop.thumbnail((previo, previo), Image.LANCZOS)

        arr = np.array(crop).astype(float)
        lum = arr[:, :, :3].mean(axis=2)
        alpha = np.clip((244 - lum) / 18.0, 0, 1)
        alpha[lum < 238] = 1.0
        arr[:, :, 3] = alpha * 255
        a8 = arr.astype(np.uint8)

        keep = mayor_isla(a8[:, :, 3])
        fuera = (a8[:, :, 3] > 40) & ~keep
        a8[fuera, 3] = 0
        out = Image.fromarray(a8, "RGBA")
        bb = out.getbbox()
        if bb:
            out = out.crop(bb)
        out.thumbnail((lado, lado), Image.LANCZOS)
        p = os.path.join(destino, slug(nombre) + ".png")
        out.save(p, optimize=True)
        hechos.append(nombre)
        print("  %-14s %sx%s  %3d KB" % (nombre, out.width, out.height,
                                         os.path.getsize(p) // 1024))
    return hechos


if __name__ == "__main__":
    if len(sys.argv) < 5:
        raise SystemExit(__doc__)
    src, cols, filas = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    nombres = [n if n != "-" else None for n in sys.argv[4:]]
    hechos = cortar(src, cols, filas, nombres)
    print("\n%d objetos guardados en assets/vocab/" % len(hechos))
