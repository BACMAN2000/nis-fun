# -*- coding: utf-8 -*-
"""Graba con Edge TTS todo lo que el curso frances lee en voz alta.

Es el gemelo de gen_audio_edge.py, con dos diferencias que importan:

  * lee de content-fr/ y escribe en audio/fr/. El audio SI se separa por
    idioma —al reves que los dibujos, que se comparten—: 'train', 'six' u
    'orange' se escriben igual en los dos idiomas y no se pronuncian igual.
    Compartir carpeta haria sonar la voz inglesa en la clase de frances.
  * graba tambien words/ (una palabra por mp3) y los dialogos de escucha,
    que el curso ingles trae ya grabados de antes.

El nombre del archivo se saca del propio texto con el mismo criterio que
SAY.slug() en el motor —acentos incluidos: 'poupee.mp3', no 'poup-e.mp3'—
para que el curso lo encuentre sin llevar ninguna lista.

    python tools/gen_audio_fr.py                 todo lo que falte
    python tools/gen_audio_fr.py words clues     solo esos bloques
    python tools/gen_audio_fr.py --contar        solo dice cuanto falta
    python tools/gen_audio_fr.py --root <ruta>   otro arbol de trabajo

Edge TTS es gratis y sin limite: no hay cuota que administrar.
"""
import asyncio, glob, io, json, os, re, subprocess, sys, unicodedata

import edge_tts

# El contenido frances y el audio publicado viven en el arbol del portal, que
# es el que se despliega. --root permite trabajar sobre otra copia.
ROOT = r"C:\Projects\nis-portal\nis-fun"
if "--root" in sys.argv:
    ROOT = sys.argv[sys.argv.index("--root") + 1]
CONTENT = os.path.join(ROOT, "content-fr")
AUDIO = os.path.join(ROOT, "audio", "fr")

# Las mismas reglas que en ingles: la mascota guia siempre con la misma voz y
# la historia la narra otra, para que el alumno sepa quien habla sin mirar.
VOZ_GUIA = "fr-FR-EloiseNeural"      # joven y clara: la mascota y las palabras
VOZ_NARRA = "fr-FR-DeniseNeural"     # la historia y el bocadillo
VOZ_PISTA = "fr-FR-HenriNeural"      # las pistas del crucigrama

# Quien habla en los dialogos de escucha. Sin esto los dos personajes suenan
# igual y el alumno no sabe a quien esta escuchando.
VOCES_DIALOGO = {"freya": "fr-FR-EloiseNeural", "nico": "fr-FR-HenriNeural"}
VOZ_DIALOGO_DEF = VOZ_NARRA

# Despacio: son ninos de seis a diez anos.
RITMO = {"starters": "-18%", "movers": "-12%", "flyers": "-8%"}


def slug(t):
    """El mismo nombre que calcula SAY.slug() en el motor."""
    t = str(t).lower()
    t = "".join(c for c in unicodedata.normalize("NFD", t)
                if unicodedata.category(c) != "Mn")
    t = t.replace("'", "")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60]


def limpia(t):
    """Quita el marcado que no se lee en voz alta."""
    t = re.sub(r"<[^>]+>", " ", str(t or ""))
    t = t.replace("\u2026", "...").replace("\u2014", ", ")
    return re.sub(r"\s+", " ", t).strip()


def turnos(script):
    """Parte 'Nico : ... Freya : ...' en (quien, texto), en orden.

    El dialogo se graba por turnos y se pega despues: una sola voz leyendo a
    los dos personajes suena a lista de la compra, no a conversacion.
    """
    partes = re.split(r"(?:^|\s)(?:\u2026|\.\.\.)?\s*([A-Z][a-z]+)\s*:\s*", " " + script)
    out = []
    for i in range(1, len(partes) - 1, 2):
        texto = limpia(partes[i + 1]).strip(" .\u2026")
        if texto:
            out.append((partes[i].lower(), texto))
    return out


def trabajos(filtro):
    """(carpeta, nombre, texto, voz, ritmo) de todo lo que hay que grabar."""
    out = []

    def anade(carpeta, texto, voz, ritmo):
        t = limpia(texto)
        if len(t) < 2:
            return
        out.append((carpeta, slug(t), t, voz, ritmo))

    for f in sorted(glob.glob(os.path.join(CONTENT, "*", "unit-*.json"))):
        nivel = os.path.basename(os.path.dirname(f))
        r = RITMO.get(nivel, "-12%")
        d = json.load(io.open(f, encoding="utf-8"))
        sc = d.get("scene") or {}

        if not filtro or "words" in filtro:
            # La pantalla de palabras dice cada una al tocarla, y una palabra
            # suelta se lee mas despacio que dentro de una frase.
            for w in (d.get("wordlist") or []) + (d.get("wordlist_extra") or []):
                anade("words", w, VOZ_GUIA, "-25%")
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

    # sin repetir: la misma frase en dos unidades es el mismo archivo
    visto, unicos = set(), []
    for t in out:
        k = (t[0], t[1])
        if k in visto:
            continue
        visto.add(k)
        unicos.append(t)
    return unicos


def dialogos():
    """(destino, [(voz, texto)]) de cada actividad de escucha con guion."""
    out = []
    for f in sorted(glob.glob(os.path.join(CONTENT, "*", "unit-*.json"))):
        d = json.load(io.open(f, encoding="utf-8"))
        for a in d.get("activities", []):
            guion = (a.get("data") or {}).get("script")
            if not a.get("audio") or not guion:
                continue
            piezas = [(VOCES_DIALOGO.get(q, VOZ_DIALOGO_DEF), t) for q, t in turnos(guion)]
            if piezas:
                out.append((os.path.join(AUDIO, *a["audio"].split("/")), piezas))
    return out


async def di(texto, voz, ritmo, destino):
    com = edge_tts.Communicate(texto, voz, rate=ritmo)
    with open(destino, "wb") as f:
        async for trozo in com.stream():
            if trozo["type"] == "audio":
                f.write(trozo["data"])


async def graba_dialogo(destino, piezas, ritmo="-15%"):
    """Cada turno con su voz, pegados con una pausa corta entre medias."""
    tmp = destino + ".partes"
    os.makedirs(tmp, exist_ok=True)
    trozos = []
    for i, (voz, texto) in enumerate(piezas):
        p = os.path.join(tmp, f"{i:02d}.mp3")
        await di(texto, voz, ritmo, p)
        trozos.append(p)
    lista = os.path.join(tmp, "lista.txt")
    with io.open(lista, "w", encoding="utf-8") as f:
        for p in trozos:
            f.write("file '%s'\n" % p.replace("\\", "/"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", lista, "-c", "copy", destino], check=True)
    for p in trozos + [lista]:
        os.remove(p)
    os.rmdir(tmp)


async def principal(filtro, solo_contar):
    todo = trabajos(filtro)
    pendientes = []
    for carpeta, nombre, texto, voz, ritmo in todo:
        destino = os.path.join(AUDIO, carpeta, nombre + ".mp3")
        if not os.path.exists(destino):
            pendientes.append((destino, texto, voz, ritmo))

    dial = [] if (filtro and "dialogos" not in filtro) else \
        [(d, p) for d, p in dialogos() if not os.path.exists(d)]

    print("%d grabaciones en total, %d por hacer (+%d dialogos)"
          % (len(todo), len(pendientes), len(dial)))
    if solo_contar:
        for d, _, _, _ in pendientes[:10]:
            print("   falta", os.path.relpath(d, AUDIO))
        return

    for i, (destino, texto, voz, ritmo) in enumerate(pendientes, 1):
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        await di(texto, voz, ritmo, destino)
        print("  [%d/%d] %s" % (i, len(pendientes), os.path.relpath(destino, AUDIO)))

    for destino, piezas in dial:
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        await graba_dialogo(destino, piezas)
        print("  dialogo (%d turnos) %s" % (len(piezas), os.path.relpath(destino, AUDIO)))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--root" in sys.argv:
        args = [a for a in args if a != ROOT]
    asyncio.run(principal(set(args), "--contar" in sys.argv))
