# -*- coding: utf-8 -*-
"""Graba en frances los cuentos de Nordic Little Readers.

El lector tiene un boton por pagina: si hay mp3 lo suena y si no lo lee la
voz del navegador. La voz del navegador depende de lo que el alumno tenga
instalado —en un Windows del colegio a veces no hay francesa— asi que las
paginas se graban de verdad.

Los nombres salen del propio texto con el mismo slug que usa di() en
readers/index.html: sin tildes, sin apostrofes y cortado a 60. El lector no
lleva ninguna lista de archivos, los busca por el nombre.

    python tools/gen_audio_readers_fr.py            todo lo que falte
    python tools/gen_audio_readers_fr.py --contar   solo dice cuanto falta
"""
import asyncio, glob, io, json, os, re, sys, unicodedata

import edge_tts

ROOT = r"C:\Projects\nis-portal\nis-fun\readers"
DATOS = os.path.join(ROOT, "data-fr")
AUDIO = os.path.join(ROOT, "audio-fr")

# La narradora de las paginas y la mascota que pide las palabras de la
# actividad: dos voces, para que se note cuando el cuento acaba y empieza
# el ejercicio.
VOZ_CUENTO = "fr-FR-DeniseNeural"
VOZ_PALABRA = "fr-FR-EloiseNeural"

# Por grado, como en el curso: a los de seis anos se les lee mas despacio.
RITMO = {"G1": "-22%", "G2": "-18%", "G3": "-14%", "G4": "-12%", "G5": "-8%"}


def slug(t):
    """El mismo nombre que calcula di() en readers/index.html."""
    t = "".join(c for c in unicodedata.normalize("NFD", str(t).lower())
                if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60]


def trabajos():
    out, visto = [], set()
    for f in sorted(glob.glob(os.path.join(DATOS, "*.json"))):
        if os.path.basename(f) == "index.json":
            continue
        d = json.load(io.open(f, encoding="utf-8"))
        r = RITMO.get(d.get("grado"), "-14%")
        for p in d.get("paginas", []):
            out.append((p["texto"], VOZ_CUENTO, r))
        for it in ((d.get("actividad") or {}).get("items") or []):
            out.append((it["palabra"], VOZ_PALABRA, "-25%"))
    unicos = []
    for texto, voz, ritmo in out:
        n = slug(texto)
        if not n or n in visto:
            continue
        visto.add(n)
        unicos.append((n, texto, voz, ritmo))
    return unicos


async def di(texto, voz, ritmo, destino):
    com = edge_tts.Communicate(texto, voz, rate=ritmo)
    with open(destino, "wb") as f:
        async for trozo in com.stream():
            if trozo["type"] == "audio":
                f.write(trozo["data"])


async def principal(solo_contar):
    todo = trabajos()
    pend = [(os.path.join(AUDIO, n + ".mp3"), t, v, r) for n, t, v, r in todo
            if not os.path.exists(os.path.join(AUDIO, n + ".mp3"))]
    print("%d grabaciones en total, %d por hacer" % (len(todo), len(pend)))
    if solo_contar:
        return
    os.makedirs(AUDIO, exist_ok=True)
    for i, (destino, texto, voz, ritmo) in enumerate(pend, 1):
        await di(texto, voz, ritmo, destino)
        print("  [%d/%d] %s" % (i, len(pend), os.path.basename(destino)))


if __name__ == "__main__":
    asyncio.run(principal("--contar" in sys.argv))
