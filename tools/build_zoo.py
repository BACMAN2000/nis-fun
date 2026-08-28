# -*- coding: utf-8 -*-
"""Dibuja la entrada del zoo para Movers 1.

La regla del curso es que los escenarios son del campus de Nordic, pero la
historia de esta unidad pasa en el zoo y del zoo no hay fotos del colegio.
Es la excepcion, asi que el sitio se dibuja aqui en vez de salir de una
foto: arco de entrada, taquilla, vallas, recintos al fondo y los carteles
de lo que hay dentro.

Los animales no se dibujan aqui: se pegan del banco de vocabulario, que
ya los tiene en el mismo estilo 3D que el resto del curso. Antes la escena
era solo el arco y unos carteles, y un zoo sin animales no se lee como un
zoo: el alumno tiene que ver a donde va antes de leer la historia.

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


BANCO = os.path.join(ROOT, "assets", "vocab")


def pega(im, nombre, cx, suelo, alto):
    """Pone un animal del banco con su sombra de contacto.

    Se escala por la altura y se apoya por los pies, no por el centro: los
    dibujos del banco vienen recortados a su contenido y cada animal tiene
    una proporcion distinta, asi que centrarlos deja unos flotando y otros
    hundidos en la hierba."""
    ruta = os.path.join(BANCO, nombre + ".png")
    if not os.path.exists(ruta):
        return False
    a = Image.open(ruta).convert("RGBA")
    # Los recortes del banco conservan un borde casi blanco que sobre la
    # hierba se ve como un parche. Se quita antes de escalar, cuando el
    # pixel todavia es el original y no una mezcla del remuestreo.
    import numpy as np
    arr = np.array(a)
    casi_blanco = (arr[:, :, :3].min(axis=2) > 228) & (arr[:, :, 3] < 250)
    arr[casi_blanco, 3] = 0
    a = Image.fromarray(arr, "RGBA")
    esc = alto / a.height
    a = a.resize((max(1, int(a.width * esc)), alto), Image.LANCZOS)

    sombra = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse(
        [cx - a.width * .40, suelo - 12, cx + a.width * .40, suelo + 12],
        fill=(42, 62, 40, 90))
    im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(7)))
    im.alpha_composite(a, (int(cx - a.width / 2), suelo - alto))
    return True


def corral(im, d, x0, x1, y0, y1, nombre, animales, alto):
    """Un recinto de primera fila: hierba, animal dentro y valla delante."""
    d.rounded_rectangle([x0, y0, x1, y1], 22, fill=(150, 196, 122),
                        outline=(120, 166, 96), width=3)

    # el cartel arriba: colgado a media altura tapaba al animal, que es
    # justo lo que la escena tiene que dejar ver
    cartel(d, (x0 + x1) // 2, y0 + 12, nombre, ancho=int((x1 - x0) * .88), alto=32)

    suelo = y1 - 46
    n = len(animales)
    for i, (bicho, k) in enumerate(animales):
        cx = x0 + (x1 - x0) * (i + 1) / (n + 1)
        pega(im, bicho, cx, suelo + (0 if n == 1 else 8 * (i % 2)), int(alto * k))

    valla(d, x0 + 6, x1 - 6, y1 - 14, 56)


def recinto(d, x, y, ancho, nombre):
    """Un recinto al fondo: valla curva, seto y su cartelito."""
    d.ellipse([x - ancho // 2, y - 46, x + ancho // 2, y + 26], fill=HOJA_C)
    valla(d, x - ancho // 2, x + ancho // 2, y + 30, 42)
    cartel(d, x, y + 44, nombre, ancho=int(ancho * .78), alto=34)


def zoo():
    im = Image.new("RGBA", (W, H), "white")
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

    # arboles del fondo
    for x, e in ((90, .8), (520, .6), (1200, .6), (1660, .8)):
        arbol(d, x, int(H * .40), e)

    # arco de entrada, mas arriba y mas pequeno que antes: la mitad de
    # abajo hace falta entera para los recintos
    ax0, ax1, ay = int(W * .34), int(W * .66), int(H * .40)
    d.rectangle([ax0, ay - 210, ax0 + 34, ay], fill=MADERA)
    d.rectangle([ax1 - 34, ay - 210, ax1, ay], fill=MADERA)
    d.rectangle([ax0 - 16, ay - 246, ax1 + 16, ay - 202], fill=MADERA_C)
    d.polygon([(ax0 - 30, ay - 246), (W // 2, ay - 310), (ax1 + 30, ay - 246)], fill=TECHO)
    d.text((W // 2, ay - 224), "NORDIC ZOO", font=fuente(44),
           fill=(255, 246, 232), anchor="mm")

    # taquilla, ahora dentro del cuadro y sin que la valla la tape
    tx = ax0 - 180
    d.rounded_rectangle([tx - 74, ay - 124, tx + 74, ay], 12, fill=(238, 226, 200),
                        outline=MADERA, width=5)
    d.polygon([(tx - 94, ay - 124), (tx, ay - 168), (tx + 94, ay - 124)], fill=TECHO)
    d.rounded_rectangle([tx - 48, ay - 96, tx + 48, ay - 52], 8, fill=(176, 214, 232),
                        outline=MADERA, width=4)
    cartel(d, tx, ay - 44, "TICKETS", ancho=124, alto=30)

    valla(d, 0, tx - 96, ay + 4, 46)
    valla(d, ax1 + 10, W, ay + 4, 46)

    # camino corto: solo el trozo que va del arco a los recintos
    d.polygon([(int(W * .40), ay), (int(W * .60), ay),
               (W, H), (0, H)], fill=CAMINO)

    # los recintos, en primera fila y con los animales dentro. Son los que
    # nombra la historia de la unidad: pandas, leones, elefantes, pinguinos
    # y monos, mas el estanque de los delfines.
    CORRALES = [
        ("PANDAS",    [("panda", 1.00)],     1.00),
        ("LIONS",     [("lion", 1.00)],      1.00),
        ("ELEPHANTS", [("elephant", 1.00)],  1.06),
        ("PENGUINS",  [("penguin", 1.00)],    .96),
        ("MONKEYS",   [("monkey", 1.00)],     .96),
        ("KANGAROOS", [("kangaroo", 1.00)],  1.02),
    ]
    y0, y1 = int(H * .41), int(H * .74)
    ancho = (W - 2 * 12 - 5 * 8) // 6
    alto = int((y1 - y0) * .62)
    for i, (nombre, bichos, k) in enumerate(CORRALES):
        x0 = 12 + i * (ancho + 8)
        corral(im, d, x0, x0 + ancho, y0, y1, nombre, bichos, int(alto * k))

    # un poco de profundidad, como en las demas escenas del curso
    im = im.convert("RGB")
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
