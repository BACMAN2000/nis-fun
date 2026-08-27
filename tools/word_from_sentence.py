# -*- coding: utf-8 -*-
"""Regraba una palabra pronunciandola DENTRO de una frase, y la recorta.

Una palabra suelta es donde peor acierta el TTS: 'kite' le sale /kit/ en
vez de /kait/. Dentro de una frase la pronuncia bien porque tiene contexto
gramatical. Aqui se genera la frase, se piden los tiempos por palabra al
reconocedor y se recorta justo ese tramo.

Se comprueba ademas que el recorte, por si solo, se sigue reconociendo como
la palabra pedida: si no, no se pisa el audio anterior.

    python tools/word_from_sentence.py kite "This is a kite. The kite is red."
"""
import json, os, re, subprocess, sys, tempfile, urllib.request, uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from check_word_audio import key, norm            # reutiliza la key y el normalizador

VOICE = "nDJIICjR9zfJExIFeSCN"                    # Emmaline
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{v}?output_format=mp3_44100_128"
STT = "https://api.elevenlabs.io/v1/speech-to-text"
OUT = os.path.join(ROOT, "audio", "words")
FFMPEG = ("C:/Users/User/AppData/Local/Microsoft/WinGet/Packages/"
          "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/"
          "ffmpeg-8.1.2-full_build/bin/ffmpeg.exe")


def slug(w):
    return re.sub(r"[^a-z0-9]+", "-", w.lower().replace("'", "")).strip("-")


def tts(texto, api_key):
    body = json.dumps({
        "text": texto, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.65, "similarity_boost": 0.8,
                           "style": 0.35, "use_speaker_boost": True, "speed": 0.92},
    }).encode()
    req = urllib.request.Request(TTS.format(v=VOICE), data=body, method="POST",
                                 headers={"xi-api-key": api_key,
                                          "Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=90).read()


def stt(mp3, api_key, tiempos=True):
    b = "----" + uuid.uuid4().hex
    def campo(n, v):
        return ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n'
                % (b, n, v)).encode()
    data = campo("model_id", "scribe_v1") + campo("language_code", "eng")
    if tiempos:
        data += campo("timestamps_granularity", "word")
    data += ('--%s\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\n'
             'Content-Type: audio/mpeg\r\n\r\n' % b).encode()
    data += mp3 + b"\r\n" + ("--%s--\r\n" % b).encode()
    req = urllib.request.Request(STT, data=data, method="POST",
        headers={"xi-api-key": api_key, "Content-Type": "multipart/form-data; boundary=" + b})
    return json.load(urllib.request.urlopen(req, timeout=120))


def recorta(src, dst, ini, fin):
    subprocess.run([FFMPEG, "-y", "-v", "error", "-i", src,
                    "-ss", "%.3f" % ini, "-to", "%.3f" % fin,
                    "-af", "afade=t=in:st=0:d=0.02,afade=t=out:st=%.3f:d=0.06"
                           % max(0.02, fin - ini - 0.06),
                    dst], check=True)


def rehacer(palabra, frase, api_key):
    audio = tts(frase, api_key)
    tmp = os.path.join(tempfile.gettempdir(), "frase_%s.mp3" % slug(palabra))
    open(tmp, "wb").write(audio)
    r = stt(audio, api_key)
    objetivo = norm(palabra)
    for w in (r.get("words") or []):
        if w.get("type") != "word":
            continue
        if norm(w.get("text", "")) != objetivo:
            continue
        # margen generoso: cortar al ras se lleva por delante la
        # consonante final y el recorte deja de entenderse
        ini = max(0, float(w["start"]) - 0.14)
        fin = float(w["end"]) + 0.22
        corte = os.path.join(tempfile.gettempdir(), "corte_%s.mp3" % slug(palabra))
        recorta(tmp, corte, ini, fin)
        # el recorte debe seguir entendiendose solo
        dicho = norm(stt(open(corte, "rb").read(), api_key, tiempos=False).get("text"))
        if dicho == objetivo:
            dst = os.path.join(OUT, slug(palabra) + ".mp3")
            open(dst, "wb").write(open(corte, "rb").read())
            return True, 'de "%s" (%.2f-%.2f s), se reconoce como "%s"' % (
                frase, ini, fin, dicho)
        return False, 'el recorte se oye como "%s", no se pisa el anterior' % dicho
    return False, "el reconocedor no encontro la palabra en la frase"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    ok, info = rehacer(sys.argv[1], sys.argv[2], key())
    print(("  OK   " if ok else "  NO   ") + sys.argv[1] + "  " + info)
