# -*- coding: utf-8 -*-
"""Compone la escena de apertura de cada unidad de la demo.

Fondo: una foto real del campus de NIS (assets/scenes), la que mejor encaja
con la historia. Encima, los objetos 3D del vocabulario de esa misma unidad
(assets/vocab), para que el alumno reconozca en la ilustracion las palabras
que va a aprender.

Sustituye a las escenas dibujadas en SVG: aquellas no pegaban con el 3D de
los personajes y no usaban el campus, que es lo que da identidad al curso.

    python tools/build_unit_scenes.py
"""
import os
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONDOS = os.path.join(ROOT, "assets", "scenes")
VOCAB = os.path.join(ROOT, "assets", "vocab")
SALIDA = os.path.join(ROOT, "assets", "unit-scenes")

W, H = 1280, 560          # panoramica: cabe bien a ancho completo

# Para cada unidad: fondo del campus + que objetos poner y donde.
# (x, y) es el centro en tanto por uno; s es el alto del objeto en tanto por
# uno del alto de la escena.
ESCENAS = {
    # La caja de juguetes de Freya se vuelca en el aula
    "starters/1": ("classroom", [
        ("ball", .13, .74, .30), ("train", .29, .78, .26), ("car", .44, .80, .22),
        ("teddy", .60, .74, .32), ("doll", .74, .74, .30), ("kite", .88, .34, .30),
        ("red", .05, .40, .16), ("blue", .14, .32, .16),
        ("green", .23, .40, .16), ("yellow", .32, .32, .16),
    ]),
    # Nico ensena la foto de su familia a la entrada del colegio
    "starters/2": ("entrance", [
        ("mother", .16, .70, .46), ("father", .30, .69, .48),
        ("sister", .43, .73, .40), ("brother", .55, .73, .40),
        ("grandma", .68, .71, .44), ("grandpa", .81, .70, .46),
        ("baby", .93, .77, .30),
    ]),
    # El Club del Fiordo visita el zoo: los animales, en el huerto del campus
    "movers/1": ("garden", [
        ("panda", .10, .72, .34), ("lion", .26, .72, .34),
        ("kangaroo", .42, .70, .38), ("penguin", .57, .72, .32),
        ("parrot", .71, .68, .34), ("whale", .87, .76, .28),
        ("snail", .05, .90, .16),
    ]),
    # Sabado de lluvia y sol junto al fiordo, visto desde el mirador
    "movers/2": ("mirador", [
        ("rainy", .11, .28, .30), ("windy", .27, .24, .26),
        ("rainbow", .50, .30, .34), ("sunny", .74, .24, .28),
        ("cloudy", .90, .28, .24),
        ("umbrella", .16, .76, .28), ("hot", .84, .74, .26), ("cold", .93, .74, .26),
    ]),
    # Maletas abiertas antes de la Expedicion Aurora
    "flyers/1": ("facade", [
        ("suitcase", .12, .74, .34), ("uniform", .28, .70, .36),
        ("scarf", .42, .74, .30), ("gloves", .55, .76, .26),
        ("sunhat", .68, .74, .28), ("socks", .80, .76, .26),
        ("umbrella", .92, .70, .32), ("belt", .30, .92, .14), ("ring", .48, .93, .12),
    ]),
    # El mapa de lugares de Diego y Maya
    "flyers/2": ("main-building-v2", [
        ("museum", .09, .70, .34), ("theatre", .24, .70, .34),
        ("castle", .39, .68, .36), ("stadium", .55, .72, .30),
        ("restaurant", .70, .70, .32), ("chemist's", .84, .71, .30),
        ("bridge", .95, .78, .24), ("airport", .30, .26, .22),
    ]),
}


def slug(w):
    import re
    return re.sub(r"[^a-z0-9]+", "-", w.lower().replace("'", "")).strip("-")


def componer(fondo, piezas):
    f = Image.open(os.path.join(FONDOS, fondo + ".jpg")).convert("RGB")
    # recorte central a 1280x560 conservando proporcion
    escala = max(W / f.width, H / f.height)
    f = f.resize((int(f.width * escala), int(f.height * escala)), Image.LANCZOS)
    x = (f.width - W) // 2; y = (f.height - H) // 2
    base = f.crop((x, y, x + W, y + H))

    # un velo claro: el campus queda de fondo y los objetos leen por delante
    velo = Image.new("RGB", (W, H), "white")
    base = Image.blend(base, velo, 0.22)

    for nombre, px, py, ps in piezas:
        p = os.path.join(VOCAB, slug(nombre) + ".png")
        if not os.path.exists(p):
            print("    falta", nombre); continue
        ob = Image.open(p).convert("RGBA")
        alto = int(H * ps)
        ob.thumbnail((int(W), alto), Image.LANCZOS)
        cx, cy = int(W * px), int(H * py)
        ox, oy = cx - ob.width // 2, cy - ob.height // 2
        # sombra suave para asentar el objeto sobre la foto
        sombra = Image.new("RGBA", (ob.width, max(8, ob.height // 6)), (0, 0, 0, 0))
        from PIL import ImageDraw
        ImageDraw.Draw(sombra).ellipse(
            [ob.width * .12, 0, ob.width * .88, sombra.height], fill=(30, 40, 55, 70))
        sombra = sombra.filter(ImageFilter.GaussianBlur(6))
        base.paste(sombra, (ox, oy + ob.height - sombra.height // 2), sombra)
        base.paste(ob, (ox, oy), ob)
    return base


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    for clave, (fondo, piezas) in ESCENAS.items():
        lvl, n = clave.split("/")
        im = componer(fondo, piezas)
        p = os.path.join(SALIDA, "%s-%s.jpg" % (lvl, n))
        im.save(p, quality=86, optimize=True)
        print("  %-14s fondo %-18s %2d objetos  %3d KB"
              % (clave, fondo, len(piezas), os.path.getsize(p) // 1024))
