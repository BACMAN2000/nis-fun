# -*- coding: utf-8 -*-
"""Recorta una hoja de personaje (grid sobre fondo blanco) en poses individuales.

Uso:
  python segment_sheet.py <sheet.png> <out_dir> <pose_nums>
  pose_nums = números de pose destino en orden de lectura, ej. "1,2,3,4,5,6,7,8,10"

Salida: <out_dir>/pose-NN.png (fondo transparente, recortado con margen).
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw

WHITE_T = 232          # umbral: píxel "de fondo" si los 3 canales >= WHITE_T
MIN_BAND_FRAC = 0.004  # una fila/col cuenta como "con contenido" si >0.4% de píxeles

def bands(profile, min_size=12):
    """Devuelve [(ini,fin)] de tramos consecutivos con contenido."""
    out, start = [], None
    for i, v in enumerate(profile):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= min_size:
                out.append((start, i))
            start = None
    if start is not None and len(profile) - start >= min_size:
        out.append((start, len(profile)))
    return out

def remove_bg(cell):
    """Fondo blanco → transparente (flood fill desde los 4 bordes)."""
    im = cell.convert("RGB")
    SENT = (255, 0, 255)
    w, h = im.size
    px = im.load()
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
             (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
    for s in seeds:
        if px[s] != SENT and all(c >= WHITE_T - 12 for c in px[s]):
            ImageDraw.floodfill(im, s, SENT, thresh=38)
    a = np.array(im)
    mask = (a[:, :, 0] == 255) & (a[:, :, 1] == 0) & (a[:, :, 2] == 255)
    rgba = np.dstack([np.array(cell.convert("RGB")), np.where(mask, 0, 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA")

def main(sheet_path, out_dir, pose_nums):
    im = Image.open(sheet_path).convert("RGB")
    a = np.array(im)
    fg = ~np.all(a >= WHITE_T, axis=2)
    rows = bands([r.sum() > fg.shape[1] * MIN_BAND_FRAC for r in fg], min_size=30)
    cells = []
    for (r0, r1) in rows:
        band = fg[r0:r1]
        cols = bands([c.sum() > (r1 - r0) * MIN_BAND_FRAC for c in band.T], min_size=30)
        for (c0, c1) in cols:
            sub = fg[r0:r1, c0:c1]
            ys, xs = np.where(sub)
            if len(ys) < 400:      # ruido
                continue
            m = 14
            box = (max(0, c0 + xs.min() - m), max(0, r0 + ys.min() - m),
                   min(im.width, c0 + xs.max() + m), min(im.height, r0 + ys.max() + m))
            cells.append(box)
    os.makedirs(out_dir, exist_ok=True)
    nums = [int(x) for x in pose_nums.split(",")]
    if len(cells) != len(nums):
        print(f"AVISO: {len(cells)} celdas detectadas, {len(nums)} poses esperadas")
    for box, n in zip(cells, nums):
        out = remove_bg(im.crop(box))
        out.save(os.path.join(out_dir, f"pose-{n:02d}.png"))
    print(f"{min(len(cells), len(nums))} poses -> {out_dir}  (celdas={len(cells)})")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
