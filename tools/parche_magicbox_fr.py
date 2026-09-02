# -*- coding: utf-8 -*-
"""Mete las familias francesas en la caja magica.

No se traduce la tabla inglesa: se pone otra al lado. "bigger, biggest" no
existe en frances y la s de "he plays" tampoco; traducir la caja inglesa
ensenaria gramatica inglesa con palabras francesas. La tabla francesa
ensena lo que si es del frances —el genero de un/une, el acuerdo del
adjetivo, el partitif, el passe compose con avoir o con etre— y reusa los
mismos dibujos, que no tienen idioma.

Ademas quedan tres rotulos del propio motor de la caja: el titulo, el "Yes!"
y el "Try another one".
"""
import io, os, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = r"C:\Projects\nis-portal\nis-fun\engine\magicbox.js"
FR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "magicbox_fr.js")

ANCLA = """  /* Las unidades de repaso y las de estrategia de examen no llevan caja a
     proposito: no ensenan ninguna regla nueva, repasan las que ya se
     dieron. Ponerles una seria decorado, y ademas se la quitaria a la
     unidad donde esa regla si se explica. */
  const SIN_CAJA = /review|revision|strategies|exam strategies|whole course|paper strategies/i;

  function familiaDe(ud) {
    const t = ((ud.grammar || '') + ' ' + (ud.topic || '') + ' ' + (ud.title || '')).toLowerCase();
    if (SIN_CAJA.test(t)) return null;
    return FAMILIAS.find(f => f.busca.test(t)) || null;
  }"""

NUEVO_FAMILIA_DE = """  /* Las unidades de repaso y las de estrategia de examen no llevan caja a
     proposito: no ensenan ninguna regla nueva, repasan las que ya se
     dieron. Ponerles una seria decorado, y ademas se la quitaria a la
     unidad donde esa regla si se explica. */
  const SIN_CAJA = /review|revision|strategies|exam strategies|whole course|paper strategies/i;

  function familiaDe(ud) {
    const fr = window.LANG === 'fr';
    const t = ((ud.grammar || '') + ' ' + (ud.topic || '') + ' ' + (ud.title || '')).toLowerCase();
    if ((fr ? SIN_CAJA_FR : SIN_CAJA).test(t)) return null;
    return (fr ? FAMILIAS_FR : FAMILIAS).find(f => f.busca.test(t)) || null;
  }"""

ROTULOS = [
    ("""      titulo: '🎁 The Magic Box — ' + f.titulo,""",
     """      titulo: T('🎁 The Magic Box — ', '🎁 La Boîte Magique — ') + f.titulo,"""),
    ("""          eco.textContent = bien ? 'Yes! ⭐' : 'Try another one…';""",
     """          eco.textContent = bien ? T('Yes! ⭐', 'Oui ! ⭐') : T('Try another one…', 'Essaie encore…');"""),
]


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")

    if "FAMILIAS_FR" not in t:
        if t.count(ANCLA) != 1:
            print("ANCLA FALLA: familiaDe (%d)" % t.count(ANCLA))
            return 1
        fr = io.open(FR, encoding="utf-8", newline="").read().replace("\r\n", "\n")
        t = t.replace(ANCLA, fr.rstrip() + "\n\n" + NUEVO_FAMILIA_DE)

    for v, n in ROTULOS:
        if n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:60]))
            return 1
        t = t.replace(v, n)

    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("magicbox.js: familias francesas dentro")
    return 0


if __name__ == "__main__":
    sys.exit(main())
