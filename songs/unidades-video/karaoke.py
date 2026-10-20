"""Video karaoke de una canción o chant de unidad (Fun for Nordic).

Uso: python songs/unidades-video/karaoke.py movers 03 chant

Lee la letra de nis-portal/nis-fun/content/songs-<nivel>.json y el mp3 publicado
(nis-portal/nis-fun/audio/songs/<archivo>), alinea palabra a palabra con
faster-whisper y monta el video con la misma estética que chants-video/video.py:
escena de fondo, los personajes de la unidad bailando abajo, la letra arriba
iluminándose. Para los chants de verbos «Today I go — yesterday I WENT!» la
pareja presente → pasado salta en grande en el centro.
Sale en songs/unidades-video/out/<nivel>-<unidad>-<tipo>.mp4 y .jpg (portada).
"""
import difflib, json, math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PORTAL = r"C:\Projects\nis-portal\nis-fun"
FONTS = r"C:\Projects\nis-portal\fonts"
W, H, FPS = 1280, 720, 24
NAVY = (27, 42, 74)
ACENTO = (230, 80, 90)
INTRO = 2.0  # segundos de título antes de que empiece el audio

# por unidad: escena, elenco (el primero hace de Leader) y BPM aproximado
UNIDAD = {("movers", "03"): {"escena": "funfair", "elenco": ["valentina", "mateo", "sofia", "erik"], "bpm": 112}}
COLOR = {"valentina": (230, 120, 160), "mateo": (70, 120, 190), "sofia": (88, 168, 122), "erik": (232, 178, 58)}
NOMBRE = {"sofia": "Sofía"}

norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())


def font(size, weight="Bold"):
    name = {"Bold": "GothamBold.ttf", "Book": "GothamBook.ttf", "Round": "TTRoundsNeue-Black.ttf"}[weight]
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def lineas(letra):
    """[Leader]/[Kids]/[All] solos en su línea marcan quién canta lo que sigue; el resto son secciones."""
    out, who = [], None
    for raw in letra.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        m = re.fullmatch(r"\[([^\]]+)\]", raw)
        if m:
            who = m.group(1).split()[0]
            continue
        words = []
        for w in raw.split():
            if norm(w) or not words:
                words.append(w)
            else:  # «—» y similares van pegados a la palabra anterior
                words[-1] += " " + w
        out.append({"who": who, "text": raw, "words": words})
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


def sprite(nivel, c, alto):
    im = Image.open(os.path.join(RAIZ, "assets", "characters", nivel, c, "fullbody.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * alto / im.height), alto), Image.LANCZOS)


def flecha(dr, x, y, w, col):
    head = w * 0.46
    g = max(3, head * 0.22)
    dr.rounded_rectangle([x, y - g, x + w - head * 0.6, y + g], g, fill=col)
    dr.polygon([(x + w - head, y - head * 0.7), (x + w, y), (x + w - head, y + head * 0.7)], fill=col)


def parejas(L):
    """Leader «Today I eat —» + Kids «yesterday I ATE!»: cada pareja se ve desde poco antes de que el
    Leader cante el verbo hasta que empieza la siguiente; el pasado salta cuando lo cantan los Kids."""
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


def render(nivel, unidad, tipo, d, L, dur, out):
    cfg = UNIDAD[(nivel, unidad)]
    elenco, bpm = cfg["elenco"], cfg["bpm"]
    leader = elenco[0]
    alto = 300
    spr = {c: {k: sprite(nivel, c, round(alto * k)) for k in (1.0, 1.18)} for c in elenco}
    xs = [W * (i + 1) / (len(elenco) + 1) for i in range(len(elenco))]
    big = cover(Image.open(os.path.join(RAIZ, "assets", "scenes", cfg["escena"] + ".jpg")).convert("RGB"),
                int(W * 1.12), int(H * 1.12))
    pares = parejas(L)
    titulo = d["titulo"]
    sub = f"Fun for Nordic  ·  {nivel.capitalize()}  ·  Unit {int(unidad)}"
    fn, ft = font(28, "Book"), font(84, "Round")

    mp3 = os.path.join(PORTAL, "audio", "songs", d["archivo"])
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", mp3, "-af", f"adelay={int(INTRO * 1000)}:all=1", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)

    def linea_en(t):
        cur = None
        for i, l in enumerate(L):
            if l["t"][0][0] - 0.25 <= t:
                cur = i
        if cur is not None and t > L[cur]["t"][-1][1] + 2.5 and (cur + 1 >= len(L) or t < L[cur + 1]["t"][0][0] - 0.25):
            return cur, False
        return cur, True

    portada = None
    for f in range(int(dur * FPS) + 1):
        t = f / FPS
        z = 1.12 - 0.10 * (t / dur)
        cw, chh = int(W * z / 1.12 * big.width / W), int(H * z / 1.12 * big.height / H)
        x0 = (big.width - cw) // 2 + int(20 * math.sin(t / 7))
        frame = big.crop((x0, (big.height - chh) // 2, x0 + cw, (big.height - chh) // 2 + chh)).resize((W, H), Image.BILINEAR).convert("RGBA")
        li, cantando = linea_en(t)
        Ln = L[li] if li is not None else None
        who = Ln["who"] if (Ln and cantando) else None
        quien = leader if who == "Leader" else None
        todos = who in ("Kids", "All")
        beat = abs(math.sin(math.pi * t * bpm / 60))

        suelo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ds = ImageDraw.Draw(suelo)
        for c, x in zip(elenco, xs):
            w0 = spr[c][1.0].width
            if c == quien or todos:
                ds.ellipse([x - w0 * 0.75, H - 50, x + w0 * 0.75, H + 6], fill=COLOR[c] + (150 if c == quien else 90,))
            ds.ellipse([x - w0 * 0.35, H - 30, x + w0 * 0.35, H - 12], fill=(0, 0, 0, 60))
        frame.alpha_composite(suelo.filter(ImageFilter.GaussianBlur(6)))

        tags = []
        for c, x in zip(elenco, xs):
            activo = c == quien
            im = spr[c][1.18 if activo else 1.0]
            y = H - 22 - im.height - beat * (26 if activo or todos else 8)
            frame.alpha_composite(im, (int(x - im.width / 2), int(y)))
            if activo:
                tags.append((c, x, y))

        ui = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(ui)
        for c, x, y in tags:
            nm = NOMBRE.get(c, c.capitalize())
            tw = dr.textlength(nm, font=fn)
            bx, by = x - tw / 2 - 18, max(180, y - 52)
            dr.rounded_rectangle([bx, by, bx + tw + 36, by + 44], 22, fill=COLOR[c] + (255,))
            dr.text((bx + 18, by + 7), nm, font=fn, fill="white")
        if todos:
            tw = dr.textlength("Everybody!", font=fn)
            dr.rounded_rectangle([W / 2 - tw / 2 - 18, 380, W / 2 + tw / 2 + 18, 424], 22, fill=NAVY + (230,))
            dr.text((W / 2 - tw / 2, 387), "Everybody!", font=fn, fill="white")

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
                col = (NAVY if t >= t1 + 0.4 else col_q) if t >= t0 else (175, 182, 198)
                dr.text((x, 52 + (-6 if t0 <= t < t1 else 0)), w, font=f1, fill=col)
                x += widths[k]
            if li + 1 < len(L):
                nx = L[li + 1]["text"]
                tw = dr.textlength(nx, font=fn)
                dr.text((W / 2 - tw / 2, 120), nx, font=fn, fill=(140, 148, 168))

        # pareja presente → pasado en grande; con el coro final, las seis juntas
        fin = L[-1]["t"][-1][1] + 0.5
        coro = next((l for l in L if l["who"] == "All"), None)
        en_coro = bool(pares and coro and coro["t"][0][0] - 0.25 <= t < fin)
        act = None if en_coro else next((pq for pq in reversed(pares) if pq["desde"] <= t), None)
        if act and t < fin:
            fp, fa = font(110, "Round"), font(90, "Round")
            pres, past = act["pres"], act["past"]
            wp = dr.textlength(pres, font=fp)
            if t >= act["past_t"]:
                p = min(1, (t - act["past_t"]) / 0.35)
                s = 0.6 + 0.4 * p + 0.12 * math.sin(p * math.pi)
                fq = font(int(110 * s), "Round")
                wq = dr.textlength(past, font=fq)
                tot = wp + 40 + 90 + 40 + wq
                x = W / 2 - tot / 2
                dr.rounded_rectangle([x - 40, 210, x + tot + 40, 360], 40, fill=(255, 255, 255, 225))
                dr.text((x, 225), pres, font=fp, fill=(140, 148, 168))
                flecha(dr, x + wp + 40, 285, 90, NAVY)
                dr.text((x + wp + 170, 225 + (110 - int(110 * s)) / 2), past, font=fq, fill=ACENTO)
            else:
                tot = wp + 40 + 90 + 30 + dr.textlength("?", font=fa)
                x = W / 2 - tot / 2
                dr.rounded_rectangle([x - 40, 210, x + tot + 40, 360], 40, fill=(255, 255, 255, 225))
                dr.text((x, 225), pres, font=fp, fill=COLOR[leader])
                flecha(dr, x + wp + 40, 285, 90, (175, 182, 198))
                dr.text((x + wp + 160, 232), "?", font=fa, fill=(175, 182, 198))
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
                portada = frame.copy()
                portada.alpha_composite(ui)

        if t < INTRO + 0.4:
            a = int(255 * min(1, (INTRO + 0.4 - t) / 0.5))
            tw = dr.textlength(titulo, font=ft)
            y = 270 - 30 * max(0, 0.4 - t) / 0.4
            dr.rounded_rectangle([W / 2 - tw / 2 - 50, y - 20, W / 2 + tw / 2 + 50, y + 160], 50, fill=ACENTO + (int(a * 0.95),))
            dr.text((W / 2 - tw / 2, y), titulo, font=ft, fill=(255, 255, 255, a))
            sw = dr.textlength(sub, font=fn)
            dr.text((W / 2 - sw / 2, y + 112), sub, font=fn, fill=(255, 255, 255, a))
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
    L = lineas(d["letra"])
    tiempos = os.path.join(AQUI, "tiempos", f"{nivel}-{unidad}-{tipo}.json")
    if os.path.exists(tiempos):
        T = json.load(open(tiempos, encoding="utf-8"))
        L, dur = T["lines"], T["duration"]
    else:
        dur, hit, total = alinea(os.path.join(PORTAL, "audio", "songs", d["archivo"]), L)
        os.makedirs(os.path.dirname(tiempos), exist_ok=True)
        json.dump({"duration": dur, "hit": hit, "total": total, "lines": L}, open(tiempos, "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)
    out = os.path.join(AQUI, "out", f"{nivel}-{unidad}-{tipo}.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for l in L:  # la intro corre el audio
        l["t"] = [[a + INTRO, b + INTRO] for a, b in l["t"]]
    render(nivel, unidad, tipo, d, L, dur + INTRO, out)
