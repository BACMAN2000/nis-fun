# -*- coding: utf-8 -*-
"""Graba con Edge TTS todo lo que el curso lee en voz alta.

Hasta ahora, cuando no habia mp3, el curso recurria a la voz del navegador.
Eso falla en cuanto el equipo no tiene voces inglesas instaladas — y en el
portatil del colegio solo hay tres voces, las tres en castellano: las pistas
del crucigrama se leian con acento espanol o no se leian. El alumno lo ve
como "no funciona".

Con los mp3 grabados el curso deja de depender de lo que tenga el equipo.
Edge TTS es gratis y sin limite, asi que se graba todo:

  clues/        las pistas de los crucigramas
  stories/      la historia de apertura de cada unidad
  bubbles/      lo que dice el personaje en su bocadillo
  acts/         la instruccion que lee la mascota en cada actividad
  readers/      las frases de los cuentos de Nordic Little Readers

El nombre del archivo se saca del propio texto, con el mismo criterio que
usa SAY.slug() en el motor, para que el curso lo encuentre sin llevar
ninguna lista.

    python tools/gen_audio_edge.py            todo lo que falte
    python tools/gen_audio_edge.py clues      solo un bloque
    python tools/gen_audio_edge.py --contar   solo dice cuanto falta
"""
import asyncio, glob, io, json, os, re, sys

import edge_tts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
AUDIO = os.path.join(ROOT, "audio")
READERS = os.path.join(ROOT, "readers")

# La mascota guia el curso, asi que las instrucciones las dice siempre la
# misma voz. Las historias las narra una voz distinta, para que el alumno
# distinga quien habla sin mirar.
VOZ_GUIA = "en-GB-LibbyNeural"      # joven, clara: la mascota
VOZ_NARRA = "en-GB-SoniaNeural"     # la historia de la unidad
VOZ_PISTA = "en-GB-RyanNeural"      # las pistas del crucigrama
VOZ_CUENTO = "en-GB-LibbyNeural"    # los cuentos de primaria

# Despacio: son ninos de seis a diez anos.
RITMO = {"starters": "-18%", "movers": "-12%", "flyers": "-8%"}


def slug(t):
    """El mismo nombre que calcula SAY.slug() en el motor."""
    t = str(t).lower().replace("'", "")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60]


def limpia(t):
    """Quita el marcado que no se lee en voz alta."""
    t = re.sub(r"<[^>]+>", " ", str(t or ""))
    t = t.replace("…", "...").replace("—", ", ")
    return re.sub(r"\s+", " ", t).strip()


def trabajos(filtro):
    """(carpeta, nombre, texto, voz, ritmo) de todo lo que hay que grabar."""
    out = []

    def anade(carpeta, texto, voz, ritmo):
        t = limpia(texto)
        if len(t) < 3:
            return
        out.append((carpeta, slug(t), t, voz, ritmo))

    for f in sorted(glob.glob(os.path.join(CONTENT, "*", "unit-*.json"))):
        nivel = os.path.basename(os.path.dirname(f))
        r = RITMO.get(nivel, "-12%")
        d = json.load(io.open(f, encoding="utf-8"))
        sc = d.get("scene") or {}

        if not filtro or "stories" in filtro:
            if sc.get("intro"):
                anade("stories", sc["intro"], VOZ_NARRA, r)
        if not filtro or "bubbles" in filtro:
            if sc.get("bubble"):
                anade("bubbles", sc["bubble"], VOZ_NARRA, r)

        for a in d.get("activities", []):
            if not filtro or "acts" in filtro:
                t = a.get("instructions") or a.get("title")
                if t:
                    anade("acts", t, VOZ_GUIA, r)
            if (not filtro or "clues" in filtro) and a.get("type") == "crossword":
                for w in ((a.get("data") or {}).get("words") or []):
                    if w.get("clue"):
                        anade("clues", w["clue"], VOZ_PISTA, r)

    if not filtro or "readers" in filtro:
        for f in sorted(glob.glob(os.path.join(READERS, "data", "g*.json"))):
            d = json.load(io.open(f, encoding="utf-8"))
            for p in d.get("paginas", []):
                anade("readers", p["texto"], VOZ_CUENTO, "-20%")
            for it in (d.get("actividad") or {}).get("items", []):
                anade("readers", it["palabra"], VOZ_CUENTO, "-20%")

    # sin repetir: la misma frase en dos unidades es el mismo archivo
    visto, unicos = set(), []
    for t in out:
        k = (t[0], t[1])
        if k in visto:
            continue
        visto.add(k)
        unicos.append(t)
    return unicos


async def di(texto, voz, ritmo, destino):
    com = edge_tts.Communicate(texto, voz, rate=ritmo)
    with open(destino, "wb") as f:
        async for trozo in com.stream():
            if trozo["type"] == "audio":
                f.write(trozo["data"])


async def principal(filtro, solo_contar):
    todo = trabajos(filtro)
    pendientes = []
    for carpeta, nombre, texto, voz, ritmo in todo:
        base = READERS if carpeta == "readers" else AUDIO
        destino = os.path.join(base, "audio" if carpeta == "readers" else carpeta,
                               nombre + ".mp3")
        if carpeta == "readers":
            destino = os.path.join(READERS, "audio", nombre + ".mp3")
        if os.path.exists(destino) and os.path.getsize(destino) > 800:
            continue
        pendientes.append((carpeta, texto, voz, ritmo, destino))

    car = sum(len(t) for _, t, _, _, _ in pendientes)
    print("  %d piezas en total · %d por grabar · %s caracteres"
          % (len(todo), len(pendientes), format(car, ",")))
    if solo_contar or not pendientes:
        return

    hechos = fallos = 0
    for carpeta, texto, voz, ritmo, destino in pendientes:
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        try:
            await di(texto, voz, ritmo, destino)
            if os.path.getsize(destino) < 800:
                raise RuntimeError("archivo vacio")
            hechos += 1
            if hechos % 25 == 0:
                print("   %d/%d" % (hechos, len(pendientes)))
        except Exception as e:
            fallos += 1
            try:
                os.remove(destino)
            except OSError:
                pass
            print("FALLO %-9s %s — %s" % (carpeta, texto[:40], str(e)[:50]))
    print("")
    print("  %d grabados, %d fallidos" % (hechos, fallos))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    asyncio.run(principal(args, "--contar" in sys.argv))
