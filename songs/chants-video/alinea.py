"""Alinea la letra de cada chant de Rhymes & chants con su mp3 (faster-whisper).

Uso: python songs/chants-video/alinea.py [id ...]     (sin ids: todos los mp3 de songs/audio/chants)
Deja songs/chants-video/tiempos/<id>.json con, por línea, quién la canta y el
tiempo de cada palabra. Las palabras que whisper no oye se reparten entre las
vecinas (igual que en songs/clases/2B-u5-prepositions/alinea.py).
"""
import difflib, json, os, re, subprocess, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
SONGS = os.path.dirname(AQUI)
CHANTS = {c["id"]: c for c in json.load(open(os.path.join(SONGS, "chants-tradicionales.json"), encoding="utf-8"))["chants"]}
SUNO = json.load(open(os.path.join(SONGS, "chants-tradicionales-suno.json"), encoding="utf-8"))["chants"]


def letra(cid):
    c = CHANTS[cid]
    return c["letra_nis"] if SUNO[cid]["version"] == "nis" and "letra_nis" in c else c["letra"]


def lineas(cid):
    out, sec = [], None
    for raw in letra(cid).splitlines():
        raw = raw.strip()
        if not raw:
            continue
        m = re.fullmatch(r"\[([^\]]+)\]", raw)
        if m:
            sec = m.group(1)
            continue
        quien = None
        m = re.match(r"\[([^\]]+)\]\s*(.*)", raw)
        if m:
            quien, raw = m.group(1), m.group(2)
        out.append({"sec": sec, "who": quien, "text": raw, "words": raw.split()})
    return out


norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower().replace("á", "a"))


def alinea(model, cid):
    mp3 = os.path.join(SONGS, "audio", "chants", cid + ".mp3")
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    L = lineas(cid)
    flat = [(li, wi, norm(w)) for li, l in enumerate(L) for wi, w in enumerate(l["words"])]
    best = None
    # con la letra de pista suele ir mejor, pero a veces whisper se desvía con ella: se prueba también sin
    for prompt in (" ".join(l["text"] for l in L[:8]), None):
        segs, info = model.transcribe(audio, language="en", word_timestamps=True, vad_filter=False, initial_prompt=prompt)
        heard = [(norm(w.word).replace("thomas", "tomas"), w.start, w.end) for s in segs for w in s.words if norm(w.word)]
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
    os.makedirs(os.path.join(AQUI, "tiempos"), exist_ok=True)
    json.dump({"id": cid, "duration": info.duration, "hit": hit, "total": len(flat), "lines": L},
              open(os.path.join(AQUI, "tiempos", cid + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{cid}: {hit}/{len(flat)} palabras ({100*hit/len(flat):.0f} %), {info.duration:.0f} s", flush=True)


if __name__ == "__main__":
    from faster_whisper import WhisperModel
    ids = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(os.path.join(SONGS, "audio", "chants")) if f.endswith(".mp3"))
    model = WhisperModel("medium.en", device="cpu", compute_type="int8")
    for cid in ids:
        alinea(model, cid)
