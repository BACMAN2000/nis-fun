# -*- coding: utf-8 -*-
"""Graba con Edge TTS los dialogos de las tareas visuales de Flyers.

Sin esto el motor cae a la voz del navegador, y eso no vale en clase: el
portatil del colegio solo tiene voces castellanas, asi que el examen de
listening se oiria con acento espanol o directamente no se oiria.

Cada actividad es un mp3 con varias voces. El guion viene ya escrito en el
JSON como turnos separados por '…':

    Diego: And who is the boy with the green shirt? … Maya: That is Bruno.

Se graba turno a turno, cada personaje con SU voz, y se pegan los mp3 uno
detras de otro. Pegar streams de mp3 funciona en el navegador y evita meter
una dependencia de audio solo para concatenar.

La etiqueta 'Nombre:' NO se lee: es una acotacion para saber quien habla, no
parte del examen. La respuesta va siempre dentro de la frase.

    python tools/gen_audio_visual.py            graba lo que falte
    python tools/gen_audio_visual.py --contar   solo dice cuanto falta
    python tools/gen_audio_visual.py --rehacer  vuelve a grabar todo
"""
import asyncio
import glob
import io
import json
import os
import re
import sys

import edge_tts

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENIDO = os.path.join(RAIZ, "content", "flyers")
AUDIO = os.path.join(RAIZ, "audio")
CAST = json.load(io.open(os.path.join(RAIZ, "content", "cast-flyers.json"), encoding="utf-8"))

RITMO = "-8%"          # A2, ninos de diez anos
CONTAR = "--contar" in sys.argv
REHACER = "--rehacer" in sys.argv

# Dos voces por sexo para que dos ninas seguidas no suenen igual, y una
# neutra para la linea de instrucciones ("Listen and write the names").
VOCES_NINA = ["en-GB-SoniaNeural", "en-GB-LibbyNeural"]
VOCES_NINO = ["en-GB-RyanNeural", "en-GB-ThomasNeural"]
VOZ_NARRA = "en-GB-LibbyNeural"

# quien habla -> voz, fijo por personaje: si Diego cambia de voz entre dos
# unidades el alumno deja de reconocerlo
VOZ = {}
_n = _b = 0
for _slug, _p in CAST["personajes"].items():
    if _p["tipo"] == "nina":
        VOZ[_p["nombre"]] = VOCES_NINA[_n % len(VOCES_NINA)]
        _n += 1
    elif _p["tipo"] == "nino":
        VOZ[_p["nombre"]] = VOCES_NINO[_b % len(VOCES_NINO)]
        _b += 1
    else:
        VOZ[_p["nombre"]] = VOZ_NARRA


def turnos(guion):
    """(voz, texto) de cada turno del dialogo."""
    out = []
    for trozo in str(guion or "").split("…"):
        t = trozo.strip()
        if not t:
            continue
        m = re.match(r"^([A-Z][a-zA-Z]{1,12}):\s*(.+)$", t)
        if m and m.group(1) in VOZ:
            out.append((VOZ[m.group(1)], m.group(2).strip()))
        else:
            # sin etiqueta es la instruccion o una linea de narrador
            out.append((VOZ_NARRA, re.sub(r"^[A-Za-z]{1,12}:\s*", "", t)))
    return [(v, x) for v, x in out if len(x) >= 3]


def trabajos():
    out = []
    for ruta in sorted(glob.glob(os.path.join(CONTENIDO, "unit-*.json"))):
        d = json.load(io.open(ruta, encoding="utf-8"))
        for a in d.get("activities", []):
            if not a.get("audio"):
                continue
            guion = (a.get("data") or {}).get("script")
            if not guion or a["type"] not in ("label_people", "picture_mc", "match_pictures"):
                continue
            destino = os.path.join(AUDIO, *a["audio"].split("/"))
            out.append((d["number"], a["code"], destino, turnos(guion)))
    return out


async def turno(voz, texto):
    com = edge_tts.Communicate(texto, voz, rate=RITMO)
    buf = io.BytesIO()
    async for t in com.stream():
        if t["type"] == "audio":
            buf.write(t["data"])
    return buf.getvalue()


async def graba(partes, destino):
    """Los turnos se piden a la vez y se pegan en orden.

    Uno detras de otro tardaba minuto y medio por dialogo (107 dialogos, unos
    once turnos cada uno): hora y media para algo que se puede pedir en
    paralelo. gather conserva el orden de la lista, que es lo unico que
    importa aqui."""
    trozos = await asyncio.gather(*(turno(v, x) for v, x in partes))
    datos = b"".join(trozos)
    if len(datos) < 800:
        raise RuntimeError("salio un mp3 vacio")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "wb") as f:
        f.write(datos)


async def principal():
    todo = trabajos()
    pend = [t for t in todo
            if REHACER or not (os.path.exists(t[2]) and os.path.getsize(t[2]) > 800)]
    print("%d dialogos · %d por grabar · %d turnos"
          % (len(todo), len(pend), sum(len(t[3]) for t in pend)))
    if CONTAR or not pend:
        return

    hechos = fallos = 0
    for u, code, destino, partes in pend:
        try:
            await graba(partes, destino)
            hechos += 1
        except Exception as e:                      # noqa: BLE001
            fallos += 1
            print("  u%-2d %s  FALLO: %s" % (u, code, e))
        if hechos % 10 == 0 and hechos:
            print("  ... %d/%d" % (hechos, len(pend)))
    print("Grabados %d, fallos %d" % (hechos, fallos))


if __name__ == "__main__":
    asyncio.run(principal())
