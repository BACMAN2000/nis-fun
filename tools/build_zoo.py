# -*- coding: utf-8 -*-
"""Dibuja la entrada del zoo para Movers 1.

La regla del curso es que los escenarios son del campus de Nordic, pero la
historia de esta unidad pasa en el zoo y del zoo no hay fotos del colegio.
Es la excepcion, asi que el sitio se dibuja aqui en vez de salir de una
foto: arco de entrada, taquilla, vallas, recintos al fondo y los carteles
de lo que hay dentro.

Encima van los ninos del nivel mirando el plano y decidiendo por donde
empezar, que es lo que cuenta la unidad.

Salida: assets/scenes/zoo.jpg   (el sitio, sin personajes)

    python tools/build_zoo.py
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(ROOT, "assets", "scenes")

W, H = 1720, 900

CIELO = [(178, 222, 244), (226, 243, 250)]
HIERBA = [(126, 178, 104), (150, 196, 122)]
CAMINO = (222, 206, 176)
MADERA = (150, 104, 62)
MADERA_C = (176, 128, 82)
TECHO = (206, 88, 74)
HOJA = (86, 148, 90)
HOJA_C = (110, 172, 108)


def fuente(px, negrita=True):
    for n in ("segoeuib.ttf" if negrita else "segoeui.ttf", "arialbd.ttf", "arial.ttf"):
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


def arbol(d, x, y, e):
    d.ellipse([x - 9 * e, y - 6 * e, x + 9 * e, y + 6 * e], fill=(60, 90, 60, 40))
    d.rectangle([x - 7 * e, y - 52 * e, x + 7 * e, y], fill=MADERA)
    for dx, dy, r in ((0, -86, 42), (-30, -62, 32), (30, -62, 32), (0, -54, 34)):
        d.ellipse([x + (dx - r) * e, y + (dy - r) * e, x + (dx + r) * e, y + (dy + r) * e],
                  fill=HOJA if r > 33 else HOJA_C)


def valla(d, x0, x1, y, alto=54):
    d.rectangle([x0, y - alto * .55, x1, y - alto * .40], fill=MADERA_C)
    d.rectangle([x0, y - alto * .20, x1, y - alto * .05], fill=MADERA_C)
    x = x0
    while x < x1:
        d.rectangle([x, y - alto, x + 12, y], fill=MADERA)
        d.polygon([(x, y - alto), (x + 6, y - alto - 10), (x + 12, y - alto)], fill=MADERA)
        x += 46


def cartel(d, x, y, texto, ancho=190, alto=54, fondo=(247, 244, 238)):
    d.rounded_rectangle([x - ancho // 2, y, x + ancho // 2, y + alto], 10,
                        fill=fondo, outline=MADERA, width=4)
    d.rectangle([x - 6, y + alto, x + 6, y + alto + 42], fill=MADERA)
    f = fuente(int(alto * .46))
    d.text((x, y + alto // 2), texto, font=f, fill=(60, 46, 32), anchor="mm")


def recinto(d, x, y, ancho, nombre):
    """Un recinto al fondo: valla curva, seto y su cartelito."""
    d.ellipse([x - ancho // 2, y - 46, x + ancho // 2, y + 26], fill=HOJA_C)
    valla(d, x - ancho // 2, x + ancho // 2, y + 30, 42)
    cartel(d, x, y + 44, nombre, ancho=int(ancho * .78), alto=34)


def zoo():
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)

    degradado(d, (0, 0, W, int(H * .52)), CIELO[0], CIELO[1])
    # colinas
    d.ellipse([-260, int(H * .30), int(W * .46), int(H * .70)], fill=(158, 194, 152))
    d.ellipse([int(W * .52), int(H * .28), W + 260, int(H * .68)], fill=(146, 186, 142))
    degradado(d, (0, int(H * .52), W, H), HIERBA[0], HIERBA[1])

    # nubes
    for cx, cy, e in ((300, 120, 1.0), (900, 90, .7), (1420, 150, .9)):
        for dx, dy, r in ((0, 0, 46), (40, 8, 34), (-38, 10, 30)):
            d.ellipse([cx + (dx - r) * e, cy + (dy - r) * e, cx + (dx + r) * e, cy + (dy + r) * e],
                      fill=(255, 255, 255))

    # recintos al fondo, con su nombre: es lo que van a visitar
    recinto(d, 210, int(H * .40), 300, "MONKEYS")
    recinto(d, 650, int(H * .44), 290, "LIONS")
    recinto(d, 1070, int(H * .44), 290, "PENGUINS")
    recinto(d, 1510, int(H * .40), 300, "ELEPHANTS")

    for x, e in ((110, 1.0), (430, .8), (860, .75), (1290, .85), (1640, 1.0)):
        arbol(d, x, int(H * .60), e)

    # camino de entrada, ancho por delante
    d.polygon([(int(W * .34), int(H * .60)), (int(W * .66), int(H * .60)),
               (W, H), (0, H)], fill=CAMINO)
    for k in range(5):
        y = int(H * .66) + k * 48
        d.line([(int(W * .30) - k * 46, y), (int(W * .70) + k * 46, y)],
               fill=(210, 192, 160), width=3)

    # arco de entrada
    ax0, ax1, ay = int(W * .28), int(W * .72), int(H * .60)
    d.rectangle([ax0, ay - 300, ax0 + 46, ay], fill=MADERA)
    d.rectangle([ax1 - 46, ay - 300, ax1, ay], fill=MADERA)
    d.rectangle([ax0 - 22, ay - 348, ax1 + 22, ay - 288], fill=MADERA_C)
    d.polygon([(ax0 - 40, ay - 348), (W // 2, ay - 430), (ax1 + 40, ay - 348)], fill=TECHO)
    f = fuente(62)
    d.text((W // 2, ay - 318), "NORDIC ZOO", font=f, fill=(255, 246, 232), anchor="mm")

    # taquilla a la izquierda del arco
    d.rounded_rectangle([ax0 - 300, ay - 176, ax0 - 130, ay], 12, fill=(238, 226, 200),
                        outline=MADERA, width=5)
    d.polygon([(ax0 - 322, ay - 176), (ax0 - 215, ay - 232), (ax0 - 108, ay - 176)], fill=TECHO)
    d.rounded_rectangle([ax0 - 268, ay - 140, ax0 - 162, ay - 76], 8, fill=(176, 214, 232),
                        outline=MADERA, width=4)
    cartel(d, ax0 - 215, ay - 60, "TICKETS", ancho=132, alto=32)

    valla(d, 0, ax0 - 320, ay + 6)
    valla(d, ax1 + 10, W, ay + 6)

    # un poco de profundidad, como en las demas escenas del curso
    suave = im.filter(ImageFilter.GaussianBlur(W / 520.0))
    mask = Image.new("L", (W, H))
    px = mask.load()
    for y in range(H):
        v = int(255 * max(0.0, min(1.0, 1.05 - 1.5 * (y / H))))
        for x in range(W):
            px[x, y] = v
    return Image.composite(suave, im, mask)


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    p = os.path.join(SALIDA, "zoo.jpg")
    zoo().save(p, quality=90, optimize=True, progressive=True)
    print("  zoo.jpg  %d x %d  %d KB" % (W, H, os.path.getsize(p) // 1024))
