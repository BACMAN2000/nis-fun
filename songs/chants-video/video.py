"""Monta el video karaoke de un chant de Rhymes & chants.

Uso: python songs/chants-video/video.py [id ...]   (sin ids: todos los que tienen tiempos/<id>.json)

Escena del colegio de fondo (assets/scenes, con un zoom lento), los personajes
del chant en fila abajo bailando al pulso del BPM de su estilo, el que canta la
línea crece y lleva su nombre; con [Kids] botan todos. Arriba la letra se
ilumina palabra a palabra; los números y los «Oops!» saltan en grande.
Sale en songs/chants-video/out/<id>.mp4 (1280x720, 24 fps).
"""
import json, math, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SONGS = os.path.dirname(AQUI)
RAIZ = os.path.dirname(SONGS)
W, H, FPS = 1280, 720, 24
FONTS = r"C:\Projects\nis-portal\fonts"
NAVY = (27, 42, 74)
CHANTS = {c["id"]: c for c in json.load(open(os.path.join(SONGS, "chants-tradicionales.json"), encoding="utf-8"))["chants"]}
SUNO = json.load(open(os.path.join(SONGS, "chants-tradicionales-suno.json"), encoding="utf-8"))["chants"]

# escena por chant (variadas; las NIS cambiaron de tema)
ESCENA = {"eeny-meeny": "classroom", "one-potato": "main-building-v2", "ip-dip": "track", "bubble-gum": "picnic-garden",
          "engine-engine": "entrance", "inky-pinky": "zoo", "tinker-tailor": "library", "fish-alive": "mirador",
          "icka-bicka": "campus-hex", "sky-blue": "garden", "miss-mary-mack": "labyrinth", "sailor-went-to-sea": "amphitheater",
          "pat-a-cake": "lighthouse-kitchen", "double-double": "chess-plaza", "down-down-baby": "funfair",
          "teddy-bear": "track", "cinderella": "zoo", "i-like-coffee": "hockey"}
# color de cada personaje (polo de la biblia; compañeros, uno propio)
COLOR = {"freya": (127, 182, 224), "nico": (224, 92, 75), "astrid": (88, 168, 122), "tomas": (232, 178, 58),
         "pip": (38, 49, 59), "lia": (180, 120, 200), "bruno": (70, 120, 190), "aiko": (230, 120, 160),
         "samu": (90, 170, 170), "iris": (150, 110, 220), "tino": (240, 140, 60)}
NOMBRE = {"tomas": "Tomás", "lia": "Lía"}
ACENTO = [(230, 80, 90), (40, 150, 220), (250, 170, 30), (90, 180, 90), (160, 90, 210), (240, 120, 40)]
NUMEROS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
           "eight": "8", "nine": "9", "ten": "10"}
POP = {"oops": "Oops!", "pop": "POP!", "crunch": "CRUNCH!", "snap": "SNAP!", "wow": "WOW!", "pow": "POW!", "choo": "CHOO CHOO!"}

slug = lambda s: re.sub(r"[^a-z]", "", s.lower().replace("á", "a").replace("í", "i"))
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())


def font(size, weight="Bold"):
    name = {"Bold": "GothamBold.ttf", "Book": "GothamBook.ttf", "Round": "TTRoundsNeue-Black.ttf"}[weight]
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def sprite(c, alto):
    im = Image.open(os.path.join(RAIZ, "assets", "characters", "starters", c, "fullbody.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * alto / im.height), alto), Image.LANCZOS)


def render(cid):
    T = json.load(open(os.path.join(AQUI, "tiempos", cid + ".json"), encoding="utf-8"))
    ch = CHANTS[cid]
    titulo = SUNO[cid]["titulo_suno"]
    bpm = int(re.search(r"(\d+)\s*BPM", ch.get("estilo_v2", ch["estilo"])).group(1))
    acento = ACENTO[list(CHANTS).index(cid) % len(ACENTO)]
    lines = T["lines"]
    dur = T["duration"]

    # quién sale: los del chant + los que cantan alguna línea, en orden de aparición
    elenco = []
    for c in ch["personajes"] + [slug(l["who"]) for l in lines if l["who"] and l["who"] != "Kids"]:
        if c in COLOR and c not in elenco:
            elenco.append(c)
    for l in lines:  # los nombrados en la letra también salen (Not you, Lía!)
        for w in l["words"]:
            s = slug(w)
            if s in COLOR and s not in elenco and len(elenco) < 7:
                elenco.append(s)
    n = len(elenco)
    alto = 300 if n <= 5 else 250
    spr = {c: {k: sprite(c, round(alto * k)) for k in (1.0, 1.18)} for c in elenco}
    if "pip" in spr:  # Pip es un frailecillo: más pequeño
        spr["pip"] = {k: sprite("pip", round(alto * 0.62 * k)) for k in (1.0, 1.18)}
    xs = [W * (i + 1) / (n + 1) for i in range(n)]

    bg0 = Image.open(os.path.join(RAIZ, "assets", "scenes", ESCENA[cid] + ".jpg")).convert("RGB")
    big = cover(bg0, int(W * 1.12), int(H * 1.12))
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(veil).rectangle([0, 0, W, 210], fill=(255, 255, 255, 0))

    fl, fn, ft, fp = font(48), font(28, "Book"), font(84, "Round"), font(150, "Round")
    out = os.path.join(AQUI, "out", cid + ".mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    mp3 = os.path.join(SONGS, "audio", "chants", cid + ".mp3")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", mp3, "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)

    def linea_en(t):
        cur = None
        for i, l in enumerate(lines):
            if l["t"][0][0] - 0.25 <= t:
                cur = i
        if cur is not None and t > lines[cur]["t"][-1][1] + 2.5 and (cur + 1 >= len(lines) or t < lines[cur + 1]["t"][0][0] - 0.25):
            return cur, False  # silencio largo: se ve, pero sin nadie cantando
        return cur, True

    nframes = int(dur * FPS) + 1
    for f in range(nframes):
        t = f / FPS
        z = 1.12 - 0.10 * (t / dur)  # zoom lento hacia fuera
        cw, chh = int(W * z / 1.12 * big.width / W), int(H * z / 1.12 * big.height / H)
        x0 = (big.width - cw) // 2 + int(20 * math.sin(t / 7))
        frame = big.crop((x0, (big.height - chh) // 2, x0 + cw, (big.height - chh) // 2 + chh)).resize((W, H), Image.BILINEAR).convert("RGBA")
        li, cantando = linea_en(t)
        L = lines[li] if li is not None else None
        quien = slug(L["who"]) if (L and L["who"] and cantando) else None
        todos = bool(L and cantando and L["who"] in (None, "Kids"))  # coro: botan todos
        beat = abs(math.sin(math.pi * t * bpm / 60))

        # suelo: sombras y foco de color bajo quien canta (capa aparte: ImageDraw no mezcla sobre RGBA)
        suelo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ds = ImageDraw.Draw(suelo)
        for c, x in zip(elenco, xs):
            w0 = spr[c][1.0].width
            if c == quien:
                ds.ellipse([x - w0 * 0.75, H - 50, x + w0 * 0.75, H + 6], fill=COLOR[c] + (150,))
            ds.ellipse([x - w0 * 0.35, H - 30, x + w0 * 0.35, H - 12], fill=(0, 0, 0, 60))
        frame.alpha_composite(suelo.filter(ImageFilter.GaussianBlur(6)))

        # personajes
        tags = []
        for c, x in zip(elenco, xs):
            activo = (c == quien)
            im = spr[c][1.18 if activo else 1.0]
            salto = beat * (26 if activo or todos else 8)
            y = H - 22 - im.height - salto
            frame.alpha_composite(im, (int(x - im.width / 2), int(y)))
            if activo:
                tags.append((c, x, y))

        ui = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ui)
        for c, x, y in tags:
            nm = NOMBRE.get(c, c.capitalize())
            tw = d.textlength(nm, font=fn)
            bx, by = x - tw / 2 - 18, max(180, y - 52)
            d.rounded_rectangle([bx, by, bx + tw + 36, by + 44], 22, fill=COLOR[c] + (255,))
            d.text((bx + 18, by + 7), nm, font=fn, fill="white")

        # letra
        if L is not None:
            words = L["words"]
            size = 48
            while True:
                f1 = font(size)
                widths = [d.textlength(w + " ", font=f1) for w in words]
                if sum(widths) < W - 160 or size <= 28:
                    break
                size -= 2
            d.rounded_rectangle([40, 22, W - 40, 168], 30, fill=(255, 255, 255, 235))
            d.rounded_rectangle([40, 22, 56, 168], 8, fill=COLOR.get(quien, acento) if quien else acento)
            x = W / 2 - sum(widths) / 2
            for k, (w, (t0, t1)) in enumerate(zip(words, L["t"])):
                col = (COLOR.get(quien) if quien and quien != "pip" else acento) if t >= t0 else (175, 182, 198)
                if t >= t0:
                    col = NAVY if t >= t1 + 0.4 else col
                lift = -6 if t0 <= t < t1 else 0
                d.text((x, 52 + lift), w, font=f1, fill=col)
                x += widths[k]
            if li + 1 < len(lines):
                nx = lines[li + 1]["text"]
                tw = d.textlength(nx, font=fn)
                d.text((W / 2 - tw / 2, 120), nx, font=fn, fill=(140, 148, 168))

            # números y onomatopeyas que saltan
            for w, (t0, t1) in zip(words, L["t"]):
                k = norm(w)
                txt = NUMEROS.get(k) or POP.get(k)
                if txt and t0 <= t < t0 + 0.7:
                    p = (t - t0) / 0.7
                    s = 0.6 + 0.5 * math.sin(min(p, 0.5) * math.pi)
                    fpx = font(int(150 * s), "Round")
                    tw = d.textlength(txt, font=fpx)
                    a = int(255 * (1 - max(0, p - 0.6) / 0.4))
                    cx, cy = W / 2 - tw / 2, 230
                    for ox, oy in ((-5, 0), (5, 0), (0, -5), (0, 5)):
                        d.text((cx + ox, cy + oy), txt, font=fpx, fill=(255, 255, 255, a))
                    d.text((cx, cy), txt, font=fpx, fill=acento + (a,))

        # título al principio
        if t < 3.2:
            a = int(255 * min(1, (3.2 - t) / 0.6))
            tw = d.textlength(titulo, font=ft)
            y = 270 - 30 * max(0, 0.4 - t) / 0.4
            d.rounded_rectangle([W / 2 - tw / 2 - 50, y - 20, W / 2 + tw / 2 + 50, y + 160], 50, fill=acento + (int(a * 0.95),))
            d.text((W / 2 - tw / 2, y), titulo, font=ft, fill=(255, 255, 255, a))
            sub = "Fun for Nordic  ·  Rhymes & Chants"
            sw = d.textlength(sub, font=fn)
            d.text((W / 2 - sw / 2, y + 112), sub, font=fn, fill=(255, 255, 255, a))
        frame.alpha_composite(ui)
        if t > dur - 1.0:
            frame.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * (t - dur + 1.0)))))

        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print(cid, "->", out, flush=True)


if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(f[:-5] for f in os.listdir(os.path.join(AQUI, "tiempos")) if f.endswith(".json"))
    for cid in ids:
        render(cid)
