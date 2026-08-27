# -*- coding: utf-8 -*-
"""Genera las dos escenas de "encuentra las diferencias" de cada unidad.

Antes eran dos rejillas de emoji con 3-4 diferencias: no daba juego para
hablar. Ahora son dos fotos del mismo sitio del campus con los personajes y
los objetos del vocabulario colocados, y mas de ocho diferencias de tipos
distintos, que es lo que permite construir frases:

  color      "In picture A the ball is red, but in B it is blue."
  cantidad   "In A there are three cars, in B there are two."
  tamano     "The teddy is bigger in B."
  posicion   "The kite is next to the window in B."
  ausencia   "There isn't a doll in picture B."

Salida: assets/spot-diff/{nivel}-{n}-A.jpg, -B.jpg y -diffs.json con las
zonas para poder pulsarlas en pantalla.

    python tools/build_spot_diff.py
"""
import json, os
from PIL import Image, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONDOS = os.path.join(ROOT, "assets", "scenes")
VOCAB = os.path.join(ROOT, "assets", "vocab")
CHARS = os.path.join(ROOT, "assets", "characters")
SALIDA = os.path.join(ROOT, "assets", "spot-diff")

W, H = 900, 620


def slug(w):
    import re
    return re.sub(r"[^a-z0-9]+", "-", w.lower().replace("'", "")).strip("-")


def gira_tono(im, grados):
    """Cambia el color conservando la forma: para el 'de rojo a azul'."""
    rgb = im.convert("RGB")
    import colorsys
    px = rgb.load()
    a = im.getchannel("A")
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s < 0.18:                    # gris y blanco se dejan en paz
                continue
            h = (h + grados / 360.0) % 1.0
            r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
            px[x, y] = (int(r2 * 255), int(g2 * 255), int(b2 * 255))
    out = rgb.convert("RGBA")
    out.putalpha(a)
    return out


# Cada escena: fondo, personajes y objetos con su sitio, y que cambia en B.
# pos = (x, y) centro en tanto por uno; alto en tanto por uno del alto.
ESCENAS = {
    "starters/1": {
        "fondo": "classroom",
        "personajes": [("starters", "freya", .16, .62, .40),
                       ("starters", "nico", .30, .63, .38)],
        "objetos": [
            ("ball",   .46, .74, .17), ("train",  .58, .78, .15),
            ("car",    .68, .79, .13), ("teddy",  .79, .72, .19),
            ("doll",   .90, .72, .18), ("kite",   .52, .26, .17),
            ("red",    .06, .22, .11), ("blue",   .14, .17, .11),
            ("green",  .22, .22, .11), ("yellow", .30, .17, .11),
        ],
        # que se hace en la foto B
        "cambios": [
            ("color", "ball", 150),          # de roja a azulada
            ("quitar", "doll", None),        # ya no esta la muneca
            ("tamano", "teddy", 1.45),       # el oso, mucho mayor
            ("mover", "kite", (.72, .20)),   # la cometa, al otro lado
            ("color", "car", 200),
            ("duplicar", "train", (.44, .90)),   # aparece un segundo tren
            ("espejar", "ball", None),
            ("quitar", "green", None),
            ("color", "yellow", 300),
            ("tamano", "car", 0.65),
            ("mover", "red", (.06, .40)),
        ],
    },
    "movers/1": {
        "fondo": "garden",
        "personajes": [("movers", "erik", .12, .64, .38),
                       ("movers", "valentina", .25, .63, .40)],
        "objetos": [
            ("panda",   .42, .72, .22), ("lion",     .55, .72, .22),
            ("kangaroo", .68, .70, .24), ("penguin", .80, .73, .20),
            ("parrot",  .90, .58, .20), ("snail",    .36, .90, .11),
            ("whale",   .60, .90, .14),
        ],
        "cambios": [
            ("quitar", "penguin", None),
            ("color", "parrot", 140),
            ("tamano", "kangaroo", 1.4),
            ("duplicar", "snail", (.50, .92)),
            ("mover", "whale", (.86, .90)),
            ("color", "lion", 220),
            ("espejar", "panda", None),
            ("tamano", "snail", 1.8),
            ("color", "kangaroo", 300),
            ("quitar", "whale", None),
        ],
    },
    # La familia de Nico en la entrada del colegio
    "starters/2": {
        "fondo": "entrance",
        "personajes": [("starters", "nico", .10, .64, .38)],
        "objetos": [
            ("mother",  .28, .66, .32), ("father",   .40, .65, .34),
            ("sister",  .52, .70, .26), ("brother",  .62, .70, .26),
            ("grandma", .74, .67, .30), ("grandpa",  .87, .66, .32),
            ("baby",    .46, .86, .18),
        ],
        "cambios": [
            ("quitar", "brother", None),
            ("color", "mother", 160),
            ("tamano", "baby", 1.5),
            ("mover", "grandma", (.74, .84)),
            ("espejar", "father", None),
            ("color", "sister", 240),
            ("duplicar", "baby", (.20, .88)),
            ("tamano", "grandpa", 0.72),
            ("color", "grandpa", 120),
            ("quitar", "sister", None),
        ],
    },
    # El sabado del tiempo, visto desde el mirador
    "movers/2": {
        "fondo": "mirador",
        "personajes": [("movers", "sofia", .12, .66, .36),
                       ("movers", "mateo", .24, .67, .34)],
        "objetos": [
            ("sunny",  .44, .22, .20), ("cloudy",  .60, .20, .18),
            ("rainy",  .76, .22, .19), ("rainbow", .90, .30, .20),
            ("windy",  .36, .34, .17), ("umbrella", .44, .74, .22),
            ("hot",    .62, .76, .19), ("cold",     .74, .76, .19),
            ("snowy",  .88, .70, .17),
        ],
        "cambios": [
            ("quitar", "rainy", None),
            ("color", "umbrella", 190),
            ("tamano", "sunny", 1.45),
            ("mover", "rainbow", (.55, .46)),
            ("espejar", "windy", None),
            ("color", "snowy", 280),
            ("duplicar", "cold", (.30, .78)),
            ("quitar", "cloudy", None),
            ("tamano", "hot", 0.65),
            ("color", "rainbow", 60),
        ],
    },
    # El mapa de lugares de Diego, sobre el edificio principal
    "flyers/2": {
        "fondo": "main-building-v2",
        "personajes": [("flyers", "maya", .10, .66, .36),
                       ("flyers", "oliver", .22, .67, .34)],
        "objetos": [
            ("museum",     .38, .70, .22), ("theatre",  .50, .70, .22),
            ("castle",     .62, .68, .24), ("stadium",  .74, .72, .20),
            ("restaurant", .86, .70, .21), ("bridge",   .95, .84, .16),
            ("airport",    .40, .26, .17), ("funfair",  .60, .26, .19),
        ],
        "cambios": [
            ("quitar", "stadium", None),
            ("color", "theatre", 150),
            ("tamano", "castle", 1.4),
            ("mover", "airport", (.80, .22)),
            ("espejar", "museum", None),
            ("color", "restaurant", 220),
            ("duplicar", "bridge", (.30, .88)),
            ("quitar", "funfair", None),
            ("tamano", "museum", 0.7),
            ("color", "castle", 300),
        ],
    },
    "flyers/1": {
        "fondo": "facade",
        "personajes": [("flyers", "ingrid", .12, .62, .40),
                       ("flyers", "diego", .26, .63, .38)],
        "objetos": [
            ("suitcase", .42, .76, .19), ("uniform", .54, .70, .21),
            ("scarf",    .65, .74, .18), ("gloves",  .75, .77, .15),
            ("sunhat",   .85, .74, .16), ("socks",   .94, .77, .14),
            ("umbrella", .50, .28, .19), ("ring",    .36, .92, .09),
            ("belt",     .62, .92, .10),
        ],
        "cambios": [
            ("color", "suitcase", 180),
            ("quitar", "gloves", None),
            ("tamano", "sunhat", 1.5),
            ("mover", "umbrella", (.80, .26)),
            ("color", "scarf", 120),
            ("duplicar", "ring", (.46, .93)),
            ("espejar", "uniform", None),
            ("quitar", "belt", None),
            ("color", "socks", 250),
            ("tamano", "suitcase", 0.7),
        ],
    },
}


def carga(nombre, alto_px, kind="obj", lvl=None):
    if kind == "char":
        for ext in ("png", "svg"):
            p = os.path.join(CHARS, lvl, nombre, "fullbody." + ext)
            if os.path.exists(p) and ext == "png":
                im = Image.open(p).convert("RGBA"); break
        else:
            p = os.path.join(CHARS, lvl, nombre, "pose-01.png")
            if not os.path.exists(p):
                return None
            im = Image.open(p).convert("RGBA")
    else:
        p = os.path.join(VOCAB, slug(nombre) + ".png")
        if not os.path.exists(p):
            return None
        im = Image.open(p).convert("RGBA")
    r = alto_px / im.height
    return im.resize((max(1, int(im.width * r)), alto_px), Image.LANCZOS)


def monta(cfg, cambios_activos):
    f = Image.open(os.path.join(FONDOS, cfg["fondo"] + ".jpg")).convert("RGB")
    e = max(W / f.width, H / f.height)
    f = f.resize((int(f.width * e), int(f.height * e)), Image.LANCZOS)
    x = (f.width - W) // 2; y = (f.height - H) // 2
    base = f.crop((x, y, x + W, y + H))
    base = Image.blend(base, Image.new("RGB", (W, H), "white"), 0.18)

    cam = {c[1]: c for c in cambios_activos} if cambios_activos else {}
    zonas = []

    for lvl, nom, px, py, ps in cfg["personajes"]:
        im = carga(nom, int(H * ps), "char", lvl)
        if im:
            base.paste(im, (int(W * px - im.width / 2), int(H * py - im.height / 2)), im)

    extras = []
    for nom, px, py, ps in cfg["objetos"]:
        ops = [c for c in (cambios_activos or []) if c[1] == nom]
        if any(o[0] == "quitar" for o in ops):
            zonas.append((px, py, ps))
            continue
        alto = int(H * ps)
        for o in ops:
            if o[0] == "tamano":
                alto = int(alto * o[2])
        im = carga(nom, alto)
        if im is None:
            continue
        for o in ops:
            if o[0] == "color":
                im = gira_tono(im, o[2])
            if o[0] == "espejar":
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            if o[0] == "mover":
                px, py = o[2]
            if o[0] == "duplicar":
                extras.append((nom, o[2][0], o[2][1], ps))
        if ops:
            zonas.append((px, py, ps))
        base.paste(im, (int(W * px - im.width / 2), int(H * py - im.height / 2)), im)

    for nom, px, py, ps in extras:
        im = carga(nom, int(H * ps))
        if im:
            base.paste(im, (int(W * px - im.width / 2), int(H * py - im.height / 2)), im)
            zonas.append((px, py, ps))
    return base, zonas


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    for clave, cfg in ESCENAS.items():
        lvl, n = clave.split("/")
        a, _ = monta(cfg, None)
        b, zonas = monta(cfg, cfg["cambios"])
        a.save(os.path.join(SALIDA, "%s-%s-A.jpg" % (lvl, n)), quality=85, optimize=True)
        b.save(os.path.join(SALIDA, "%s-%s-B.jpg" % (lvl, n)), quality=85, optimize=True)
        # zonas unicas, redondeadas: una por diferencia visible
        vistas, limpio = set(), []
        for px, py, ps in zonas:
            k = (round(px, 2), round(py, 2))
            if k in vistas:
                continue
            vistas.add(k)
            limpio.append({"x": round(px, 3), "y": round(py, 3),
                           "r": round(max(0.05, ps * 0.62), 3)})
        json.dump({"zonas": limpio, "total": len(limpio)},
                  open(os.path.join(SALIDA, "%s-%s-diffs.json" % (lvl, n)), "w"),
                  ensure_ascii=False)
        print("  %-12s fondo %-10s %2d diferencias" % (clave, cfg["fondo"], len(limpio)))
