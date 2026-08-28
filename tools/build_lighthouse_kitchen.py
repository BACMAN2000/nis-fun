# -*- coding: utf-8 -*-
"""Dibuja la cocina del faro para Flyers 1.

La historia de la unidad empieza ahi: "It is the first morning of the Aurora
Expedition, and the lighthouse kitchen is full of open suitcases". La lamina
era la fachada del colegio con la ropa flotando en fila, que no tiene nada
que ver con lo que el alumno esta leyendo.

Como el zoo, es de los pocos sitios del curso que no estan en el campus de
Nordic, asi que no hay foto y se dibuja: pared curva de piedra, el ojo de
buey con el mar de fondo, la encimera, la alacena con las tazas y el suelo
de baldosas. El centro se deja despejado - ahi van Ingrid con su lista, Kili
y las maletas abiertas, que los pega tools/build_unit_scenes.py.

Salida: assets/scenes/lighthouse-kitchen.jpg

    python tools/build_lighthouse_kitchen.py
"""
import math, os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(ROOT, "assets", "scenes")

W, H = 1720, 900

PARED = (232, 222, 204)
JUNTA = (200, 188, 168)
SUELO = (196, 176, 152)
SUELO2 = (178, 158, 134)
MADERA = (158, 112, 68)
MADERA_C = (186, 140, 92)
MAR = (108, 158, 186)
MAR_C = (146, 190, 210)
CIELO = (196, 226, 240)
METAL = (198, 204, 210)


def fuente(px):
    for n in ("segoeuib.ttf", "arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(n, px)
        except Exception:
            pass
    return ImageFont.load_default()


def piedra(d, y0, y1):
    """La pared: hiladas de sillares con la junta marcada. Las filas van
    alternadas para que se lea como piedra y no como azulejo."""
    d.rectangle([0, y0, W, y1], fill=PARED)
    alto = 62
    fila = 0
    y = y0
    while y < y1:
        desfase = 0 if fila % 2 == 0 else 92
        x = -desfase
        while x < W:
            d.rectangle([x, y, x + 184, y + alto], outline=JUNTA, width=3)
            x += 186
        y += alto + 2
        fila += 1
    # la pared es curva: se oscurece hacia los lados
    sombra = Image.new("RGBA", (W, y1 - y0), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sombra)
    for x in range(W):
        t = abs(x - W / 2) / (W / 2)
        sd.line([(x, 0), (x, y1 - y0)], fill=(120, 108, 92, int(90 * t ** 2)))
    return sombra


def ojo_de_buey(im, d, cx, cy, r):
    """La ventana redonda con el mar. Es lo que dice que esto es un faro y
    no una cocina cualquiera."""
    d.ellipse([cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16],
              fill=METAL, outline=(158, 166, 174), width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CIELO)

    mar = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
    md = ImageDraw.Draw(mar)
    md.rectangle([0, r, 2 * r, 2 * r], fill=MAR)
    for k in range(6):
        y = r + 14 + k * 22
        md.line([(0, y), (2 * r, y)], fill=MAR_C, width=4)
    circulo = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(circulo).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    from PIL import ImageChops
    im.paste(mar, (cx - r, cy - r), ImageChops.multiply(circulo, mar.split()[3]))

    for a in (45, 135, 225, 315):
        px = cx + (r + 8) * math.cos(math.radians(a))
        py = cy + (r + 8) * math.sin(math.radians(a))
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(170, 178, 186))
    d.line([(cx - r * .5, cy - r * .5), (cx + r * .1, cy - r * .8)],
           fill=(255, 255, 255), width=9)


def alacena(d, x0, y0, x1, y1):
    """Estantes con tazas y platos: la cocina tiene que parecer usada."""
    d.rounded_rectangle([x0, y0, x1, y1], 10, fill=MADERA_C, outline=MADERA, width=6)
    filas = 3
    alto = (y1 - y0) / filas
    for i in range(filas):
        y = y0 + alto * (i + 1)
        d.rectangle([x0 + 6, y - 9, x1 - 6, y], fill=MADERA)
        n = 5
        for k in range(n):
            cx = x0 + (x1 - x0) * (k + .5) / n
            if i == 0:                                   # tazas
                d.rounded_rectangle([cx - 20, y - 52, cx + 16, y - 10], 6,
                                    fill=(240, 236, 226), outline=(206, 198, 184), width=3)
                d.arc([cx + 10, y - 46, cx + 34, y - 20], -90, 90,
                      fill=(206, 198, 184), width=5)
            elif i == 1:                                 # platos de canto
                d.ellipse([cx - 26, y - 56, cx + 26, y - 8],
                          fill=(246, 242, 232), outline=(202, 194, 180), width=3)
            else:                                        # botes
                c = [(214, 152, 96), (176, 196, 148), (206, 176, 196)][k % 3]
                d.rounded_rectangle([cx - 18, y - 58, cx + 18, y - 8], 7, fill=c,
                                    outline=(120, 104, 88), width=3)
                d.rectangle([cx - 22, y - 62, cx + 22, y - 52], fill=(150, 134, 118))


def encimera(d, x0, y0, x1, y1):
    """La encimera con el fregadero y el grifo."""
    d.rounded_rectangle([x0, y0, x1, y1], 8, fill=MADERA_C, outline=MADERA, width=5)
    d.rectangle([x0, y0, x1, y0 + 18], fill=(216, 176, 130))
    n = 3
    for k in range(n):
        a = x0 + (x1 - x0) * k / n + 10
        b = x0 + (x1 - x0) * (k + 1) / n - 10
        d.rounded_rectangle([a, y0 + 34, b, y1 - 14], 8, fill=MADERA,
                            outline=(126, 88, 54), width=4)
        d.ellipse([(a + b) / 2 - 7, y0 + 62, (a + b) / 2 + 7, y0 + 76], fill=METAL)
    fx = x0 + (x1 - x0) * .74
    d.rounded_rectangle([fx - 90, y0 - 4, fx + 90, y0 + 16], 8, fill=(184, 190, 196))
    d.line([(fx, y0 - 4), (fx, y0 - 58)], fill=METAL, width=11)
    d.line([(fx, y0 - 58), (fx + 46, y0 - 58)], fill=METAL, width=11)


def cocina():
    im = Image.new("RGB", (W, H), PARED)
    d = ImageDraw.Draw(im)

    horizonte = int(H * .62)
    sombra_pared = piedra(d, 0, horizonte)

    # suelo de baldosas, en perspectiva hacia el frente. Se pinta aparte y
    # se pega solo de la linea del horizonte para abajo: el punto de fuga
    # queda por encima, y sin recortar las lineas cruzaban toda la pared.
    piso = Image.new("RGB", (W, H - horizonte), SUELO)
    pd = ImageDraw.Draw(piso)
    fuga = (W // 2, int(-H * .30))
    for k in range(-9, 10):
        pd.line([fuga, (W // 2 + k * 190, H - horizonte)], fill=SUELO2, width=3)
    y, paso = 10, 16
    while y < H - horizonte:
        pd.line([(0, y), (W, y)], fill=SUELO2, width=3)
        paso = int(paso * 1.32)
        y += paso
    im.paste(piso, (0, horizonte))

    # rodapie: cierra la pared contra el suelo
    d.rectangle([0, horizonte - 22, W, horizonte + 6], fill=MADERA_C)

    im.paste(sombra_pared, (0, 0), sombra_pared)

    ojo_de_buey(im, d, int(W * .27), int(H * .27), 118)
    alacena(d, int(W * .60), int(H * .10), int(W * .93), int(H * .44))
    encimera(d, int(W * .58), int(H * .46), int(W * .97), horizonte + 4)

    # la mesa donde se preparan las maletas: la unidad las pega encima
    mx0, mx1 = int(W * .08), int(W * .48)
    my = int(H * .655)
    d.rounded_rectangle([mx0, my, mx1, my + 34], 10, fill=MADERA_C,
                        outline=MADERA, width=5)
    for px in (mx0 + 40, mx1 - 40):
        d.rectangle([px - 14, my + 34, px + 14, my + 190], fill=MADERA)

    # la lista de la expedicion, clavada en la pared
    lx, ly = int(W * .47), int(H * .16)
    d.rounded_rectangle([lx - 74, ly, lx + 74, ly + 150], 8, fill=(250, 247, 238),
                        outline=(206, 198, 184), width=4)
    d.rectangle([lx - 74, ly, lx + 74, ly + 26], fill=(196, 132, 88))
    d.text((lx, ly + 13), "AURORA", font=fuente(19), fill=(255, 248, 238), anchor="mm")
    for k in range(5):
        yy = ly + 48 + k * 20
        d.rectangle([lx - 52, yy, lx - 38, yy + 12], outline=(170, 162, 148), width=3)
        d.line([(lx - 28, yy + 6), (lx + 54, yy + 6)], fill=(198, 190, 176), width=5)

    # profundidad, como en las demas escenas del curso
    suave = im.filter(ImageFilter.GaussianBlur(W / 620.0))
    mask = Image.new("L", (W, H))
    px = mask.load()
    for yy in range(H):
        v = int(255 * max(0.0, min(1.0, 1.10 - 1.6 * (yy / H))))
        for xx in range(W):
            px[xx, yy] = v
    return Image.composite(suave, im, mask)


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    p = os.path.join(SALIDA, "lighthouse-kitchen.jpg")
    cocina().save(p, quality=90, optimize=True, progressive=True)
    print("  lighthouse-kitchen.jpg  %d x %d  %d KB"
          % (W, H, os.path.getsize(p) // 1024))
