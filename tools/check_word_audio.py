# -*- coding: utf-8 -*-
"""Comprueba que cada mp3 de vocabulario dice de verdad su palabra.

Manda los audios al reconocedor de voz de ElevenLabs y compara la
transcripcion con la palabra esperada. Sirve para detectar sin oirlos los
fallos tipicos del TTS: palabras leidas como otra cosa, letras deletreadas,
o terminos que el modelo pronuncia mal.

    python tools/check_word_audio.py
"""
import json, os, re, sys, urllib.request, urllib.error, uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_FILES = [r"C:\Projects\mocks-cambridge\elevenlabs-key.txt",
             r"C:\Projects\mocks-cambridge\A2 Level.txt"]
WORDS = os.path.join(ROOT, "audio", "words")
DEMO = [("starters", [1, 2]), ("movers", [1, 2]), ("flyers", [1, 2])]


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


# El reconocedor escribe en ingles americano y a veces antepone el articulo.
# Ni una cosa ni la otra son fallos de pronunciacion.
EQUIV = {"theater": "theatre", "gray": "grey", "color": "colour",
         "airplane": "aeroplane", "mom": "mum"}


def norm(t):
    """Para comparar: minusculas, sin puntuacion, sin articulo, grafia GB."""
    t = re.sub(r"[^a-z ]", "", (t or "").lower()).strip()
    t = re.sub(r"^(the|a|an) ", "", t)
    return " ".join(EQUIV.get(w, w) for w in t.split())


def transcribe(path, api_key):
    b = "----" + uuid.uuid4().hex
    def campo(n, v):
        return ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n'
                % (b, n, v)).encode()
    data = campo("model_id", "scribe_v1") + campo("language_code", "eng")
    data += ('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\n'
             'Content-Type: audio/mpeg\r\n\r\n' % (b, os.path.basename(path))).encode()
    data += open(path, "rb").read() + b"\r\n" + ("--%s--\r\n" % b).encode()
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/speech-to-text", data=data, method="POST",
        headers={"xi-api-key": api_key,
                 "Content-Type": "multipart/form-data; boundary=" + b})
    return json.load(urllib.request.urlopen(req, timeout=120))


def main():
    palabras = []
    for lvl, units in DEMO:
        for n in units:
            ud = json.load(open(os.path.join(ROOT, "content", lvl, "unit-%02d.json" % n),
                                encoding="utf-8"))
            for w in ud.get("wordlist", []):
                if w not in palabras:
                    palabras.append(w)

    api_key = key()
    malos, dudosos, ok = [], [], 0
    for w in palabras:
        p = os.path.join(WORDS, slug(w) + ".mp3")
        if not os.path.exists(p):
            malos.append((w, "FALTA EL MP3", 0.0))
            continue
        try:
            r = transcribe(p, api_key)
        except urllib.error.HTTPError as e:
            print("  %-18s HTTP %s — se corta" % (w, e.code))
            break
        dicho = norm(r.get("text"))
        esperado = norm(w)
        prob = r.get("language_probability", 0)
        if dicho == esperado:
            ok += 1
        elif dicho.replace(" ", "") == esperado.replace(" ", ""):
            ok += 1                       # solo difiere el espaciado
        else:
            (dudosos if esperado in dicho or dicho in esperado else malos).append(
                (w, r.get("text"), prob))

    print("\n%d palabras · %d correctas" % (len(palabras), ok))
    if dudosos:
        print("\nCon matices (se entiende la palabra, pero no es exacta):")
        for w, dicho, prob in dudosos:
            print('  %-18s -> "%s"' % (w, dicho))
    if malos:
        print("\nMAL PRONUNCIADAS o irreconocibles:")
        for w, dicho, prob in malos:
            print('  %-18s -> "%s"' % (w, dicho))
    if not malos and not dudosos:
        print("Todas se reconocen exactamente. Ingles correcto.")


if __name__ == "__main__":
    main()
