# -*- coding: utf-8 -*-
"""Dibuja la familia monstruo de Flyers 24.

La unidad practica "has got" con adjetivos de descripcion, y el chiste es
que cada monstruo tiene un numero distinto de ojos, brazos y dientes: se
describe mejor a alguien raro que a alguien normal.

Estos tres no salen de una IA a proposito. Son formas simples — un color,
unos ojos, unos brazos — y dibujarlos aqui sale mejor que encargarlos:
quedan los tres con el mismo trazo, se pueden repetir sin variaciones y la
biblia puede fijar exactamente cuantos ojos tiene cada uno, que es lo que
el ejercicio necesita.

Salida: assets/characters/flyers/{grum,zog,zip}/pose-01.png y fullbody.png

    python tools/build_monsters.py
"""
import math, os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(ROOT, "assets", "characters", "flyers")

W, H = 520, 720

# Cada uno con lo que dice la biblia: Grum verde con tres ojos y muy
# peludo, Zog morado con un ojo y dos brazos largos, Zip naranja con
# cuatro ojos y redondo.
MONSTRUOS = {
    "grum": {"color": (108, 168, 92), "oscuro": (78, 128, 66), "ojos": 3,
             "brazos": 2, "peludo": True, "alto": 0.92, "ancho": 0.72,
             "dientes": 4, "cuernos": 2},
    "zog":  {"color": (146, 108, 186), "oscuro": (108, 78, 142), "ojos": 1,
             "brazos": 2, "peludo": False, "alto": 0.96, "ancho": 0.58,
             "dientes": 2, "cuernos": 0, "brazos_largos": True},
    "zip":  {"color": (232, 146, 74), "oscuro": (190, 112, 52), "ojos": 4,
             "brazos": 2, "peludo": False, "alto": 0.62, "ancho": 0.78,
             "dientes": 6, "cuernos": 1},
}


def pelo(d, x0, y0, x1, y1, color, n=26):
    """El borde peludo de Grum: puntas cortas alrededor del cuerpo."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    for i in range(n):
        a = 2 * math.pi * i / n
        px, py = cx + rx * math.cos(a), cy + ry * math.sin(a)
        qx, qy = cx + (rx + 16) * math.cos(a), cy + (ry + 16) * math.sin(a)
        d.line([(px, py), (qx, qy)], fill=color, width=9)


def ojo(d, cx, cy, r, mirando=0.0):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=(60, 60, 70), width=3)
    pr = r * 0.42
    d.ellipse([cx - pr + mirando * r * .3, cy - pr, cx + pr + mirando * r * .3, cy + pr],
              fill=(40, 42, 52))
    d.ellipse([cx - pr * .5 + mirando * r * .3, cy - pr * .7,
               cx - pr * .1 + mirando * r * .3, cy - pr * .3], fill=(255, 255, 255))


def monstruo(cfg):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    cw = int(W * cfg["ancho"])
    ch = int(H * cfg["alto"] * 0.62)
    x0 = (W - cw) // 2
    y1 = int(H * 0.90)
    y0 = y1 - ch

    # sombra en el suelo
    d.ellipse([x0 + 10, y1 - 14, x0 + cw - 10, y1 + 18], fill=(30, 40, 55, 60))

    # las piernas, cortas y gordas
    for k in (0.34, 0.66):
        px = x0 + int(cw * k)
        d.rounded_rectangle([px - 26, y1 - 74, px + 26, y1 + 6], 22,
                            fill=cfg["oscuro"])

    if cfg.get("peludo"):
        pelo(d, x0, y0, x0 + cw, y1 - 40, cfg["oscuro"])

    # los brazos
    largo = 1.7 if cfg.get("brazos_largos") else 1.0
    for lado in (-1, 1):
        bx = x0 + (0 if lado < 0 else cw)
        d.line([(bx, y0 + ch * 0.40),
                (bx + lado * int(78 * largo), y0 + ch * (0.34 if largo > 1 else 0.66))],
               fill=cfg["oscuro"], width=34)
        ex = bx + lado * int(78 * largo)
        ey = y0 + ch * (0.34 if largo > 1 else 0.66)
        d.ellipse([ex - 22, ey - 22, ex + 22, ey + 22], fill=cfg["oscuro"])

    # el cuerpo
    d.rounded_rectangle([x0, y0, x0 + cw, y1 - 40], int(cw * 0.42), fill=cfg["color"])

    # los cuernos
    for i in range(cfg.get("cuernos", 0)):
        k = 0.5 if cfg["cuernos"] == 1 else (0.30 + 0.40 * i)
        hx = x0 + int(cw * k)
        d.polygon([(hx - 16, y0 + 12), (hx, y0 - 46), (hx + 16, y0 + 12)],
                  fill=cfg["oscuro"])

    # los ojos, repartidos: es lo que la unidad hace contar
    n = cfg["ojos"]
    r = 42 if n <= 2 else (34 if n == 3 else 28)
    oy = y0 + ch * 0.30
    for i in range(n):
        k = (i + 1) / (n + 1)
        ojo(d, x0 + cw * k, oy + (8 if i % 2 else 0), r, mirando=0.1)

    # la boca y los dientes
    bw, bh = cw * 0.50, ch * 0.16
    bx0, by0 = x0 + (cw - bw) / 2, y0 + ch * 0.56
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], int(bh / 2), fill=(52, 34, 44))
    dn = cfg.get("dientes", 3)
    for i in range(dn):
        k = (i + 0.5) / dn
        tx = bx0 + bw * k
        d.polygon([(tx - 9, by0 + 2), (tx + 9, by0 + 2), (tx, by0 + bh * 0.62)],
                  fill=(250, 250, 245))
    return im


if __name__ == "__main__":
    for slug, cfg in MONSTRUOS.items():
        carpeta = os.path.join(SALIDA, slug)
        os.makedirs(carpeta, exist_ok=True)
        im = monstruo(cfg)
        for nombre in ("pose-01.png", "fullbody.png"):
            im.save(os.path.join(carpeta, nombre), optimize=True)
        print("  %-6s %d ojos · %d dientes · %s"
              % (slug, cfg["ojos"], cfg.get("dientes", 0),
                 "peludo" if cfg.get("peludo") else "liso"))
