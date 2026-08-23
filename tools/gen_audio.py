# -*- coding: utf-8 -*-
"""Genera el audio de las actividades C (listening) con ElevenLabs.

- Una voz fija por personaje (contrato de la biblia).
- Parsea el script: segmentos separados por '…', cada uno "Hablante: texto".
- Concatena los mp3 de los segmentos en audio/<nivel>/uNN-c.mp3.
- Idempotente: salta los archivos que ya existen.
- Si se acaba la cuota (HTTP 401/429), para y deja lo generado.
"""
import json, os, sys, glob, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_FILE = r"C:\Projects\mocks-cambridge\A2 Level.txt"
API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128"

VOICES = {
    # Flyers — La Expedición Aurora
    "ingrid":    "MF3mGyEYCl7XYWbV9V6O",  # Elli — joven, decidida
    "diego":     "ErXwobaYiN019PkySvjV",  # Antoni — enérgico
    "maya":      "EXAVITQu4vr4xnSDxMaL",  # Bella — serena
    "oliver":    "yoZ06aMxZJJ28mfd3POQ",  # Sam — cálido
    # Movers — El Club del Fiordo
    "erik":      "ErXwobaYiN019PkySvjV",
    "valentina": "EXAVITQu4vr4xnSDxMaL",
    "sofia":     "MF3mGyEYCl7XYWbV9V6O",
    "mateo":     "yoZ06aMxZJJ28mfd3POQ",
    # Starters — Los Exploradores del Faro
    "freya":     "MF3mGyEYCl7XYWbV9V6O",
    "nico":      "ErXwobaYiN019PkySvjV",
    "astrid":    "EXAVITQu4vr4xnSDxMaL",
    "tomas":     "yoZ06aMxZJJ28mfd3POQ",
    # Adultos / invitados
    "rosa":      "21m00Tcm4TlvDq8ikWAM",  # Rachel
    "grandpa":   "pNInz6obpgDQGcFmaJgB",  # Adam
    "carla":     "AZnzlk1XvdvUeBnXmlld",  # Domi
}
DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"

def key():
    with open(KEY_FILE, encoding="utf-8") as f:
        return f.readline().strip()

def tts(text, voice, api_key):
    body = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }).encode()
    req = urllib.request.Request(API.format(voice=voice), data=body, method="POST", headers={
        "xi-api-key": api_key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def main():
    api_key = key()
    files = sorted(glob.glob(os.path.join(ROOT, "content", "*", "unit-*.json")))
    done = skipped = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            ud = json.load(f)
        for act in ud.get("activities", []):
            if act.get("type") != "listening" or "audio" not in act:
                continue
            out = os.path.join(ROOT, "audio", act["audio"].replace("/", os.sep))
            if os.path.exists(out):
                skipped += 1
                continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            segments = [s.strip() for s in act["data"]["script"].split("…") if s.strip()]
            blob = b""
            try:
                for seg in segments:
                    if ":" in seg:
                        speaker, text = seg.split(":", 1)
                        voice = VOICES.get(speaker.strip().lower(), DEFAULT_VOICE)
                        text = text.strip()
                    else:
                        voice, text = DEFAULT_VOICE, seg
                    if not text:
                        continue
                    blob += tts(text, voice, api_key)
                    time.sleep(0.25)
            except Exception as e:
                print(f"STOP en {ud['id']}: {e}")
                print(f"Generados: {done} · ya existian: {skipped}")
                sys.exit(1)
            with open(out, "wb") as f:
                f.write(blob)
            done += 1
            print(f"{ud['id']} -> {act['audio']} ({len(blob)//1024} KB)")
    print(f"LISTO. Generados: {done} · ya existian: {skipped}")

if __name__ == "__main__":
    main()
