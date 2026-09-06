# -*- coding: utf-8 -*-
"""Lleva las canciones al curso: copia los mp3 y escribe la letra que ve el alumno.

Las letras viven en songs/<nivel>.json y los mp3 aprobados en songs/audio/.
El motor necesita las dos cosas dentro del portal, y sobre todo necesita saber
CUALES tienen audio: una pantalla de cancion sin cancion es peor que no tener
pantalla ([[nada-incompleto-en-vivo]]). Por eso la disponibilidad se calcula
del disco, no se declara a mano.

    python tools/build_songs.py            # todos los niveles que existan
    python tools/build_songs.py starters
"""
import glob, io, json, os, re, shutil, sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS = os.path.join(AQUI, "songs")
PORTAL = r"C:\Projects\nis-portal\nis-fun"
DESTINO_AUDIO = os.path.join(PORTAL, "audio", "songs")
DESTINO_DATOS = os.path.join(PORTAL, "content")

# En songs/audio los archivos se llaman en-<nivel>-<NN>-<chant|cancion>.mp3.
# Dentro del curso se quita el idioma: el motor ya sabe en cual esta.
NOMBRE = re.compile(r"^en-(starters|movers|flyers)-(\d{2})-(chant|cancion)"
                    r"(?:-v\d+)?\.mp3$")


def mp3_disponibles():
    """Que mp3 hay de verdad en disco, por (nivel, unidad, tipo)."""
    hay = {}
    for f in sorted(glob.glob(os.path.join(SONGS, "audio", "*.mp3"))):
        m = NOMBRE.match(os.path.basename(f))
        if not m:
            continue
        nivel, u, tipo = m.groups()
        # una toma "-v1" es una version vieja: solo vale si no hay definitiva
        if os.path.basename(f).count("-v") and (nivel, u, tipo) in hay:
            continue
        hay[(nivel, u, tipo)] = f
    return hay


def construye(nivel, hay):
    p = os.path.join(SONGS, nivel + ".json")
    if not os.path.exists(p):
        return None
    datos = json.load(io.open(p, encoding="utf-8"))["unidades"]

    os.path.isdir(DESTINO_AUDIO) or os.makedirs(DESTINO_AUDIO)
    fuera, copiados = {}, 0
    for n in sorted(datos, key=int):
        e = datos[n]
        piezas = {}
        for tipo, clave in (("chant", "chant"), ("cancion", "cancion")):
            src = hay.get((nivel, n, tipo))
            if not src:
                continue                      # sin mp3 no se ofrece
            dst = os.path.join(DESTINO_AUDIO, "%s-%s-%s.mp3" % (nivel, n, tipo))
            if not os.path.exists(dst) or \
               os.path.getsize(dst) != os.path.getsize(src):
                shutil.copy2(src, dst)
                copiados += 1
            piezas[tipo] = {"titulo": e[clave]["titulo"],
                            "letra": e[clave]["letra"],
                            "archivo": os.path.basename(dst)}
        if piezas:
            piezas["groove"] = e["cancion"].get("groove", "")
            fuera[n] = piezas

    salida = os.path.join(DESTINO_DATOS, "songs-%s.json" % nivel)
    io.open(salida, "w", encoding="utf-8").write(json.dumps(
        {"_nivel": nivel,
         "_nota": "Solo las unidades cuyo mp3 ya esta en el curso. Lo escribe "
                  "tools/build_songs.py mirando el disco; no editar a mano.",
         "unidades": fuera}, ensure_ascii=False, indent=1) + "\n")
    return len(fuera), copiados, len(datos)


def main(argv):
    niveles = argv or ["starters", "movers", "flyers"]
    hay = mp3_disponibles()
    for nivel in niveles:
        r = construye(nivel, hay)
        if r is None:
            continue
        con, cop, total = r
        print("%-9s %2d de %2d unidades con audio  (%d mp3 copiados)"
              % (nivel, con, total, cop))
    return 0


if __name__ == "__main__":
    sys.exit(main([a for a in sys.argv[1:] if not a.startswith("-")]))
