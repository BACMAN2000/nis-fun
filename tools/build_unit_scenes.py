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
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONDOS = os.path.join(ROOT, "assets", "scenes")
VOCAB = os.path.join(ROOT, "assets", "vocab")
CHARS = os.path.join(ROOT, "assets", "characters")
SALIDA = os.path.join(ROOT, "assets", "unit-scenes")

W, H = 1720, 752          # panoramica; a esta talla aguanta pantalla grande

# Para cada unidad: fondo del campus + que poner encima y donde.
# (x, y) es el centro en tanto por uno; s es el alto en tanto por uno del
# alto de la escena. El nombre dice de que se trata:
#   "ball"              un objeto del banco de dibujos
#   "char:freya:2"      un personaje, en la pose indicada
#   "prop:toybox"       utileria dibujada aqui mismo
# Repetir un nombre pone otra copia: la historia de Starters 1 habla de tres
# cochecitos, asi que en el dibujo hay tres.
ESCENAS = {
    # "What's this? It's my toy box! Look - a red ball, a yellow kite... and
    # Pip is hiding inside!" — Freya senala su caja y esta todo lo que dice:
    # la pelota, la cometa, los TRES cochecitos y Pip asomando.
    "starters/1": ("classroom", [
        ("char:freya:2", .16, .64, .58),
        ("prop:toybox", .46, .78, .40),
        ("char:pip:1", .46, .58, .20),
        ("ball", .70, .82, .22),
        ("kite", .84, .30, .28),
        ("car", .62, .93, .13), ("car", .74, .95, .12), ("car", .86, .93, .13),
        ("teddy", .95, .78, .26), ("doll", .05, .88, .19),
        # los colores, en fila por el suelo: colgados del techo no se
        # entendian como los lapices que hay que nombrar
        ("red", .30, .90, .12), ("blue", .38, .95, .12),
        ("green", .17, .95, .12), ("yellow", .24, .90, .12),
    ]),
    # Nico ensena la foto de su familia a la entrada del colegio
    "starters/2": ("entrance", [
        ("mother", .16, .70, .46), ("father", .30, .69, .48),
        ("sister", .43, .73, .40), ("brother", .55, .73, .40),
        ("grandma", .68, .71, .44), ("grandpa", .81, .70, .46),
        ("baby", .93, .77, .30), ("family", .06, .28, .20),
    ]),
    # El Club del Fiordo llega al zoo. Es la unica escena que no pasa en el
    # campus: la historia es en el zoo y del zoo no hay fotos de Nordic, asi
    # que el sitio se dibuja (tools/build_zoo.py). Los ninos estan en la
    # entrada mirando el plano y decidiendo por donde empezar, y los
    # animales asoman por sus recintos.
    "movers/1": ("zoo", [
        ("char:valentina:2", .28, .68, .48), ("char:erik:1", .42, .70, .46),
        ("char:sofia:1", .58, .69, .46), ("char:mateo:4", .72, .70, .44),
        # el plano va DELANTE: se dibuja de menor a mayor y, asi que con la
        # y mas alta que la de los ninos queda en sus manos y no detras
        ("prop:zoomap", .50, .78, .24),
        ("lion", .09, .50, .22), ("panda", .21, .44, .18),
        ("penguin", .81, .45, .18), ("kangaroo", .93, .49, .22),
        ("parrot", .14, .28, .13), ("whale", .10, .90, .16),
        ("dolphin", .90, .90, .16), ("snail", .35, .94, .10),
    ]),
    # Sabado de lluvia y sol junto al fiordo, visto desde el mirador
    "movers/2": ("mirador", [
        ("rainy", .11, .28, .30), ("windy", .27, .24, .26),
        ("rainbow", .50, .30, .34), ("sunny", .74, .24, .28),
        ("cloudy", .90, .28, .24),
        ("umbrella", .16, .76, .28), ("hot", .84, .74, .26), ("cold", .93, .74, .26),
        ("weather", .40, .76, .26),
    ]),
    # Maletas abiertas antes de la Expedicion Aurora
    "flyers/1": ("facade", [
        ("suitcase", .12, .74, .34), ("uniform", .28, .70, .36),
        ("scarf", .42, .74, .30), ("gloves", .55, .76, .26),
        ("sunhat", .68, .74, .28), ("socks", .80, .76, .26),
        ("umbrella", .92, .70, .32), ("belt", .30, .92, .14), ("ring", .48, .93, .12),
        ("pocket", .64, .92, .14),
    ]),
    # El mapa de lugares de Diego y Maya
    "flyers/2": ("main-building-v2", [
        ("museum", .09, .70, .34), ("theatre", .24, .70, .34),
        ("castle", .39, .68, .36), ("stadium", .55, .72, .30),
        ("restaurant", .70, .70, .32), ("chemist's", .84, .71, .30),
        ("bridge", .95, .78, .24), ("airport", .30, .26, .22),
    ]),

    # Unidades que nombraban cosas dibujables y no tenian escena propia.
    "starters/6":  ("classroom", [
        ("red", .20, .52, .26), ("blue", .40, .44, .26),
        ("green", .60, .52, .26), ("yellow", .80, .44, .26),
    ]),
    "starters/30": ("mirador", [
        ("castle", .50, .62, .48), ("train", .18, .82, .24), ("kite", .82, .28, .26),
    ]),
    "starters/31": ("mirador", [
        ("sunny", .20, .34, .30), ("cloudy", .44, .30, .28),
        ("rainy", .68, .34, .30), ("rainbow", .88, .40, .30),
    ]),
    "movers/3":    ("amphitheater", [
        ("funfair", .50, .62, .50), ("kite", .16, .26, .24), ("teddy", .86, .78, .24),
    ]),
    "movers/25":   ("mirador", [
        ("cold", .28, .60, .34), ("hot", .70, .60, .34),
        ("scarf", .14, .84, .22), ("gloves", .86, .84, .22),
    ]),
    "flyers/6":    ("track", [
        ("cold", .26, .58, .34), ("hot", .72, .58, .34),
        ("uniform", .50, .74, .30),
    ]),
    "flyers/51":   ("entrance", [
        ("family", .50, .60, .46), ("mother", .18, .70, .38), ("father", .82, .70, .40),
    ]),
}


def slug(w):
    import re
    return re.sub(r"[^a-z0-9]+", "-", w.lower().replace("'", "")).strip("-")


def caja_juguetes(alto):
    """La caja de Freya, abierta y de tres cuartos, para que Pip asome.

    No hay dibujo de caja en el banco y encargar uno por una sola escena no
    compensa, asi que se dibuja: carton claro, tapa abierta hacia atras y
    una franja de color para que se vea de lejos."""
    A = alto
    W_ = int(A * 1.5)
    im = Image.new("RGBA", (W_, A), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    carton, sombra_c, borde = (214, 168, 116), (188, 140, 92), (140, 98, 60)

    frente = [(int(W_*.10), int(A*.42)), (int(W_*.70), int(A*.42)),
              (int(W_*.70), int(A*.96)), (int(W_*.10), int(A*.96))]
    lado   = [(int(W_*.70), int(A*.42)), (int(W_*.94), int(A*.30)),
              (int(W_*.94), int(A*.84)), (int(W_*.70), int(A*.96))]
    canto  = [(int(W_*.10), int(A*.42)), (int(W_*.34), int(A*.30)),
              (int(W_*.94), int(A*.30)), (int(W_*.70), int(A*.42))]
    d.polygon(frente, fill=carton, outline=borde)
    d.polygon(lado, fill=sombra_c, outline=borde)
    d.polygon(canto, fill=(232, 196, 152), outline=borde)

    # franja de color, como las cajas de juguetes de verdad
    d.rectangle([int(W_*.10), int(A*.60), int(W_*.70), int(A*.72)], fill=(224, 92, 75))

    # tapa abierta hacia atras
    tapa = [(int(W_*.34), int(A*.30)), (int(W_*.94), int(A*.30)),
            (int(W_*.80), int(A*.02)), (int(W_*.20), int(A*.02))]
    d.polygon(tapa, fill=(232, 196, 152), outline=borde)
    return im


def plano_zoo(alto):
    """El plano que miran los ninos en la entrada del zoo.

    Se dibuja porque no hay ningun dibujo asi en el banco y solo hace falta
    aqui: un papel doblado con los caminos y cuatro chinchetas de color, una
    por recinto."""
    A = alto
    W_ = int(A * 1.32)
    im = Image.new("RGBA", (W_, A), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    papel, linea, borde = (250, 246, 232), (196, 208, 186), (150, 132, 100)

    d.rounded_rectangle([2, 2, W_ - 3, A - 3], int(A * .05), fill=papel,
                        outline=borde, width=max(2, A // 60))
    # el doblez del centro
    d.line([(W_ // 2, 6), (W_ // 2, A - 6)], fill=(232, 226, 208), width=max(2, A // 90))
    # caminos
    d.line([(int(W_ * .16), int(A * .78)), (int(W_ * .50), int(A * .52)),
            (int(W_ * .84), int(A * .74))], fill=linea, width=max(3, A // 34))
    d.line([(int(W_ * .50), int(A * .52)), (int(W_ * .50), int(A * .22))],
           fill=linea, width=max(3, A // 34))
    # una chincheta por recinto
    for x, y, c in ((.20, .70, (224, 92, 75)), (.40, .40, (232, 178, 58)),
                    (.62, .36, (75, 168, 160)), (.80, .66, (138, 111, 181))):
        r = max(3, A // 16)
        d.ellipse([W_ * x - r, A * y - r, W_ * x + r, A * y + r], fill=c,
                  outline=(255, 255, 255), width=max(1, A // 90))
    # una banda arriba, como el titulo del plano
    d.rounded_rectangle([int(W_ * .18), int(A * .07), int(W_ * .82), int(A * .17)],
                        int(A * .03), fill=(206, 88, 74))
    return im


def carga_pieza(nombre, alto):
    """Devuelve la imagen de una pieza, sea objeto, personaje o utileria."""
    if nombre.startswith("prop:"):
        cual = nombre.split(":", 1)[1]
        if cual == "toybox":
            return caja_juguetes(alto)
        if cual == "zoomap":
            return plano_zoo(alto)
        return None
    if nombre.startswith("char:"):
        partes = nombre.split(":")
        quien, pose = partes[1], (partes[2] if len(partes) > 2 else "01")
        for f in ("pose-%s.png" % str(pose).zfill(2), "fullbody.png", "pose-01.png"):
            for lvl in os.listdir(CHARS):
                r = os.path.join(CHARS, lvl, quien, f)
                if os.path.exists(r):
                    im = Image.open(r).convert("RGBA")
                    e = alto / im.height
                    return im.resize((max(1, int(im.width * e)), alto), Image.LANCZOS)
        return None
    r = os.path.join(VOCAB, slug(nombre) + ".png")
    if not os.path.exists(r):
        return None
    im = Image.open(r).convert("RGBA")
    im.thumbnail((W, alto), Image.LANCZOS)
    return im


def profundidad(base):
    """Deja el fondo ligeramente fuera de foco, como en los videos.

    El fondo es un dibujo de lineas planas y las figuras son 3D con
    volumen: juntos se veian pegados con cola. Desenfocar un poco el fondo
    los separa en dos planos y el ojo lo lee como una foto con el sujeto
    enfocado, que es el lenguaje de los renders del curso. El desenfoque
    crece hacia arriba, que es lo que esta mas lejos."""
    suave = base.filter(ImageFilter.GaussianBlur(W / 520.0))
    mascara = Image.new("L", (W, H))
    px = mascara.load()
    for y in range(H):
        # arriba (lejos) todo desenfocado, abajo (el suelo) casi nitido
        v = int(255 * max(0.0, min(1.0, 1.05 - 1.35 * (y / H))))
        for x in range(W):
            px[x, y] = v
    return Image.composite(suave, base, mascara)


def gradacion(im):
    """Un mismo bano de luz para el fondo y las figuras, que es lo que de
    verdad hace que parezcan la misma imagen."""
    from PIL import ImageEnhance
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    # luz calida por arriba, como la del faro de los videos
    luz = Image.new("RGB", (W, H), (255, 236, 200))
    velo = Image.new("L", (W, H))
    px = velo.load()
    for y in range(H):
        v = int(38 * max(0.0, 1.0 - y / (H * 0.8)))
        for x in range(W):
            px[x, y] = v
    im = Image.composite(Image.blend(im, luz, 0.5), im, velo)
    # vinetado muy suave para cerrar la composicion
    borde = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(borde)
    d.ellipse([-W * .12, -H * .28, W * 1.12, H * 1.28], fill=255)
    borde = borde.filter(ImageFilter.GaussianBlur(W / 22.0))
    oscuro = ImageEnhance.Brightness(im).enhance(0.88)
    return Image.composite(im, oscuro, borde)


def componer(fondo, piezas):
    f = Image.open(os.path.join(FONDOS, fondo + ".jpg")).convert("RGB")
    escala = max(W / f.width, H / f.height)
    f = f.resize((int(f.width * escala), int(f.height * escala)), Image.LANCZOS)
    x = (f.width - W) // 2; y = (f.height - H) // 2
    base = f.crop((x, y, x + W, y + H))

    base = profundidad(base)
    # un velo claro, mucho mas leve que antes: el fondo ya no compite
    # gracias al desenfoque, y aclararlo tanto lo dejaba lavado
    velo = Image.new("RGB", (W, H), "white")
    base = Image.blend(base, velo, 0.10)

    # de fondo a primer plano, para que lo de delante tape a lo de atras
    for nombre, px, py, ps in sorted(piezas, key=lambda q: q[2]):
        ob = carga_pieza(nombre, int(H * ps))
        if ob is None:
            print("    falta", nombre); continue
        cx, cy = int(W * px), int(H * py)
        ox, oy = cx - ob.width // 2, cy - ob.height // 2
        # sombra suave para asentar el objeto sobre la foto
        # dos sombras: una ancha y difusa que asienta la figura en el
        # espacio, y otra pequena y oscura pegada al pie, que es la que
        # hace que no parezca recortada y pegada encima
        ancha = Image.new("RGBA", (int(ob.width * 1.25), max(10, ob.height // 4)), (0, 0, 0, 0))
        ImageDraw.Draw(ancha).ellipse([0, 0, ancha.width - 1, ancha.height - 1],
                                      fill=(26, 36, 52, 46))
        ancha = ancha.filter(ImageFilter.GaussianBlur(ancha.height / 2.4))
        base.paste(ancha, (ox - (ancha.width - ob.width) // 2,
                           oy + ob.height - ancha.height // 2), ancha)

        contacto = Image.new("RGBA", (int(ob.width * .72), max(6, ob.height // 12)), (0, 0, 0, 0))
        ImageDraw.Draw(contacto).ellipse([0, 0, contacto.width - 1, contacto.height - 1],
                                         fill=(20, 28, 42, 108))
        contacto = contacto.filter(ImageFilter.GaussianBlur(max(2, contacto.height / 3.0)))
        base.paste(contacto, (ox + (ob.width - contacto.width) // 2,
                              oy + ob.height - contacto.height // 2), contacto)
        base.paste(ob, (ox, oy), ob)

    return gradacion(base)


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    for clave, (fondo, piezas) in ESCENAS.items():
        lvl, n = clave.split("/")
        im = componer(fondo, piezas)
        p = os.path.join(SALIDA, "%s-%s.jpg" % (lvl, n))
        im.save(p, quality=90, optimize=True, progressive=True)
        print("  %-14s fondo %-18s %2d objetos  %3d KB"
              % (clave, fondo, len(piezas), os.path.getsize(p) // 1024))
