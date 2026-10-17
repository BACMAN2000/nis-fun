"""Transcribe una toma con faster-whisper y alinea cada palabra de la letra.

Uso: python alinea.py toma.mp3 salida.json
Imprime cuántas palabras de la letra se reconocen (la toma que se entiende
mejor es la que más reconoce) y guarda, por palabra, su tiempo de inicio y fin.
Las palabras que whisper no oyó se reparten entre las vecinas que sí oyó.
"""
import difflib, json, re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

LETRA = open(__file__.replace("alinea.py", "letra.txt"), encoding="utf-8").read()


def lineas():
    out, sec = [], None
    for raw in LETRA.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith("["):
            sec = raw.strip("[]")
            continue
        out.append({"sec": sec, "text": raw, "words": raw.split()})
    return out


norm = lambda w: re.sub(r"[^a-z]", "", w.lower())

if __name__ == "__main__":
    mp3, out = sys.argv[1], sys.argv[2]
    model = WhisperModel("medium.en", device="cpu", compute_type="int8")
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout  # av de faster-whisper falla con este ffmpeg
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, info = model.transcribe(audio, language="en", word_timestamps=True, vad_filter=False,
                                  initial_prompt=" ".join(l["text"] for l in lineas()[:8]))
    heard = [(norm(w.word), w.start, w.end) for s in segs for w in s.words if norm(w.word)]
    L = lineas()
    flat = [(li, wi, norm(w)) for li, l in enumerate(L) for wi, w in enumerate(l["words"])]
    sm = difflib.SequenceMatcher(None, [f[2] for f in flat], [h[0] for h in heard], autojunk=False)
    times = [None] * len(flat)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            times[a + k] = heard[b + k][1:]
    hit = sum(t is not None for t in times)
    # rellenar huecos interpolando entre las palabras oídas
    known = [i for i, t in enumerate(times) if t]
    for i in range(len(times)):
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
    json.dump({"duration": info.duration, "hit": hit, "total": len(flat), "lines": L},
              open(out, "w", encoding="utf-8"), indent=1)
    print(f"{mp3}: {hit}/{len(flat)} palabras reconocidas ({100*hit/len(flat):.0f} %), {info.duration:.0f} s")
