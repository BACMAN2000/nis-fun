# -*- coding: utf-8 -*-
"""Regenera las palabras que el reconocedor no entiende bien.

Una palabra suelta sin contexto es dificil para el TTS: con poca estabilidad
el modelo improvisa y 'kite' sale como "key day". Este script prueba varias
combinaciones de ajustes y de texto para cada palabra problematica, y se
queda con la primera que el reconocedor de voz devuelve exacta.

    python tools/fix_word_audio.py kite shark scarf
    python tools/fix_word_audio.py            # relee el informe y arregla todo
"""
import json, os, re, sys, time, urllib.request, urllib.error, uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_FILES = [r"C:\Projects\mocks-cambridge\elevenlabs-key.txt",
             r"C:\Projects\mocks-cambridge\A2 Level.txt"]
VOICE = "nDJIICjR9zfJExIFeSCN"          # Emmaline — nina britanica
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{v}?output_format=mp3_44100_128"
STT = "https://api.elevenlabs.io/v1/speech-to-text"
OUT = os.path.join(ROOT, "audio", "words")

# De mas expresivo a mas neutro. Se conserva la alegria mientras se pueda:
# solo se sube la estabilidad si el reconocedor no entiende la palabra.
INTENTOS = [
    {"texto": "{w}.",        "stability": 0.60, "style": 0.40},
    {"texto": "{w}.",        "stability": 0.75, "style": 0.25},
    {"texto": "The {w}.",    "stability": 0.70, "style": 0.30},  # contexto de sustantivo
    {"texto": "{w}, {w}.",   "stability": 0.80, "style": 0.20},
    {"texto": "A {w}.",      "stability": 0.85, "style": 0.15},
]


def key():
    for p in KEY_FILES:
        try:
            m = re.search(r"(sk_[A-Za-z0-9]{20,})", open(p, encoding="utf-8").read())
            if m:
                return m.group(1)
        except OSError:
            continue
    raise SystemExit("no encuentro la API key")


def slug(w):
    return re.sub(r"[^a-z0-9]+", "-", w.lower().replace("'", "")).strip("-")


def norm(t):
    return re.sub(r"[^a-z ]", "", (t or "").lower()).strip()


def tts(texto, api_key, stability, style):
    body = json.dumps({
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": stability, "similarity_boost": 0.8,
                           "style": style, "use_speaker_boost": True, "speed": 0.9},
    }).encode()
    req = urllib.request.Request(TTS.format(v=VOICE), data=body, method="POST",
                                 headers={"xi-api-key": api_key,
                                          "Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=90).read()


def stt(mp3, api_key):
    b = "----" + uuid.uuid4().hex
    def campo(n, v):
        return ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n'
                % (b, n, v)).encode()
    data = campo("model_id", "scribe_v1") + campo("language_code", "eng")
    data += ('--%s\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\n'
             'Content-Type: audio/mpeg\r\n\r\n' % b).encode()
    data += mp3 + b"\r\n" + ("--%s--\r\n" % b).encode()
    req = urllib.request.Request(STT, data=data, method="POST",
        headers={"xi-api-key": api_key,
                 "Content-Type": "multipart/form-data; boundary=" + b})
    return json.load(urllib.request.urlopen(req, timeout=120)).get("text", "")


def arregla(w, api_key):
    """Devuelve (mp3, descripcion) de la primera variante que se entienda."""
    esperado = norm(w)
    for i, cfg in enumerate(INTENTOS, 1):
        texto = cfg["texto"].format(w=w)
        try:
            audio = tts(texto, api_key, cfg["stability"], cfg["style"])
        except urllib.error.HTTPError as e:
            return None, "HTTP %s" % e.code
        dicho = norm(stt(audio, api_key))
        # la palabra debe aparecer entera; se admite el articulo que se le puso
        limpio = re.sub(r"^(the|a|an) ", "", dicho)
        if limpio == esperado or limpio == (esperado + " " + esperado):
            return audio, 'intento %d: "%s" (stab %.2f) -> "%s"' % (
                i, texto, cfg["stability"], dicho)
        time.sleep(0.3)
    return None, "ninguna variante se entendio"


def main():
    palabras = sys.argv[1:]
    if not palabras:
        raise SystemExit("uso: python tools/fix_word_audio.py <palabra> [palabra...]")
    api_key = key()
    for w in palabras:
        audio, info = arregla(w, api_key)
        if audio:
            open(os.path.join(OUT, slug(w) + ".mp3"), "wb").write(audio)
            print("  %-12s ARREGLADA  %s" % (w, info))
        else:
            print("  %-12s SIGUE MAL  %s" % (w, info))


if __name__ == "__main__":
    main()
