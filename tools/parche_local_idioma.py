# -*- coding: utf-8 -*-
"""Las marcas locales del navegador llevan idioma.

Las entregas ya se separaban por idioma en la base (columna `lang`), pero lo
que el motor guarda en el navegador NO: las cuatro claves eran las mismas
para el curso ingles y el frances.

Lo que se veia: el alumno que ya habia visto la presentacion inglesa entraba
al curso frances directo a la lista de unidades, y no llegaba a ver nunca su
mascota ni a su equipo — de ahi el "no aparecen los videos". Y ademas veia
sus estrellas inglesas puestas en las unidades francesas.

  nisfun-<nivel>-u<n>          lo hecho en cada unidad
  nisfun-<nivel>-lastUnit      por donde iba
  nisfun-<nivel>-intro-seen    si ya vio la presentacion  <- el del video
  nisfun-sc-<nivel>-u<n>       el autoexamen

El ingles conserva su prefijo de siempre a proposito: cambiarselo borraria
de un plumazo el avance de todos los que ya estan en el curso. El frances
estrena `nisfun-fr-`.
"""
import io, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = r"C:\Projects\nis-portal\nis-fun\engine\index.html"

CAMBIOS = [
    ("""const store = {
  key: (u)=>`nisfun-${LEVEL}-u${u}`,""",
     """/* Prefijo de lo que se guarda en el navegador. Lleva el idioma porque el
   curso frances es otro curso: sus unidades hechas, su ultima unidad y su
   presentacion no son las del ingles. El ingles se queda con el prefijo de
   siempre — cambiarselo borraria el avance de quien ya esta dentro. */
const LPFX = LANG === 'fr' ? 'nisfun-fr' : 'nisfun';
const store = {
  key: (u)=>`${LPFX}-${LEVEL}-u${u}`,"""),

    ("""  const ultima = Number(localStorage.getItem(`nisfun-${LEVEL}-lastUnit`));""",
     """  const ultima = Number(localStorage.getItem(`${LPFX}-${LEVEL}-lastUnit`));"""),

    ("""  const introKey = `nisfun-${LEVEL}-intro-seen`;""",
     """  const introKey = `${LPFX}-${LEVEL}-intro-seen`;"""),

    ("""  try { localStorage.setItem(`nisfun-${LEVEL}-lastUnit`, String(UNIT)); } catch(e) {}""",
     """  try { localStorage.setItem(`${LPFX}-${LEVEL}-lastUnit`, String(UNIT)); } catch(e) {}"""),

    ("""  const clave = `nisfun-sc-${LEVEL}-u${UD.number}`;""",
     """  const clave = `${LPFX}-sc-${LEVEL}-u${UD.number}`;"""),
]


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    n = 0
    for v, x in CAMBIOS:
        if x in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:70]))
            return 1
        t = t.replace(v, x)
        n += 1
    if "nisfun-${LEVEL}" in t or "nisfun-sc-${LEVEL}" in t:
        print("queda alguna clave sin prefijo")
        return 1
    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("index.html: %d claves locales con idioma" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
