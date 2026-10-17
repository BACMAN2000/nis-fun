"""Genera songs/chants-musica.json: qué rimas de Rhymes & chants tienen ya canción y video.

Uso: python songs/chants-video/publica.py
Solo entra un chant si existen su mp3 (songs/audio/chants) y su mp4 (chants-video/out):
la tarjeta del portal no ofrece nada que no esté hecho. Copiar el JSON a
nis-portal/nis-fun/songs/ y subir los archivos a /opt/nis-media:
  mp3 -> /opt/nis-media/nis-fun-audio/chants/   (web: /nis-fun/audio/chants/<id>.mp3)
  mp4 + jpg (portada) -> /opt/nis-media/videos/chants/        (web: /nis-fun/assets/videos/chants/<id>.mp4)
"""
import json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
SONGS = os.path.dirname(AQUI)
CHANTS = {c["id"]: c for c in json.load(open(os.path.join(SONGS, "chants-tradicionales.json"), encoding="utf-8"))["chants"]}
SUNO = json.load(open(os.path.join(SONGS, "chants-tradicionales-suno.json"), encoding="utf-8"))["chants"]

GENERO = {  # etiqueta corta para la tarjeta, sacada de estilo_v2
    "eeny-meeny": "hip-hop", "one-potato": "sea shanty", "ip-dip": "reggae", "bubble-gum": "rock 'n' roll",
    "engine-engine": "country", "inky-pinky": "Andean huayno", "tinker-tailor": "marching band",
    "fish-alive": "calypso", "icka-bicka": "ska", "sky-blue": "bossa nova", "miss-mary-mack": "K-pop",
    "sailor-went-to-sea": "surf rock", "pat-a-cake": "tarantella", "double-double": "Peruvian cumbia",
    "down-down-baby": "Motown soul", "teddy-bear": "Afrobeat", "cinderella": "samba", "i-like-coffee": "electro swing"}


def letra_cantada(cid):
    c = CHANTS[cid]
    t = c["letra_nis"] if SUNO[cid]["version"] == "nis" and "letra_nis" in c else c["letra"]
    t = re.sub(r"^\[(Intro|Verse.*|Break|Outro|Chorus)\]\s*\n?", "", t, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


out = {}
for cid, s in SUNO.items():
    if not (os.path.exists(os.path.join(SONGS, "audio", "chants", cid + ".mp3"))
            and os.path.exists(os.path.join(AQUI, "out", cid + ".mp4"))):
        continue
    out[cid] = {"titulo": s["titulo_suno"], "nueva_letra": s["version"] == "nis", "genero": GENERO[cid],
                "mp3": f"/nis-fun/audio/chants/{cid}.mp3", "mp4": f"/nis-fun/assets/videos/chants/{cid}.mp4",
                "poster": f"/nis-fun/assets/videos/chants/{cid}.jpg",
                "letra": letra_cantada(cid)}
json.dump({"_nota": "Generado por nis-fun/songs/chants-video/publica.py. Canción (Suno) y video karaoke de cada chant.",
           "chants": out}, open(os.path.join(SONGS, "chants-musica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "chants con música:", ", ".join(out))
