# -*- coding: utf-8 -*-
"""Genera un mp3 por palabra del wordlist, para la pronunciacion al hacer clic.

Una sola voz de nina alegre para todo el vocabulario (a diferencia del
listening, que usa una voz por personaje): aqui lo que importa es que el
modelo de pronunciacion sea siempre el mismo.

Idempotente: salta las palabras que ya tienen mp3. Si se acaba la cuota
(401/429) para y deja lo generado.

    python tools/gen_word_audio.py                # las 6 unidades de la demo
    python tools/gen_word_audio.py starters:1,2   # solo esas
"""
import json, os, re, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# La key vive FUERA de los repos: este archivo se publica en GitHub.
# Se prueba primero la key nueva (plan creator) y se cae a la anterior.
KEY_FILES = [r"C:\Projects\mocks-cambridge\elevenlabs-key.txt",
             r"C:\Projects\mocks-cambridge\A2 Level.txt"]
VOICE = "nDJIICjR9zfJExIFeSCN"          # Emmaline — nina britanica; el usuario
                                        # pidio voces de nino alegres
API = "https://api.elevenlabs.io/v1/text-to-speech/{v}?output_format=mp3_44100_128"
OUT = os.path.join(ROOT, "audio", "words")

DEMO = [("starters", [1, 2]), ("movers", [1, 2]), ("flyers", [1, 2])]


def key():
    for p in KEY_FILES:
        try:
            m = re.search(r"(sk_[A-Za-z0-9]{20,})", open(p, encoding="utf-8").read())
            if m:
                return m.group(1)
        except OSError:
            continue
    raise SystemExit("no encuentro la API key de ElevenLabs en " + " ni ".join(KEY_FILES))


def slug(w):
    """museum -> museum ; chemist's -> chemists ; police station -> police-station"""
    return re.sub(r"[^a-z0-9]+", "-", w.lower().replace("'", "")).strip("-")


def tts(text, api_key):
    body = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        # mas estabilidad que en el listening: una palabra suelta no debe
        # salir con entonacion de frase ni acelerada
        # style alto = mas expresiva y alegre; stability media para que no
        # salga plana pero tampoco cambie de tono entre palabras
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.8,
                           "style": 0.55, "use_speaker_boost": True, "speed": 0.9},
    }).encode()
    req = urllib.request.Request(API.format(v=VOICE), data=body, method="POST",
                                 headers={"xi-api-key": api_key,
                                          "Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=90).read()


def main():
    targets = DEMO
    if len(sys.argv) > 1 and sys.argv[1] == "todo":
        # todas las unidades de los tres niveles
        targets = []
        for lvl in ("starters", "movers", "flyers"):
            idx = json.load(open(os.path.join(ROOT, "content", lvl, "index.json"),
                                 encoding="utf-8"))
            targets.append((lvl, [u["n"] for u in idx["units"]]))
    elif len(sys.argv) > 1:
        targets = []
        for part in sys.argv[1:]:
            lvl, units = part.split(":")
            targets.append((lvl, [int(x) for x in units.split(",")]))

    words = []
    for lvl, units in targets:
        for n in units:
            p = os.path.join(ROOT, "content", lvl, "unit-%02d.json" % n)
            ud = json.load(open(p, encoding="utf-8"))
            for w in ud.get("wordlist", []):
                if w not in words:
                    words.append(w)

    os.makedirs(OUT, exist_ok=True)
    api_key = key()
    hechas = saltadas = 0
    for w in words:
        dst = os.path.join(OUT, slug(w) + ".mp3")
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            saltadas += 1
            continue
        try:
            data = tts(w, api_key)
        except urllib.error.HTTPError as e:
            print("  %-18s HTTP %s — se corta aqui" % (w, e.code))
            break
        open(dst, "wb").write(data)
        hechas += 1
        print("  %-18s %6d bytes" % (w, len(data)))
        time.sleep(0.35)

    print("\n%d palabras: %d generadas, %d ya estaban" % (len(words), hechas, saltadas))


if __name__ == "__main__":
    main()
