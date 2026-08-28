# -*- coding: utf-8 -*-
"""Trocea la hoja de companeros de clase y la instala en los tres niveles.

La hoja sale de Gemini con las seis fichas de characters/bible.md. El corte
lo hace cut_3d_sheet, que ya sabe separar figuras sobre fondo blanco; aqui
solo se decide donde va cada una.

Van a los tres niveles a proposito. El motor arma la ruta como
assets/characters/<nivel>/<slug>/, asi que un companero que solo viva en
starters no se puede usar en una escena de patio de flyers, y el patio es
justo donde salen. Pesan poco y asi funcionan en cualquier unidad.

    python tools/cut_classmates.py hoja.jpg [cols] [filas]
"""
import os, shutil, sys, tempfile

from cut_3d_sheet import cortar

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NIVELES = ("starters", "movers", "flyers")
COMPANEROS = ["lia", "bruno", "aiko", "samu", "iris", "tino"]

# La biblia pide 01 waving, 07 running, 06 sitting y 03 talking. De momento
# solo hay una figura por nino, asi que las cuatro poses apuntan a ella:
# mejor el mismo dibujo repetido que una casilla rota en la lamina.
POSES = ("pose-01.png", "pose-03.png", "pose-06.png", "pose-07.png",
         "fullbody.png")


def main(src, cols=3, filas=2):
    tmp = tempfile.mkdtemp(prefix="companeros-")
    hechos = cortar(src, cols, filas, COMPANEROS, destino=tmp, lado=720)
    if not hechos:
        raise SystemExit("no se recorto nada; revisa cols/filas")

    for slug in hechos:
        origen = os.path.join(tmp, slug + ".png")
        for nivel in NIVELES:
            carpeta = os.path.join(ROOT, "assets", "characters", nivel, slug)
            os.makedirs(carpeta, exist_ok=True)
            for pose in POSES:
                shutil.copyfile(origen, os.path.join(carpeta, pose))
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n%d companeros instalados en %s"
          % (len(hechos), ", ".join(NIVELES)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 3,
         int(sys.argv[3]) if len(sys.argv) > 3 else 2)
