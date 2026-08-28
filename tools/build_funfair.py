# -*- coding: utf-8 -*-
"""Dibuja la feria para Movers 3.

La historia de la unidad pasa entera ahi: "Yesterday the funfair came to
town, with its big wheel, its ring game and its mountain of popcorn! Mateo
lost his ticket TWO times, Erik won a little green dragon, and everyone
screamed on the big wheel." La lamina era el anfiteatro del campus, que no
tiene nada que ver.

Como el zoo y la cocina del faro, la feria no esta en el campus de Nordic y
no hay foto, asi que se dibuja: la noria, la caseta de los aros, la de las
palomitas y los banderines. La franja de abajo se deja despejada para Erik y
Mateo, que los pega tools/build_unit_scenes.py.

Salida: assets/scenes/funfair.jpg

    python tools/build_funfair.py
"""
import math, os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(ROOT, "assets", "scenes")

W, H = 1720, 900

# Atardecer: la historia dice que estuvieron alli todo el dia
CIELO = [(250, 202, 154), (196, 214, 238)]
TIERRA = (196, 172, 140)
TIERRA2 = (178, 154, 124)
ROJO = (206, 78, 68)
CREMA = (250, 244, 232)
MADERA = (150, 104, 62)
METAL = (168, 176, 186)
AZUL = (78, 132, 180)
VERDE = (86, 158, 108)
AMARILLO = (232, 182, 66)


def fuente(px):
    for n in ("segoeuib.ttf", "arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(n, px)
        except Exception:
            pass
    return ImageFont.load_default()


def degradado(d, caja, c1, c2):
    x0, y0, x1, y1 = caja
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        d.line([(x0, y), (x1, y)], fill=c)


def noria(d, cx, cy, r):
    """La big wheel. Es lo primero que nombra la historia, asi que es lo
    mas grande de la lamina."""
    d.line([(cx - r * .55, cy + r + 60), (cx, cy)], fill=MADERA, width=22)
    d.line([(cx + r * .55, cy + r + 60), (cx, cy)], fill=MADERA, width=22)

    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=METAL, width=13)
    d.ellipse([cx - r * .72, cy - r * .72, cx + r * .72, cy + r * .72],
              outline=METAL, width=8)

    colores = [ROJO, AMARILLO, AZUL, VERDE, (196, 132, 188), (236, 148, 84)]
    n = 12
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        d.line([(cx, cy), (px, py)], fill=METAL, width=6)
        # la cabina cuelga siempre hacia abajo, gire lo que gire la rueda
        c = colores[i % len(colores)]
        d.line([(px, py), (px, py + 16)], fill=METAL, width=4)
        d.rounded_rectangle([px - 26, py + 16, px + 26, py + 56], 10, fill=c,
                            outline=(70, 60, 54), width=3)
        d.rectangle([px - 18, py + 24, px + 18, py + 40], fill=(252, 248, 240))
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(70, 60, 54))


def caseta(d, x0, x1, suelo, alto, titulo, relleno):
    """Una caseta de feria: toldo a rayas, mostrador y su cartel."""
    y0 = suelo - alto
    d.rectangle([x0, y0 + 54, x1, suelo], fill=CREMA, outline=MADERA, width=5)
    d.rectangle([x0, suelo - 74, x1, suelo], fill=MADERA)

    # el toldo, a rayas
    d.polygon([(x0 - 22, y0 + 58), (x0 + 8, y0), (x1 - 8, y0), (x1 + 22, y0 + 58)],
              fill=CREMA, outline=(190, 176, 158))
    ancho = (x1 - x0) / 8
    for k in range(8):
        if k % 2:
            continue
        a = x0 + ancho * k
        d.polygon([(a, y0 + 58), (a + ancho * .5, y0), (a + ancho * 1.5, y0),
                   (a + ancho, y0 + 58)], fill=ROJO)
    relleno(d, x0, x1, y0, suelo)
    d.text(((x0 + x1) / 2, y0 + 84), titulo, font=fuente(26),
           fill=(96, 66, 48), anchor="mm")


def aros(d, x0, x1, y0, suelo):
    """Los aros colgados de la caseta del ring game."""
    for k in range(5):
        cx = x0 + (x1 - x0) * (k + .5) / 5
        cy = y0 + 150
        c = [ROJO, AMARILLO, AZUL, VERDE, (196, 132, 188)][k]
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=c, width=9)
    for k in range(3):
        bx = x0 + (x1 - x0) * (k + 1) / 4
        d.rectangle([bx - 9, suelo - 118, bx + 9, suelo - 74], fill=(120, 104, 88))
        d.ellipse([bx - 16, suelo - 140, bx + 16, suelo - 108], fill=VERDE)


def palomitas(d, x0, x1, y0, suelo):
    """El cucurucho de palomitas: la montana que dice la historia."""
    cx = (x0 + x1) / 2
    base = suelo - 92
    d.polygon([(cx - 46, base - 108), (cx + 46, base - 108), (cx + 30, base),
               (cx - 30, base)], fill=CREMA, outline=(198, 92, 82), width=4)
    for k in range(5):
        rx = cx - 36 + k * 18
        d.line([(rx, base - 108), (rx - 6, base)], fill=(224, 130, 120), width=6)
    # la montana que se desborda
    for dx, dy, r in ((0, -122, 24), (-27, -113, 19), (27, -113, 19),
                      (-13, -137, 17), (14, -137, 17), (0, -152, 14)):
        d.ellipse([cx + dx - r, base + dy - r, cx + dx + r, base + dy + r],
                  fill=(252, 240, 208), outline=(226, 208, 168), width=2)


def banderines(d, y, desde, hasta, n=16):
    """Los banderines que cruzan la feria de lado a lado."""
    colores = [ROJO, AMARILLO, AZUL, VERDE, CREMA]
    ancho = (hasta - desde) / n
    for k in range(n):
        x = desde + ancho * k
        caida = 26 * math.sin(math.pi * (k + .5) / n)
        d.line([(x, y + caida * .8), (x + ancho, y + caida * .8)],
               fill=(120, 104, 88), width=4)
        d.polygon([(x, y + caida * .8), (x + ancho, y + caida * .8),
                   (x + ancho / 2, y + caida * .8 + 40)], fill=colores[k % 5])


def feria():
    im = Image.new("RGB", (W, H), CIELO[0])
    d = ImageDraw.Draw(im)

    suelo_y = int(H * .74)
    degradado(d, (0, 0, W, suelo_y), CIELO[0], CIELO[1])

    # colinas al fondo, como en las demas escenas del curso
    d.ellipse([-300, suelo_y - 220, int(W * .50), suelo_y + 120], fill=(160, 190, 150))
    d.ellipse([int(W * .48), suelo_y - 190, W + 300, suelo_y + 120], fill=(148, 180, 142))

    # el suelo de tierra pisada
    d.rectangle([0, suelo_y, W, H], fill=TIERRA)
    for k in range(9):
        yy = suelo_y + 14 + k * 26
        d.line([(0, yy), (W, yy)], fill=TIERRA2, width=3)

    noria(d, int(W * .26), int(H * .34), 250)
    caseta(d, int(W * .55), int(W * .76), suelo_y, 330, "RING GAME", aros)
    caseta(d, int(W * .79), int(W * .97), suelo_y, 300, "POPCORN", palomitas)
    banderines(d, int(H * .07), int(W * .44), W)

    im = im.convert("RGB")
    suave = im.filter(ImageFilter.GaussianBlur(W / 560.0))
    mask = Image.new("L", (W, H))
    px = mask.load()
    for y in range(H):
        v = int(255 * max(0.0, min(1.0, 1.05 - 1.5 * (y / H))))
        for x in range(W):
            px[x, y] = v
    return Image.composite(suave, im, mask)


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    p = os.path.join(SALIDA, "funfair.jpg")
    feria().save(p, quality=90, optimize=True, progressive=True)
    print("  funfair.jpg  %d x %d  %d KB" % (W, H, os.path.getsize(p) // 1024))
