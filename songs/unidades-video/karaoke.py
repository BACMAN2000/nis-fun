"""Video karaoke de una canción o chant de unidad (Fun for Nordic).

Uso: python songs/unidades-video/karaoke.py movers 03 chant|cancion

Lee la letra de nis-portal/nis-fun/content/songs-<nivel>.json y el mp3 publicado
(nis-portal/nis-fun/audio/songs/<archivo>), alinea palabra a palabra con
faster-whisper y monta el video con la estética de chants-video/video.py:
escena de fondo, los personajes de la unidad abajo, la letra arriba
iluminándose. Los personajes GESTICULAN las palabras (GESTOS): cambian de pose,
se mueven según el verbo (caminar, galopar, masticar, celebrar…) y aparecen los
objetos (🌭 a la boca, 🎟️, 🐼, 🎡…). Gesticula el personaje nombrado en el verso;
si no hay nombre, o es el coro, todos.
En el chant «Today I go — yesterday I WENT!» la pareja presente → pasado salta
en grande; en la canción, cada pasado que se canta abre su tarjeta go → went.
Sale en songs/unidades-video/out/<nivel>-<unidad>-<tipo>.mp4 y .jpg (portada).
"""
import difflib, json, math, os, re, subprocess, sys, unicodedata
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PORTAL = r"C:\Projects\nis-portal\nis-fun"
FONTS = r"C:\Projects\nis-portal\fonts"
EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"
W, H, FPS = 1280, 720, 24
NAVY = (27, 42, 74)
ACENTO = (230, 80, 90)
GRIS = (175, 182, 198)
INTRO = 2.0  # segundos de título antes de que empiece el audio

# por unidad: escena, elenco (el primero hace de Leader), BPM aproximado por tipo
UNIDAD = {("movers", "03"): {"escena": "funfair", "elenco": ["valentina", "mateo", "sofia", "erik"],
                             "bpm": {"chant": 112, "cancion": 138}}}
COLOR = {"valentina": (230, 120, 160), "mateo": (70, 120, 190), "sofia": (88, 168, 122), "erik": (232, 178, 58)}
NOMBRE = {"sofia": "Sofía"}
# poses de cuerpo entero por intención (las 01-04 son de medio cuerpo: no sirven aquí)
POSE = {"walk": {"*": "pose-07"}, "cheer": {"*": "pose-10"}, "surprise": {"mateo": "pose-05"},
        "hold": {"mateo": "pose-08", "erik": "pose-08"}}
# palabra → gesto: pose, movimiento del cuerpo y objeto con su animación
GESTOS = {
    "go": ("walk", "walk", None, None), "went": ("walk", "walk", None, None),
    "see": ("surprise", "lean", "👀", "eyes"), "saw": ("surprise", "lean", "👀", "eyes"),
    "have": ("hold", "bob", "🎟️", "hold"), "had": ("hold", "bob", "🎟️", "hold"), "ticket": ("hold", "bob", "🎟️", "hold"),
    "ride": ("walk", "gallop", "🎠", "beside"), "rode": ("walk", "gallop", "🎠", "beside"),
    "horses": ("walk", "gallop", "🎠", "beside"),
    "eat": (None, "chew", "🌭", "mouth"), "ate": (None, "chew", "🌭", "mouth"), "hotdog": (None, "chew", "🌭", "mouth"),
    "win": ("cheer", "cheer", "🏆", "above"), "won": ("cheer", "cheer", "🏆", "above"),
    "panda": ("cheer", "cheer", "🐼", "hold"), "carry": ("hold", "strain", "🐼", "hold"),
    "lost": (None, "shake", "🎟️", "away"), "wheel": (None, "lean", "🎡", "spin"), "turn": (None, "lean", "🎡", "spin"),
    "funfair": ("cheer", "cheer", "🎡", "spin"), "learns": (None, "shake", None, None),
    "day": ("cheer", "cheer", None, None), "yesterday": (None, "back", None, None),
}
PASADOS = {"went": "go", "saw": "see", "had": "have", "rode": "ride", "ate": "eat", "won": "win", "lost": "lose"}


def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if not unicodedata.combining(c)))


def font(size, weight="Bold"):
    name = {"Bold": "GothamBold.ttf", "Book": "GothamBook.ttf", "Round": "TTRoundsNeue-Black.ttf"}[weight]
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def lineas(letra):
    """[Leader]/[Kids]/[All] marcan quién canta lo que sigue; [Verse 1], [Chorus]… son secciones."""
    out, who, sec = [], None, None
    for raw in letra.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        m = re.fullmatch(r"\[([^\]]+)\]", raw)
        if m:
            tag = m.group(1).split()[0]
            if tag in ("Leader", "Kids", "All"):
                who = tag
            else:
                sec, who = tag, None
            continue
        words = []
        for w in raw.split():
            if norm(w) or not words:
                words.append(w)
            else:  # «—» y similares van pegados a la palabra anterior
                words[-1] += " " + w
        out.append({"who": who, "sec": sec, "text": raw, "words": words})
    return out


def alinea(mp3, L):
    from faster_whisper import WhisperModel
    model = WhisperModel("medium.en", device="cpu", compute_type="int8")
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    flat = [(li, wi, norm(w)) for li, l in enumerate(L) for wi, w in enumerate(l["words"])]
    best = None
    for prompt in (" ".join(l["text"] for l in L[:8]), None):
        segs, info = model.transcribe(audio, language="en", word_timestamps=True, vad_filter=False, initial_prompt=prompt)
        heard = [(norm(w.word), w.start, w.end) for s in segs for w in s.words if norm(w.word)]
        sm = difflib.SequenceMatcher(None, [f[2] for f in flat], [h[0] for h in heard], autojunk=False)
        times = [None] * len(flat)
        for a, b, n in sm.get_matching_blocks():
            for k in range(n):
                times[a + k] = heard[b + k][1:]
        if best is None or sum(t is not None for t in times) > sum(t is not None for t in best):
            best = times
        if sum(t is not None for t in times) >= 0.85 * len(flat):
            break
    times = best
    hit = sum(t is not None for t in times)
    known = [i for i, t in enumerate(times) if t]
    for i in range(len(times)):  # las que no se oyen se reparten entre las vecinas
        if times[i]:
            continue
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        t0 = times[prev][1] if prev is not None else 0.0
        t1 = times[nxt][0] if nxt is not None else info.duration
        p0 = prev if prev is not None else -1
        p1 = nxt if nxt is not None else len(times)
        span = (t1 - t0) / (p1 - p0)
        times[i] = (t0 + span * (i - p0), t0 + span * (i - p0 + 1))
    for (li, wi, _), t in zip(flat, times):
        L[li].setdefault("t", []).append([round(t[0], 2), round(t[1], 2)])
    print(f"alineadas {hit}/{len(flat)} palabras ({100 * hit / len(flat):.0f} %), {info.duration:.1f} s", flush=True)
    return info.duration, hit, len(flat)


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def sprite(nivel, c, alto, pose="fullbody"):
    f = os.path.join(RAIZ, "assets", "characters", nivel, c, pose + ".png")
    im = Image.open(f).convert("RGBA")
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * alto / im.height), alto), Image.LANCZOS)


_emoji = {}


def emoji(ch, size):
    if ch not in _emoji:
        f = ImageFont.truetype(EMOJI, 109)
        im = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20, 20), ch, font=f, embedded_color=True)
        _emoji[ch] = im.crop(im.getbbox())
    im = _emoji[ch]
    return im.resize((size, round(im.height * size / im.width)), Image.LANCZOS)


def flecha(dr, x, y, w, col):
    head = w * 0.46
    g = max(3, head * 0.22)
    dr.rounded_rectangle([x, y - g, x + w - head * 0.6, y + g], g, fill=col)
    dr.polygon([(x + w - head, y - head * 0.7), (x + w, y), (x + w - head, y + head * 0.7)], fill=col)


def parejas(L):
    """Leader «Today I eat —» + Kids «yesterday I ATE!»: cada pareja se ve desde que el Leader canta el
    verbo hasta que empieza la siguiente; el pasado salta cuando lo cantan los Kids."""
    out = []
    for i in range(1, len(L)):
        a, b = L[i - 1], L[i]
        ma = re.match(r"Today I (\w+)", a["text"])
        mb = re.search(r"yesterday I (\w+)", b["text"], re.I)
        if a["who"] == "Leader" and b["who"] == "Kids" and ma and mb:
            t_pres = next(t0 for w, (t0, _) in zip(a["words"], a["t"]) if norm(w) == ma.group(1).lower())
            t_past = next(t0 for w, (t0, _) in zip(b["words"], b["t"]) if norm(w) == mb.group(1).lower())
            out.append({"pres": ma.group(1), "past": mb.group(1).upper(), "desde": t_pres - 0.15, "past_t": t_past})
    return out


def gestos_de(L, elenco):
    """Por línea: quién gesticula y la lista (t0, gesto). «hot dog» cuenta como una palabra."""
    leader = elenco[0]
    previo, eventos = None, []
    for l in L:
        ws = [norm(w) for w in l["words"]]
        nombrados = [c for c in elenco if c in ws]
        if not nombrados and previo and {"he", "she"} & set(ws):  # «he lost it twice» sigue siendo Mateo
            nombrados = [previo]
        previo = nombrados[0] if nombrados else None
        if l["who"] == "Leader":
            l["actores"], l["solista"] = [leader], leader
        elif l["who"] in ("Kids", "All") or l["sec"] == "Chorus":
            l["actores"], l["solista"] = list(elenco), None
        elif nombrados:
            l["actores"], l["solista"] = nombrados[:1], nombrados[0]
        else:
            l["actores"], l["solista"] = list(elenco), None
        for k, w in enumerate(ws):
            key = "hotdog" if w == "hot" and k + 1 < len(ws) and ws[k + 1] == "dog" else w
            if key in GESTOS:
                eventos.append((l["t"][k][0], l["actores"], GESTOS[key]))
    return eventos


def gesto_en(eventos, t):
    """El último gesto empezado; dura hasta el siguiente, como mucho 2,2 s (aunque cambie la línea)."""
    act = None
    for ev in eventos:
        if ev[0] - 0.1 <= t:
            act = ev
        else:
            break
    return act if act and t < act[0] + 2.2 else None


def render(nivel, unidad, tipo, d, L, dur, out):
    cfg = UNIDAD[(nivel, unidad)]
    elenco, bpm = cfg["elenco"], cfg["bpm"][tipo]
    leader = elenco[0]
    alto = 300
    poses = {}
    for c in elenco:
        poses[c] = {"fullbody": sprite(nivel, c, alto)}
        for intent, m in POSE.items():
            p = m.get(c, m.get("*"))
            if p:
                poses[c][p] = sprite(nivel, c, alto, p)
    xs = [W * (i + 1) / (len(elenco) + 1) for i in range(len(elenco))]
    big = cover(Image.open(os.path.join(RAIZ, "assets", "scenes", cfg["escena"] + ".jpg")).convert("RGB"),
                int(W * 1.12), int(H * 1.12))
    pares = parejas(L)
    eventos = gestos_de(L, elenco)
    # en la canción, cada pasado cantado abre su tarjeta
    tarjetas = [] if pares else [(t0, PASADOS[norm(w)], norm(w)) for l in L for w, (t0, _) in zip(l["words"], l["t"])
                                 if norm(w) in PASADOS]
    titulo = d["titulo"]
    sub = f"Fun for Nordic  ·  {nivel.capitalize()}  ·  Unit {int(unidad)}"
    fn = font(28, "Book")
    ft = font(84, "Round")
    while ft.getlength(titulo) > W - 220:
        ft = font(ft.size - 4, "Round")

    mp3 = os.path.join(PORTAL, "audio", "songs", d["archivo"])
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", mp3, "-af", f"adelay={int(INTRO * 1000)}:all=1",
                           "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)

    def linea_en(t):
        cur = None
        for i, l in enumerate(L):
            if l["t"][0][0] - 0.25 <= t:
                cur = i
        if cur is not None and t > L[cur]["t"][-1][1] + 2.5 and (cur + 1 >= len(L) or t < L[cur + 1]["t"][0][0] - 0.25):
            return cur, False
        return cur, True

    def cuerpo(c, x, t, g, t0, activo, bounce):
        """Dibuja al personaje con su pose y movimiento; devuelve (imagen, x, y, w, h) para colocar objetos."""
        pose_i, mov = (g[0], g[1]) if g else (None, "idle")
        pname = POSE.get(pose_i, {}).get(c, POSE.get(pose_i, {}).get("*")) if pose_i else None
        im = poses[c].get(pname) or poses[c]["fullbody"]
        dt = t - t0 if g else 0
        beat = abs(math.sin(math.pi * t * bpm / 60))
        dx = dy = rot = 0.0
        sx = sy = 1.0
        if mov == "idle":
            dy = beat * (14 if bounce else 6)
            rot = 2.5 * math.sin(2 * math.pi * t * bpm / 120 + x)
        elif mov == "walk":
            dx = 28 * math.sin(2 * math.pi * dt * 1.2)
            dy = abs(math.sin(2 * math.pi * dt * 2.4)) * 14
            rot = 3 * math.sin(2 * math.pi * dt * 2.4)
        elif mov == "gallop":
            dy = abs(math.sin(2 * math.pi * dt * 2.6)) * 34
            rot = 7 * math.sin(2 * math.pi * dt * 2.6)
            dx = 10 * math.sin(2 * math.pi * dt * 1.3)
        elif mov == "lean":
            rot = -10 * min(1, dt / 0.25)
            dy = 4 * beat
        elif mov == "chew":
            sy = 1 - 0.05 * abs(math.sin(2 * math.pi * dt * 4)) if dt > 0.45 else 1
            sx = 1 + 0.03 * abs(math.sin(2 * math.pi * dt * 4)) if dt > 0.45 else 1
            dy = 3 * beat
        elif mov == "cheer":
            dy = abs(math.sin(2 * math.pi * dt * 1.8)) * 40
            sx = sy = 1.04
        elif mov == "shake":
            rot = 8 * math.sin(2 * math.pi * dt * 3) * max(0, 1 - dt / 1.4)
        elif mov == "strain":
            rot = 4 * math.sin(2 * math.pi * dt * 5)
            sy = 0.96
        elif mov == "bob":
            dy = 8 * beat
            rot = 3 * math.sin(2 * math.pi * dt)
        elif mov == "back":  # «yesterday»: mira hacia atrás
            rot = 7 * min(1, dt / 0.3)
            dx = -12 * min(1, dt / 0.3)
        k = 1.12 if activo else 1.0
        w, h = round(im.width * sx * k), round(im.height * sy * k)
        img = im.resize((w, h), Image.BILINEAR) if (w, h) != im.size else im
        if abs(rot) > 0.3:
            img = img.rotate(rot, resample=Image.BICUBIC, expand=True, center=(img.width / 2, img.height))
        px = x + dx - img.width / 2
        py = H - 22 - img.height - dy
        return img, px, py, w, h

    def objeto(frame, ch, anim, t, t0, cx, top, w, h):
        dt = t - t0
        if anim == "mouth":  # de la mano a la boca y bocados
            p = min(1, dt / 0.45)
            sx_, sy_ = cx + w * 0.38, top + h * 0.55
            ex, ey = cx + w * 0.2, top + h * 0.24
            size = 66 if dt < 0.6 else max(30, int(66 - 12 * int((dt - 0.6) / 0.35)))
            x, y = sx_ + (ex - sx_) * p, sy_ + (ey - sy_) * p
        elif anim == "hold":
            size = 90 if ch != "🐼" else 120
            x, y = cx + (w * 0.32 if ch == "🐼" else 0), top + h * 0.56 + 6 * math.sin(dt * 6)
        elif anim == "eyes":
            p = min(1, dt / 0.25)
            size, x, y = int(60 + 40 * p), cx, top + h * 0.05 - 30 * p
        elif anim == "beside":
            size, x, y = 120, cx - w * 0.55, top + h * 0.62 - abs(math.sin(dt * 8)) * 18
        elif anim == "above":
            p = min(1, dt / 0.3)
            size, x, y = int(70 + 30 * p), cx + w * 0.42, top + h * 0.05 - 20 * p
        elif anim == "spin":
            im = emoji(ch, 110).rotate(-dt * 120, resample=Image.BICUBIC, expand=True)
            frame.alpha_composite(im, (int(cx + w * 0.45 - im.width / 2), int(top + h * 0.1 - im.height / 2)))
            return
        elif anim == "away":  # se le escapa
            p = min(1, dt / 1.2)
            size, x, y = 80, cx + w * 0.3 + 160 * p, top + h * 0.45 - 260 * p
            im = emoji(ch, size).rotate(dt * 220, resample=Image.BICUBIC, expand=True)
            im.putalpha(im.getchannel("A").point(lambda a: int(a * (1 - p))))
            frame.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
            return
        else:
            return
        im = emoji(ch, size)
        frame.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

    portada = None
    for f in range(int(dur * FPS) + 1):
        t = f / FPS
        z = 1.12 - 0.10 * (t / dur)
        cw, chh = int(W * z / 1.12 * big.width / W), int(H * z / 1.12 * big.height / H)
        x0 = (big.width - cw) // 2 + int(20 * math.sin(t / 7))
        frame = big.crop((x0, (big.height - chh) // 2, x0 + cw, (big.height - chh) // 2 + chh)).resize((W, H), Image.BILINEAR).convert("RGBA")
        li, cantando = linea_en(t)
        Ln = L[li] if li is not None else None
        g_ev = gesto_en(eventos, t)
        g_act = (g_ev[0], g_ev[2]) if g_ev else None
        actores = g_ev[1] if g_ev else []
        quien = Ln["solista"] if (Ln and cantando) else None
        todos = bool(Ln and cantando and Ln["solista"] is None)

        suelo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ds = ImageDraw.Draw(suelo)
        for c, x in zip(elenco, xs):
            w0 = poses[c]["fullbody"].width
            if c == quien or (todos and c in (Ln["actores"] if Ln else [])):
                ds.ellipse([x - w0 * 0.75, H - 50, x + w0 * 0.75, H + 6], fill=COLOR[c] + (150 if c == quien else 90,))
            ds.ellipse([x - w0 * 0.35, H - 30, x + w0 * 0.35, H - 12], fill=(0, 0, 0, 60))
        frame.alpha_composite(suelo.filter(ImageFilter.GaussianBlur(6)))

        tags = []
        for c, x in zip(elenco, xs):
            g = g_act if (g_act and c in actores) else None
            img, px, py, w, h = cuerpo(c, x, t, g[1] if g else None, g[0] if g else 0, c == quien, todos)
            if g and g[1][3] == "beside":  # el caballito va detrás/al lado
                objeto(frame, g[1][2], g[1][3], t, g[0], x, py, w, h)
            frame.alpha_composite(img, (int(px), int(py)))
            if g and g[1][2] and g[1][3] != "beside":
                objeto(frame, g[1][2], g[1][3], t, g[0], x, py, w, h)
            if c == quien:
                tags.append((c, x, py))

        ui = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(ui)
        for c, x, y in tags:
            nm = NOMBRE.get(c, c.capitalize())
            tw = dr.textlength(nm, font=fn)
            bx, by = x - tw / 2 - 18, H - 58
            dr.rounded_rectangle([bx, by, bx + tw + 36, by + 44], 22, fill=COLOR[c] + (255,))
            dr.text((bx + 18, by + 7), nm, font=fn, fill="white")
        if todos and Ln and (Ln["who"] in ("Kids", "All") or Ln["sec"] == "Chorus"):
            tw = dr.textlength("Everybody!", font=fn)
            dr.rounded_rectangle([W - 60 - tw - 36, H - 70, W - 60, H - 26], 22, fill=NAVY + (230,))
            dr.text((W - 60 - tw - 18, H - 63), "Everybody!", font=fn, fill="white")

        if Ln is not None:
            col_q = COLOR[quien] if quien else ACENTO
            words, size = Ln["words"], 48
            while True:
                f1 = font(size)
                widths = [dr.textlength(w + " ", font=f1) for w in words]
                if sum(widths) < W - 160 or size <= 28:
                    break
                size -= 2
            dr.rounded_rectangle([40, 22, W - 40, 168], 30, fill=(255, 255, 255, 235))
            dr.rounded_rectangle([40, 22, 56, 168], 8, fill=col_q)
            x = W / 2 - sum(widths) / 2
            for k, (w, (t0, t1)) in enumerate(zip(words, Ln["t"])):
                col = (NAVY if t >= t1 + 0.4 else col_q) if t >= t0 else GRIS
                dr.text((x, 52 + (-6 if t0 <= t < t1 else 0)), w, font=f1, fill=col)
                x += widths[k]
            if li + 1 < len(L):
                nx = L[li + 1]["text"]
                tw = dr.textlength(nx, font=fn)
                dr.text((W / 2 - tw / 2, 120), nx, font=fn, fill=(140, 148, 168))

        # chant: pareja presente → pasado; con el coro final, las seis juntas
        fin = L[-1]["t"][-1][1] + 0.5
        coro = next((l for l in L if l["who"] == "All"), None)
        en_coro = bool(pares and coro and coro["t"][0][0] - 0.25 <= t < fin)
        act = None if en_coro else next((pq for pq in reversed(pares) if pq["desde"] <= t), None)
        carta = None
        if act and t < fin:
            carta = (act["pres"], act["past"], act["past_t"], COLOR[leader])
        if tarjetas:  # canción: la última tarjeta abierta, 1,8 s
            tj = next((x for x in reversed(tarjetas) if x[0] <= t < x[0] + 1.8), None)
            if tj:
                carta = (tj[1], tj[2], tj[0], ACENTO)
        if carta:
            pres, past, past_t, cpres = carta
            fp, fa = font(110, "Round"), font(90, "Round")
            wp = dr.textlength(pres, font=fp)
            if t >= past_t:
                p = min(1, (t - past_t) / 0.35)
                s = 0.6 + 0.4 * p + 0.12 * math.sin(p * math.pi)
                fq = font(int(110 * s), "Round")
                wq = dr.textlength(past, font=fq)
                tot = wp + 40 + 90 + 40 + wq
                x = W / 2 - tot / 2
                dr.rounded_rectangle([x - 40, 200, x + tot + 40, 350], 40, fill=(255, 255, 255, 225))
                dr.text((x, 215), pres, font=fp, fill=(140, 148, 168))
                flecha(dr, x + wp + 40, 275, 90, NAVY)
                dr.text((x + wp + 170, 215 + (110 - int(110 * s)) / 2), past, font=fq, fill=ACENTO)
                if portada is None and tarjetas and t > past_t + 0.6:
                    portada = (frame, ui)
            else:
                tot = wp + 40 + 90 + 30 + dr.textlength("?", font=fa)
                x = W / 2 - tot / 2
                dr.rounded_rectangle([x - 40, 200, x + tot + 40, 350], 40, fill=(255, 255, 255, 225))
                dr.text((x, 215), pres, font=fp, fill=cpres)
                flecha(dr, x + wp + 40, 275, 90, GRIS)
                dr.text((x + wp + 160, 222), "?", font=fa, fill=GRIS)
        if en_coro:
            fg = font(46, "Round")
            dr.rounded_rectangle([110, 190, W - 110, 372], 36, fill=(255, 255, 255, 230))
            sung = {norm(w): t0 for w, (t0, _) in zip(coro["words"], coro["t"])}
            for k, pq in enumerate(pares):
                cx, cy = 110 + (W - 220) * (k % 3 + 0.5) / 3, 228 + 82 * (k // 3)
                on = t >= sung.get(pq["past"].lower(), 0)
                a_, b_ = pq["pres"], pq["past"].lower()
                wa_, wb_ = dr.textlength(a_, font=fg), dr.textlength(b_, font=fg)
                x = cx - (wa_ + 70 + wb_) / 2
                dr.text((x, cy), a_, font=fg, fill=(140, 148, 168))
                flecha(dr, x + wa_ + 12, cy + 27, 46, NAVY if on else (200, 205, 215))
                dr.text((x + wa_ + 70, cy), b_, font=fg, fill=ACENTO if on else (200, 205, 215))
            if portada is None and t >= L[-1]["t"][0][0]:
                portada = (frame, ui)

        if t < INTRO + 0.4:
            a = int(255 * min(1, (INTRO + 0.4 - t) / 0.5))
            tw = dr.textlength(titulo, font=ft)
            y = 270 - 30 * max(0, 0.4 - t) / 0.4
            dr.rounded_rectangle([W / 2 - tw / 2 - 50, y - 20, W / 2 + tw / 2 + 50, y + 160], 50, fill=ACENTO + (int(a * 0.95),))
            dr.text((W / 2 - tw / 2, y), titulo, font=ft, fill=(255, 255, 255, a))
            sw = dr.textlength(sub, font=fn)
            dr.text((W / 2 - sw / 2, y + 112), sub, font=fn, fill=(255, 255, 255, a))
        if portada and isinstance(portada, tuple):
            pf, pu = portada
            portada = pf.copy()
            portada.alpha_composite(pu)
        frame.alpha_composite(ui)
        if t > dur - 1.0:
            frame.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * (t - dur + 1.0)))))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    (portada or frame).convert("RGB").save(out[:-4] + ".jpg", quality=86)
    print("->", out, flush=True)


if __name__ == "__main__":
    nivel, unidad, tipo = sys.argv[1], sys.argv[2], sys.argv[3]
    d = json.load(open(os.path.join(PORTAL, "content", f"songs-{nivel}.json"), encoding="utf-8"))["unidades"][unidad][tipo]
    tiempos = os.path.join(AQUI, "tiempos", f"{nivel}-{unidad}-{tipo}.json")
    if os.path.exists(tiempos):
        T = json.load(open(tiempos, encoding="utf-8"))
        L, dur = T["lines"], T["duration"]
        for l, l2 in zip(L, lineas(d["letra"])):  # «sec» no estaba en los tiempos viejos
            l.setdefault("sec", l2["sec"])
            if l["who"] not in (None, "Leader", "Kids", "All"):
                l["who"] = l2["who"]
    else:
        L = lineas(d["letra"])
        dur, hit, total = alinea(os.path.join(PORTAL, "audio", "songs", d["archivo"]), L)
        os.makedirs(os.path.dirname(tiempos), exist_ok=True)
        json.dump({"duration": dur, "hit": hit, "total": total, "lines": L}, open(tiempos, "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)
    for l in L:  # la intro corre el audio
        l["t"] = [[a + INTRO, b + INTRO] for a, b in l["t"]]
    out = os.path.join(AQUI, "out", f"{nivel}-{unidad}-{tipo}.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    render(nivel, unidad, tipo, d, L, dur + INTRO, out)
