# -*- coding: utf-8 -*-
"""Los ultimos nueve rotulos de index.html.

Los saco la auditoria cuando aprendio a mirar POR SITIO en vez de por
cadena: que 'Listen' estuviera traducido en un boton no queria decir que lo
estuviera en los otros tres, y no lo estaba.
"""
import io, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = r"C:\Projects\nis-portal\nis-fun\engine\index.html"

CAMBIOS = [
    # el boton de la mascota: el rotulo por defecto y las dos llamadas que
    # se lo pasaban en ingles
    ("""      <button class="guia-say" type="button">🔊 ${etiqueta || 'Listen'}</button>""",
     """      <button class="guia-say" type="button">🔊 ${etiqueta || T('Listen','Écoute')}</button>"""),
    ("""      ${guiaHTML(a.instructions || a.title, 'Listen')}""",
     """      ${guiaHTML(a.instructions || a.title, T('Listen','Écoute'))}"""),

    ("""          <span class="lvplaying"><span class="lvpulse"></span> Adventure playing</span>""",
     """          <span class="lvplaying"><span class="lvpulse"></span> ${T('Adventure playing',"L'aventure est en cours")}</span>"""),

    ("""        ${DEMO ? `<div class="demoflag">Demonstration — this preview covers the first two units.
           The full course has ${idx.units.length} units.</div>` : ''}""",
     """        ${DEMO ? `<div class="demoflag">${T(`Demonstration — this preview covers the first two units. The full course has ${idx.units.length} units.`,
           `Démonstration — cet aperçu ne montre que les deux premières unités. Le cours complet en a ${idx.units.length}.`)}</div>` : ''}"""),

    ("""      : 'Units',""",
     """      : T('Units','Les unités'),"""),

    ("""      <p class="sc-nota">This unit is part of what you will be able to do
        by the end of the year:</p>""",
     """      <p class="sc-nota">${T('This unit is part of what you will be able to do by the end of the year:',
        "Cette unité fait partie de ce que tu sauras faire à la fin de l'année :")}</p>"""),

    ("""  el.innerHTML = `${act.data.extra?`<p style="margin-top:0"><i>Careful — one answer is extra and matches nothing!</i></p>`:''}""",
     """  el.innerHTML = `${act.data.extra?`<p style="margin-top:0"><i>${T('Careful — one answer is extra and matches nothing!','Attention — il y a une réponse en trop, elle ne va avec rien !')}</i></p>`:''}"""),

    # el credito del texto: es un nombre, pero "Written by" no
    ("""<p class="credit">Written by Paolo Baca</p>""",
     """<p class="credit">${T('Written by','Texte de')} Paolo Baca</p>"""),

    # los dos reproductores que quedaban con el rotulo suelto
    ("""      <button class="pause" type="button" disabled>⏸ ${T('Pause','Pause')}</button>""",
     """      <button class="pause" type="button" disabled>⏸ ${T('Pause','Pause')}</button>"""),
]


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    hechos = 0
    for v, n in CAMBIOS:
        if v == n or n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:75]))
            return 1
        t = t.replace(v, n)
        hechos += 1
    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("index.html: %d rotulos mas" % hechos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
