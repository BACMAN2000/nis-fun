# -*- coding: utf-8 -*-
"""Montaje etiquetado de los pose-NN.png de una carpeta, para revisión visual.
Uso: python montage.py <dir> <out.png>
"""
import sys, os, glob
from PIL import Image, ImageDraw

d, out = sys.argv[1], sys.argv[2]
files = sorted(glob.glob(os.path.join(d, "pose-*.png")))
CELL = 260
cols = min(5, len(files))
rows = -(-len(files) // cols)
im = Image.new("RGB", (cols * CELL, rows * CELL + 20), "#dddddd")
dr = ImageDraw.Draw(im)
for i, f in enumerate(files):
    p = Image.open(f)
    p.thumbnail((CELL - 20, CELL - 30))
    x, y = (i % cols) * CELL, (i // cols) * CELL
    im.paste(p, (x + (CELL - p.width) // 2, y + 24 + (CELL - 30 - p.height) // 2), p if p.mode == "RGBA" else None)
    dr.rectangle([x, y, x + CELL - 2, y + 20], fill="#222222")
    dr.text((x + 6, y + 4), os.path.basename(f), fill="#ffffff")
im.save(out)
print(out, im.size, len(files), "imgs")
