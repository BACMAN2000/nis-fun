# -*- coding: utf-8 -*-
"""Publica los seis videos doblados y ensena al motor a pedirlos.

Los mp4 franceses van al lado de los ingleses con el sufijo -fr; el motor
elige por idioma. El poster no cambia: es una imagen, no tiene idioma.

    python build-videos/publica_fr.py
"""
import io, os, shutil, sys

ORIGEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz-fr")
VIDEOS = r"C:\Projects\nis-portal\nis-fun\assets\videos"
E = r"C:\Projects\nis-portal\nis-fun\engine"

NOMBRES = ["pip-intro", "luna-intro", "kili-intro",
           "starters-cast", "movers-cast", "flyers-cast"]

# index.html: el video de la mascota, en la portada y en el hub del nivel.
INDEX = [
    ("""            <source src="../assets/videos/${l.mascot}-intro.mp4?v=${VIDEO_V}" type="video/mp4">""",
     """            <source src="../assets/videos/${l.mascot}-intro${VSUF}.mp4?v=${VIDEO_V}" type="video/mp4">"""),
    ("""          src="../assets/videos/${idx.mascot}-intro.mp4?v=${VIDEO_V}\"""",
     """          src="../assets/videos/${idx.mascot}-intro${VSUF}.mp4?v=${VIDEO_V}\""""),
    ("""const VIDEO_V = '2026-08-25-marca';""",
     """const VIDEO_V = '2026-09-02-fr';
/* Los videos SI se separan por idioma, como el audio: el mismo mp4 doblado
   al frances vive al lado con el sufijo -fr. El poster no, que es una
   imagen y no tiene idioma. */
const VSUF = LANG === 'fr' ? '-fr' : '';"""),
]

# banner.js: el video del elenco. Lo carga antes que index.html, asi que se
# calcula el sufijo aqui en vez de compartir la constante.
BANNER = [
    ("""    const castVideo = `../assets/videos/${nivel}-cast.mp4?v=${window.ART_V || ''}`;""",
     """    const sufijo = window.LANG === 'fr' ? '-fr' : '';
    const castVideo = `../assets/videos/${nivel}-cast${sufijo}.mp4?v=${window.VIDEO_V || window.ART_V || ''}`;"""),
]


def parchea(ruta, cambios):
    s = io.open(ruta, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    hechos = 0
    for v, n in cambios:
        if n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA en %s (%d): %r"
                  % (os.path.basename(ruta), t.count(v), v[:70]))
            return None
        t = t.replace(v, n)
        hechos += 1
    io.open(ruta, "w", encoding="utf-8",
            newline="\r\n" if crlf else "\n").write(t)
    return hechos


def main():
    faltan = [n for n in NOMBRES
              if not os.path.exists(os.path.join(ORIGEN, n + "-fr.mp4"))]
    if faltan:
        print("faltan por doblar:", ", ".join(faltan))
        return 1
    for n in NOMBRES:
        shutil.copy2(os.path.join(ORIGEN, n + "-fr.mp4"),
                     os.path.join(VIDEOS, n + "-fr.mp4"))
    print("6 videos copiados a assets/videos/")

    for f, c in (("index.html", INDEX), ("banner.js", BANNER)):
        r = parchea(os.path.join(E, f), c)
        if r is None:
            return 1
        print("  %s: %d cambios" % (f, r))

    # window.VIDEO_V lo necesita banner.js, que no ve las constantes del
    # script de la pagina.
    p = os.path.join(E, "index.html")
    s = io.open(p, encoding="utf-8", newline="").read()
    if "window.VIDEO_V" not in s:
        crlf = "\r\n" in s
        t = s.replace("\r\n", "\n").replace(
            "const VSUF = LANG === 'fr' ? '-fr' : '';",
            "const VSUF = LANG === 'fr' ? '-fr' : '';\n"
            "window.VIDEO_V = VIDEO_V;   // banner.js lo usa para su propio ?v=")
        io.open(p, "w", encoding="utf-8",
                newline="\r\n" if crlf else "\n").write(t)
        print("  index.html: window.VIDEO_V expuesto")
    return 0


if __name__ == "__main__":
    sys.exit(main())
