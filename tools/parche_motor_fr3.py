# -*- coding: utf-8 -*-
"""Los tres rotulos que ya estan escritos en el HTML antes de correr nada.

El splash tiene que decir algo mientras carga el motor, asi que su texto va
en el propio HTML y no puede salir de T(). Se reescriben al arrancar; lo que
cambia aqui es que se hace en un solo sitio y con T(), para que la auditoria
los vea traducidos en vez de darlos por ingleses.
"""
import io, sys

P = r"C:\Projects\nis-portal\nis-fun\engine\index.html"

VIEJO_HTML = """  <div><span aria-hidden="true"></span><strong>Preparing your course…</strong>"""
NUEVO_HTML = """  <div><span aria-hidden="true"></span><strong id="splash-h2">Preparing your course…</strong>"""

VIEJO_JS = """if (LANG === 'fr') { const h = document.getElementById('cele-h2'); if (h) h.textContent = 'Bravo !'; }
if (LANG === 'fr') {
  const sp = document.getElementById('splash-sub');
  if (sp) sp.textContent = 'Chargement des activités et des illustrations.';
  const t = document.querySelector('#splash h2, .splash h2, #splash strong');
  if (t && /Preparing/i.test(t.textContent)) t.textContent = 'Préparation du cours…';
}"""

NUEVO_JS = """/* Los rotulos que van escritos en el HTML: el splash tiene que decir algo
   mientras carga el motor, asi que no pueden nacer de T(). Se reescriben
   aqui, los tres juntos, para que se traduzcan en un solo sitio. */
[['splash-h2',  T('Preparing your course…', 'Préparation du cours…')],
 ['splash-sub', T('Loading activities and illustrations.', 'Chargement des activités et des illustrations.')],
 ['cele-h2',    T('Well done!', 'Bravo !')]].forEach(([id, txt]) => {
  const el = document.getElementById(id);
  if (el) el.textContent = txt;
});"""


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    for v, n in ((VIEJO_HTML, NUEVO_HTML), (VIEJO_JS, NUEVO_JS)):
        if n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:70]))
            return 1
        t = t.replace(v, n)
    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("splash y celebracion: traducidos en un solo sitio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
