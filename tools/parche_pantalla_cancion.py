# -*- coding: utf-8 -*-
"""Engancha la pantalla de cancion en el motor.

Va justo DESPUES de las palabras en imagenes y antes de las actividades: la
cancion usa esas mismas palabras, y cantarlas recien vistas es lo que las fija.
Ademas hace de respiro entre mirar y trabajar.

Se parchea por ancla, nunca copiando el archivo entero: index.html lo tocan
varias sesiones a la vez ([[nis-fun-motor-dos-copias]]).
"""
import io, os, sys

E = r"C:\Projects\nis-portal\nis-fun\engine"

CAMBIOS = [
 # 1. cargar el modulo
 ('<script src="magicbox.js?v=8"></script>',
  '<script src="magicbox.js?v=8"></script>\n<script src="songs.js?v=1"></script>'),

 # 2. meter la pantalla en su sitio
 ("""      html: `<div class="scr-centro">${pwHTML}</div>`,
      alMostrar(){ wirePictureWords(); } },
  ];""",
  """      html: `<div class="scr-centro">${pwHTML}</div>`,
      alMostrar(){ wirePictureWords(); } },
  ];

  /* La cancion de la unidad, entre las palabras y las actividades: usa ese
     mismo vocabulario y cantarlo recien visto es lo que lo fija.
     SONGS.para devuelve null mientras la unidad no tenga su mp3 dentro del
     curso, y entonces no hay pantalla — un boton de reproducir que no suena
     es peor que no ofrecer nada. */
  const laCancion = window.SONGS ? await SONGS.para(LEVEL, UD.number) : null;
  if (laCancion) {
    const iban = pantallas[2].etiquetaSiguiente;
    pantallas[2].etiquetaSiguiente = laCancion.titulo;
    pantallas.splice(3, 0, {
      titulo: laCancion.titulo,
      etiquetaSiguiente: iban,
      html: laCancion.html,
      alMostrar: laCancion.alMostrar,
    });
  }"""),
]


def main():
    p = os.path.join(E, "index.html")
    s = io.open(p, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    n = 0
    for viejo, nuevo in CAMBIOS:
        if nuevo in t:
            continue
        if t.count(viejo) != 1:
            print("ANCLA FALLA (%d coincidencias): %r" % (t.count(viejo), viejo[:70]))
            return 1
        t = t.replace(viejo, nuevo)
        n += 1
    io.open(p, "w", encoding="utf-8",
            newline="\r\n" if crlf else "\n").write(t)
    print("index.html: %d cambios" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
