# -*- coding: utf-8 -*-
"""Compone la foto que acompana a una lectura, cuando el texto habla de ella.

En Starters 2 la actividad F dice "Read about the photo" y describe a la
familia de Nico — pero no habia foto que mirar, asi que el ejercicio pedia
imaginarsela. Aqui se monta esa foto con las figuras 3D de la familia sobre
un sitio del campus y con marco, para que el alumno lea Y mire.

Salida: assets/reading-photos/{nivel}-{n}-{codigo}.jpg

    python tools/build_reading_photos.py
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONDOS = os.path.join(ROOT, "assets", "scenes")
VOCAB = os.path.join(ROOT, "assets", "vocab")
SALIDA = os.path.join(ROOT, "assets", "reading-photos")

W, H = 900, 560
MARCO = 26          # grosor del marco blanco tipo foto revelada


# Quien sale y donde, siguiendo lo que dice cada lectura.
FOTOS = {
    # "My mother is Rosa and my father is Juan. My little sister is five
    #  years old. The baby is my cousin — he is one!"
    "starters/2/F": {
        "fondo": "entrance",
        "pie": "My family",
        "figuras": [
            ("mother", .22, .60, .62),      # Rosa
            ("father", .40, .58, .66),      # Juan
            ("sister", .58, .66, .50),      # la hermana pequena, cinco anos
            ("baby",   .74, .74, .36),      # el primo bebe, un ano
            ("grandma", .88, .62, .56),
        ],
    },
}


def slug(w):
    import re
    return re.sub(r"[^a-z0-9]+", "-", w.lower().replace("'", "")).strip("-")


def compone(cfg):
    f = Image.open(os.path.join(FONDOS, cfg["fondo"] + ".jpg")).convert("RGB")
    iw, ih = W - MARCO * 2, H - MARCO * 2 - 34      # hueco para el pie
    e = max(iw / f.width, ih / f.height)
    f = f.resize((int(f.width * e), int(f.height * e)), Image.LANCZOS)
    x = (f.width - iw) // 2; y = (f.height - ih) // 2
    foto = f.crop((x, y, x + iw, y + ih))
    foto = Image.blend(foto, Image.new("RGB", (iw, ih), "white"), 0.14)

    for nombre, px, py, ps in cfg["figuras"]:
        p = os.path.join(VOCAB, slug(nombre) + ".png")
        if not os.path.exists(p):
            print("    falta", nombre); continue
        im = Image.open(p).convert("RGBA")
        alto = int(ih * ps)
        im.thumbnail((iw, alto), Image.LANCZOS)
        ox, oy = int(iw * px - im.width / 2), int(ih * py - im.height / 2)
        # sombra corta para que no floten sobre el suelo
        sombra = Image.new("RGBA", (im.width, max(6, im.height // 8)), (0, 0, 0, 0))
        ImageDraw.Draw(sombra).ellipse([im.width * .15, 0, im.width * .85, sombra.height],
                                       fill=(30, 40, 55, 65))
        foto.paste(sombra, (ox, oy + im.height - sombra.height // 2), sombra)
        foto.paste(im, (ox, oy), im)

    # marco blanco con el pie escrito a mano, como una foto de album
    lienzo = Image.new("RGB", (W, H), "#f7f4ee")
    lienzo.paste(foto, (MARCO, MARCO))
    d = ImageDraw.Draw(lienzo)
    d.rectangle([MARCO - 1, MARCO - 1, MARCO + iw, MARCO + ih], outline="#d7cfc2", width=2)
    pie = cfg.get("pie")
    if pie:
        try:
            from PIL import ImageFont
            fnt = ImageFont.truetype("segoeui.ttf", 26)
        except Exception:
            fnt = None
        d.text((W // 2, H - 24), pie, fill="#6b6257", anchor="mm", font=fnt)
    return lienzo


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    for clave, cfg in FOTOS.items():
        lvl, n, code = clave.split("/")
        im = compone(cfg)
        p = os.path.join(SALIDA, "%s-%s-%s.jpg" % (lvl, n, code))
        im.save(p, quality=88, optimize=True)
        print("  %-16s %d figuras  %3d KB" % (clave, len(cfg["figuras"]),
                                              os.path.getsize(p) // 1024))
