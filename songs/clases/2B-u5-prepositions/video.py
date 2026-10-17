"""Monta el video karaoke «Where Is Teddy?».

Uso: python video.py toma.mp3 tiempos.json salida.mp4 [alto]

En cada estrofa, mientras se canta «Where is Teddy? ... you will see!» la
escena sale sin Teddy y con una interrogación: los niños adivinan. Cuando se
canta la preposición, Teddy aparece en su sitio y la preposición sale en su
color. En el estribillo se ilumina la viñeta de la preposición que suena.
"""
import json, subprocess, sys
from PIL import Image, ImageDraw
import escenas as E

FPS = 24
VERSE_SCENE = {"Verse 1": "in", "Verse 2": "on", "Verse 3": "behind",
               "Verse 4": "in front of", "Verse 5": "next to", "Verse 6": "between"}
PHRASES = ["in front of", "next to", "between", "behind", "on", "in"]


def spans(words):
    """[(i0, i1, frase)] de las preposiciones de una línea."""
    low = [E_norm(w) for w in words]
    out, i = [], 0
    while i < len(low):
        for p in PHRASES:
            pw = p.split()
            if low[i:i + len(pw)] == pw:
                out.append((i, i + len(pw), p))
                i += len(pw)
                break
        else:
            i += 1
    return out


def E_norm(w):
    return "".join(c for c in w.lower() if c.isalpha())


def karaoke(im, line, nxt, t):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([60, 28, E.W - 60, 250], 36, fill=(255, 255, 255, 240))
    words = line["words"]
    size = 76
    while True:
        f = E.font(size)
        widths = [d.textlength(w + " ", font=f) for w in words]
        if sum(widths) < E.W - 200 or size < 40:
            break
        size -= 4
    color_of = {}
    for a, b, p in spans(words):
        for k in range(a, b):
            color_of[k] = E.COLORS[p]
    x = E.W / 2 - sum(widths) / 2
    for k, (w, (t0, t1)) in enumerate(zip(words, line["t"])):
        base = color_of.get(k, E.NAVY)
        fill = base if t >= t0 else (190, 196, 210)
        d.text((x, 70), w, font=f, fill=fill)
        if k in color_of and t >= t0:
            d.line([(x, 70 + size + 8), (x + d.textlength(w, font=f), 70 + size + 8)], fill=base, width=6)
        x += widths[k]
    if nxt:
        f2 = E.font(40, "Book")
        tw = d.textlength(nxt["text"], font=f2)
        d.text((E.W / 2 - tw / 2, 182), nxt["text"], font=f2, fill=(150, 158, 175))


def pill(im, text, y=330):
    d = ImageDraw.Draw(im)
    f = E.font(96, "Round")
    tw = d.textlength(text, font=f)
    c = E.COLORS[text]
    d.rounded_rectangle([90, y, 90 + tw + 100, y + 150], 75, fill=c)
    d.text((140, y + 18), text, font=f, fill="white")


def question(im):
    d = ImageDraw.Draw(im)
    f = E.font(260, "Round")
    d.text((E.W / 2 - d.textlength("?", font=f) / 2, 360), "?", font=f, fill=(41, 128, 185))


def frame_for(t, lines, dur):
    first = lines[0]["t"][0][0]
    if t < first - 0.3:
        return E.title_card("Where Is Teddy?", "Prepositions of place · English 2B · Unit 5")
    last_end = lines[-1]["t"][-1][1]
    if t > last_end + 1.0:
        return E.title_card("Great job!", "in · on · behind · in front of · next to · between")
    idx = 0
    for i, l in enumerate(lines):
        if l["t"][0][0] - 0.3 <= t:
            idx = i
    line = lines[idx]
    nxt = lines[idx + 1] if idx + 1 < len(lines) else None
    sec = line["sec"]
    # número de línea dentro de su sección
    pos = sum(1 for l in lines[:idx] if l["sec"] == sec and l.get("_blk") == line.get("_blk"))
    if sec in VERSE_SCENE:
        name = VERSE_SCENE[sec]
        layers = E.scene(name)
        if pos < 2:  # aún no se ha dicho dónde está: escena sin Teddy
            im = E.compose([l for l in layers if not l[3]], t)
            question(im)
        else:
            im = E.compose(layers, t)
            pill(im, name)
    elif "Chorus" in sec:
        active = None
        for l in lines[:idx + 1][-2:]:
            if l["sec"] != sec:
                continue
            for a, b, p in spans(l["words"]):
                if l["t"][a][0] <= t:
                    active = p
        if pos >= 2:
            active = None
        im = E.chorus_board(active).convert("RGBA")
    else:  # Bridge: el pueblo
        im = E.town_frame(t, "me" if pos == 3 else None)
        tag = {1: "next to", 2: "behind", 3: "in front of"}.get(pos)
        if tag:
            pill(im, tag, y=300)
    karaoke(im, line, nxt, t)
    return im


def main():
    mp3, tj, out = sys.argv[1:4]
    height = int(sys.argv[4]) if len(sys.argv) > 4 else 1080
    data = json.load(open(tj, encoding="utf-8"))
    lines = data["lines"]
    blk, prev = 0, None
    for l in lines:  # cada repetición del estribillo es un bloque distinto
        if l["sec"] != prev:
            blk += 1
        l["_blk"], prev = blk, l["sec"]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", mp3]).decode().strip())
    w = height * 16 // 9
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{E.W}x{E.H}", "-r", str(FPS), "-i", "-", "-i", mp3,
                           "-vf", f"scale={w}:{height}", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "24" if height >= 1080 else "26", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)
    n = int(dur * FPS) + 1
    for i in range(n):
        ff.stdin.write(frame_for(i / FPS, lines, dur).convert("RGB").tobytes())
        if i % (FPS * 20) == 0:
            print(f"{i / FPS:.0f}/{dur:.0f} s", flush=True)
    ff.stdin.close()
    ff.wait()
    print("listo", out)


if __name__ == "__main__":
    main()
