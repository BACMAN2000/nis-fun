"""Escenas dibujadas para el video «Where Is Teddy?» (English 2B, Unit 5).

Cada escena es una lista de capas (sprite, x, y, se_mueve). Los sprites se
dibujan una vez al doble de tamaño y se reducen, para que los bordes salgan
suaves; luego cada fotograma solo pega capas, lo que permite que Teddy rebote
sin redibujar nada.
"""
from functools import lru_cache
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FONTS = r"C:\Projects\nis-portal\fonts"
NAVY = (27, 42, 74)
COLORS = {  # un color por preposición, el mismo en el video, la clase y el anchor chart
    "in": (232, 76, 61), "on": (243, 156, 18), "behind": (142, 68, 173),
    "in front of": (39, 174, 96), "next to": (41, 128, 185), "between": (211, 84, 140),
}


def font(size, weight="Bold"):
    name = {"Bold": "GothamBold.ttf", "Book": "GothamBook.ttf",
            "Round": "TTRoundsNeue-Black.ttf"}[weight]
    return ImageFont.truetype(f"{FONTS}\\{name}", size)


def _hi(w, h):
    return Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0))


def _lo(img):
    return img.resize((img.width // 2, img.height // 2), Image.LANCZOS)


@lru_cache(None)
def teddy(scale=1.0):
    """Osito de pie, 260x340 a escala 1. El punto de apoyo es abajo al centro."""
    w, h = int(260 * scale), int(340 * scale)
    im = _hi(w, h)
    d = ImageDraw.Draw(im)
    k = 2 * scale
    B, L, D = (166, 112, 66), (226, 186, 140), (60, 38, 24)
    ol = dict(outline=(110, 70, 38), width=int(5 * k))
    E = lambda x0, y0, x1, y1, fill: d.ellipse([x0 * k, y0 * k, x1 * k, y1 * k], fill=fill, **ol)
    E(40, 250, 115, 335, B); E(145, 250, 220, 335, B)          # piernas
    E(58, 285, 100, 328, L); E(160, 285, 202, 328, L)          # plantas
    E(10, 165, 75, 250, B); E(185, 165, 250, 250, B)           # brazos
    E(45, 145, 215, 305, B)                                     # cuerpo
    E(85, 185, 175, 280, L)                                     # barriga
    E(30, 15, 95, 80, B); E(165, 15, 230, 80, B)               # orejas
    E(45, 30, 80, 65, L); E(180, 30, 215, 65, L)
    E(40, 25, 220, 185, B)                                      # cabeza
    E(92, 100, 168, 165, L)                                     # hocico
    d.ellipse([88 * k, 78 * k, 108 * k, 100 * k], fill=D)      # ojos
    d.ellipse([152 * k, 78 * k, 172 * k, 100 * k], fill=D)
    d.ellipse([93 * k, 81 * k, 99 * k, 87 * k], fill="white")
    d.ellipse([157 * k, 81 * k, 163 * k, 87 * k], fill="white")
    d.ellipse([117 * k, 110 * k, 143 * k, 128 * k], fill=D)    # nariz
    d.arc([110 * k, 118 * k, 150 * k, 150 * k], 20, 160, fill=D, width=int(5 * k))
    d.ellipse([60 * k, 115 * k, 85 * k, 135 * k], fill=(240, 140, 140, 150))
    d.ellipse([175 * k, 115 * k, 200 * k, 135 * k], fill=(240, 140, 140, 150))
    # pajarita roja: el «uniforme» del peluche de la clase
    d.polygon([(130 * k, 160 * k), (100 * k, 145 * k), (100 * k, 178 * k)], fill=(220, 50, 60))
    d.polygon([(130 * k, 160 * k), (160 * k, 145 * k), (160 * k, 178 * k)], fill=(220, 50, 60))
    d.ellipse([122 * k, 152 * k, 138 * k, 168 * k], fill=(180, 30, 40))
    return _lo(im)


BOX_W, BOX_H, LIP = 360, 250, 60


@lru_cache(None)
def box_back():
    """El hueco oscuro de la caja abierta (va detrás de lo que está «in»)."""
    im = _hi(BOX_W, LIP * 2)
    d = ImageDraw.Draw(im)
    d.polygon([(0, LIP * 2), (60, 0), (BOX_W * 2 - 60, 0), (BOX_W * 2, LIP * 2)], fill=(120, 80, 40))
    d.polygon([(30, LIP * 2), (75, 25), (BOX_W * 2 - 75, 25), (BOX_W * 2 - 30, LIP * 2)], fill=(70, 45, 22))
    return _lo(im)


@lru_cache(None)
def box_front():
    im = _hi(BOX_W + 80, BOX_H + 60)
    d = ImageDraw.Draw(im)
    o = 80  # margen para las solapas
    d.rectangle([o, 120, o + BOX_W * 2, 120 + BOX_H * 2], fill=(205, 150, 90), outline=(130, 85, 40), width=10)
    d.rectangle([o + BOX_W - 30, 120, o + BOX_W + 30, 120 + BOX_H * 2], fill=(225, 190, 120))  # cinta
    d.polygon([(o, 120), (0, 30), (o + 60, 0), (o + 120, 120)], fill=(190, 135, 75), outline=(130, 85, 40))
    d.polygon([(o + BOX_W * 2, 120), (o + BOX_W * 2 + 80, 30), (o + BOX_W * 2 + 20, 0),
               (o + BOX_W * 2 - 40, 120)], fill=(190, 135, 75), outline=(130, 85, 40))
    return _lo(im)


@lru_cache(None)
def box_closed():
    """Caja cerrada, para «on»: Teddy necesita una tapa donde sentarse."""
    im = _hi(BOX_W, BOX_H + 40)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 80, BOX_W * 2, 80 + BOX_H * 2], fill=(205, 150, 90), outline=(130, 85, 40), width=10)
    d.polygon([(0, 80), (50, 0), (BOX_W * 2 - 50, 0), (BOX_W * 2, 80)], fill=(225, 175, 110), outline=(130, 85, 40))
    d.rectangle([BOX_W - 30, 0, BOX_W + 30, 80 + BOX_H * 2], fill=(225, 190, 120))
    return _lo(im)


@lru_cache(None)
def basket():
    w, h = 340, 300
    im = _hi(w, h)
    d = ImageDraw.Draw(im)
    d.arc([60, 0, w * 2 - 60, 340], 180, 360, fill=(150, 95, 40), width=26)  # asa
    top, bot = 200, h * 2 - 10
    d.polygon([(0, top), (w * 2, top), (w * 2 - 70, bot), (70, bot)], fill=(214, 160, 80), outline=(140, 90, 35))
    for i in range(1, 6):  # trenzado
        y = top + (bot - top) * i / 6
        inset = 70 * (y - top) / (bot - top)
        d.line([(inset, y), (w * 2 - inset, y)], fill=(160, 105, 45), width=8)
    for i in range(1, 9):
        x0 = w * 2 * i / 9
        d.line([(x0, top), (70 + (w * 2 - 140) * i / 9, bot)], fill=(170, 115, 50), width=6)
    d.rounded_rectangle([-5, top - 25, w * 2 + 5, top + 25], 20, fill=(180, 120, 55))
    return _lo(im)


@lru_cache(None)
def room():
    im = Image.new("RGB", (W, H), (255, 246, 228))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 90):  # papel pintado de rayas suaves
        d.rectangle([x, 0, x + 44, 760], fill=(252, 238, 214))
    d.rectangle([0, 760, W, H], fill=(222, 178, 128))
    for y in (800, 860, 930, 1010):
        d.line([(0, y), (W, y)], fill=(205, 160, 112), width=4)
    d.ellipse([360, 820, 1560, 1060], fill=(120, 170, 210))  # alfombra de la clase
    d.ellipse([400, 838, 1520, 1042], outline=(250, 250, 250), width=6)
    return im


FLOOR = 950  # donde apoyan las cosas


def scene(name):
    """Capas de cada preposición. Devuelve [(sprite, x, y, rebota)]."""
    cx = W // 2
    T = teddy(1.0)
    bx = cx - BOX_W // 2
    by = FLOOR - BOX_H  # borde superior de la caja
    front = (box_front(), bx - 40, by - 60, False)
    if name == "in":
        return [(box_back(), bx, by - LIP, False),
                (T, cx - T.width // 2, by + 150 - T.height, True), front]
    if name == "on":
        return [(box_closed(), bx, FLOOR - BOX_H - 40, False),
                (T, cx - T.width // 2, by - 40 + 20 - T.height + 6, True)]
    if name == "behind":
        t = teddy(0.85)
        return [(t, cx - t.width // 2 + 40, by + 120 - t.height, True),
                (box_closed(), bx, FLOOR - BOX_H - 40, False)]
    if name == "in front of":
        return [(box_closed(), bx, FLOOR - BOX_H - 140, False),
                (teddy(0.95), cx - teddy(0.95).width // 2, FLOOR + 40 - teddy(0.95).height, True)]
    if name == "next to":
        b = basket()
        return [(b, cx + 30, FLOOR - b.height, False),
                (T, cx - 30 - T.width, FLOOR - T.height, True)]
    if name == "between":
        b = basket()
        return [(box_closed(), cx - 230 - BOX_W, FLOOR - BOX_H - 40, False),
                (b, cx + 200, FLOOR - b.height, False),
                (T, cx - T.width // 2, FLOOR - T.height, True)]
    raise KeyError(name)


def compose(layers, t, bob=True, bg=None, scale=1.0):
    im = (bg or room()).copy().convert("RGBA")
    for sp, x, y, moves in layers:
        dy = int(-abs(math.sin(t * math.pi * 100 / 60)) * 14) if (moves and bob) else 0  # 100 BPM
        if scale != 1.0:
            sp = sp.resize((int(sp.width * scale), int(sp.height * scale)), Image.LANCZOS)
        im.alpha_composite(sp, (int(x), int(y) + dy))
    return im


@lru_cache(None)
def mini(name):
    """Viñeta pequeña de cada preposición para el estribillo."""
    full = compose(scene(name), 0, bob=False).convert("RGB")
    crop = full.crop((W // 2 - 620, 330, W // 2 + 620, 1080))
    return crop.resize((520, 315), Image.LANCZOS)


ORDER = ["in", "on", "behind", "in front of", "next to", "between"]


def chorus_board(active=None):
    im = Image.new("RGB", (W, H), (255, 246, 228))
    d = ImageDraw.Draw(im)
    f = font(42)
    tw_, th_ = 470, 285  # deja libre la franja de la letra (y < 270)
    for i, name in enumerate(ORDER):
        col, row = i % 3, i // 3
        x, y = 195 + col * (tw_ + 60), 295 + row * (th_ + 95)
        on = (active == name)
        c = COLORS[name]
        if on:
            d.rounded_rectangle([x - 14, y - 14, x + tw_ + 14, y + th_ + 79], 30, fill=c)
        d.rounded_rectangle([x, y, x + tw_, y + th_ + 65], 22, fill="white")
        im.paste(mini(name).resize((tw_, th_), Image.LANCZOS), (x, y))
        d.rectangle([x, y + th_, x + tw_, y + th_ + 65], fill=c if on else (255, 255, 255))
        tw = d.textlength(name, font=f)
        d.text((x + tw_ / 2 - tw / 2, y + th_ + 10), name, font=f, fill="white" if on else c)
    return im


@lru_cache(None)
def town():
    im = Image.new("RGB", (W, H), (190, 228, 250))
    d = ImageDraw.Draw(im)
    d.ellipse([1500, 60, 1680, 240], fill=(255, 214, 80))
    d.rectangle([0, 720, W, H], fill=(140, 200, 110))
    d.rectangle([0, 850, W, 940], fill=(150, 150, 160))  # calle
    for x in range(40, W, 160):
        d.rectangle([x, 890, x + 80, 900], fill="white")
    f = font(40)
    # PARK (izquierda) — next to — BAKERY
    d.rounded_rectangle([60, 560, 560, 760], 30, fill=(100, 180, 90))
    for tx in (130, 300, 460):
        d.rectangle([tx - 12, 600, tx + 12, 740], fill=(120, 80, 40))
        d.ellipse([tx - 70, 470, tx + 70, 630], fill=(60, 150, 70))
    d.rectangle([220, 700, 380, 715], fill=(150, 90, 40))  # banco
    d.rounded_rectangle([190, 770, 430, 830], 16, fill="white")
    d.text((310 - d.textlength("PARK", font=f) / 2, 778), "PARK", font=f, fill=(39, 120, 60))
    d.rectangle([600, 430, 960, 760], fill=(250, 180, 200))
    d.polygon([(580, 440), (780, 330), (980, 440)], fill=(200, 80, 110))
    d.rectangle([720, 620, 840, 760], fill=(150, 80, 60))
    d.rectangle([630, 500, 700, 580], fill=(255, 255, 230)); d.rectangle([860, 500, 930, 580], fill=(255, 255, 230))
    d.rounded_rectangle([640, 770, 920, 830], 16, fill="white")
    d.text((780 - d.textlength("BAKERY", font=f) / 2, 778), "BAKERY", font=f, fill=(200, 80, 110))
    # SCHOOL con el árbol grande delante
    d.rectangle([1100, 360, 1700, 760], fill=(240, 220, 150))
    d.polygon([(1080, 370), (1400, 230), (1720, 370)], fill=(200, 90, 60))
    for wx in (1150, 1280, 1520, 1600):
        d.rectangle([wx, 430, wx + 70, 510], fill=(170, 210, 240))
    d.rounded_rectangle([1250, 770, 1550, 830], 16, fill="white")
    d.text((1400 - d.textlength("SCHOOL", font=f) / 2, 778), "SCHOOL", font=f, fill=(200, 90, 60))
    d.rectangle([1370, 560, 1430, 770], fill=(110, 70, 35))
    d.ellipse([1220, 330, 1580, 640], fill=(40, 160, 60))
    d.ellipse([1270, 380, 1420, 500], fill=(70, 185, 80))
    return im


def town_frame(t, highlight=None):
    im = town().copy().convert("RGBA")
    if highlight == "me":  # «Teddy is in front of me»: un niño y Teddy delante
        k = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(k)
        x = 1000
        d.ellipse([x - 70, 600, x + 70, 740], fill=(240, 195, 160))      # cabeza
        d.rounded_rectangle([x - 100, 730, x + 100, 1000], 50, fill=(41, 128, 185))
        d.ellipse([x - 40, 650, x - 20, 672], fill=NAVY); d.ellipse([x + 20, 650, x + 40, 672], fill=NAVY)
        d.arc([x - 35, 670, x + 35, 715], 20, 160, fill=NAVY, width=6)
        d.pieslice([x - 75, 580, x + 75, 680], 180, 360, fill=(90, 55, 30))  # pelo
        im.alpha_composite(k)
        t1 = teddy(0.75)
        dy = int(-abs(math.sin(t * math.pi * 100 / 60)) * 14)
        im.alpha_composite(t1, (x - t1.width // 2, 1060 - t1.height + dy))
    return im


def title_card(title, sub):
    im = room().copy().convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([260, 120, 1660, 520], 50, fill=(255, 255, 255, 235))
    f1, f2 = font(120, "Round"), font(48, "Book")
    d.text((W / 2 - d.textlength(title, font=f1) / 2, 190), title, font=f1, fill=NAVY)
    d.text((W / 2 - d.textlength(sub, font=f2) / 2, 380), sub, font=f2, fill=(90, 100, 120))
    t = teddy(1.0)
    im.alpha_composite(t, (W // 2 - t.width // 2, FLOOR - t.height))
    return im


if __name__ == "__main__":  # hoja de contacto para revisar las escenas
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "contacto.png"
    sheet = Image.new("RGB", (W, H * 3 // 2 + 40), "white")
    shots = [compose(scene(n), 0, bob=False).convert("RGB") for n in ORDER]
    shots += [chorus_board("behind"), town_frame(0, "me").convert("RGB"),
              title_card("Where Is Teddy?", "Prepositions of place · English 2B").convert("RGB")]
    for i, s in enumerate(shots):
        sheet.paste(s.resize((W // 3, H // 3)), ((i % 3) * W // 3, (i // 3) * (H // 3 + 10)))
    sheet.save(out)
