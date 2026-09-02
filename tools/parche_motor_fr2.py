# -*- coding: utf-8 -*-
"""Los rotulos del motor que quedaban en ingles con ?lang=fr.

Son los de las actividades que el motor arma solo —las diferencias, la caja
magica, el crucigrama, el "ensena la respuesta"— y que por eso no viven en
content-fr: los escribe el propio index.html.

Una nota sobre el nombre del colegio: "Nordic International School" no se
traduce. Es como se llama, y en la web francesa del colegio tambien.
"""
import io, sys

P = r"C:\Projects\nis-portal\nis-fun\engine\index.html"

CAMBIOS = [
    ("""          <button class="guia-say historia-say" type="button">🔊 Listen to the story</button>""",
     """          <button class="guia-say historia-say" type="button">🔊 ${T('Listen to the story',"Écoute l'histoire")}</button>"""),

    ("""          ${guiaHTML('Look at my magic box. Watch what happens to the word!', 'Listen')}""",
     """          ${guiaHTML(T('Look at my magic box. Watch what happens to the word!','Regarde ma boîte magique. Observe ce qui arrive au mot !'), T('Listen','Écoute'))}"""),

    ("""    <p class="sc-intro">Tick the things you can do. Be honest — it helps your teacher.</p>""",
     """    <p class="sc-intro">${T('Tick the things you can do. Be honest — it helps your teacher.','Coche ce que tu sais faire. Sois honnête — ça aide ton professeur.')}</p>"""),

    ("""    <p class="vis-sitio">Everybody is in ${esc(d.place || 'the picture')}.</p>""",
     """    <p class="vis-sitio">${T('Everybody is in','Tout le monde est')} ${esc(d.place || T('the picture',"sur l'image"))}.</p>"""),

    ("""      <button class="reveal" type="button">👁 See one possible story</button>""",
     """      <button class="reveal" type="button">👁 ${T('See one possible story','Voir une histoire possible')}</button>"""),

    ("""    caja.innerHTML = `<b>One way of telling it:</b><br>${esc(d.model)}`;""",
     """    caja.innerHTML = `<b>${T('One way of telling it:','Une façon de la raconter :')}</b><br>${esc(d.model)}`;"""),

    ("""        title="Listen to the clue" aria-label="Listen to clue ${n}">🔊</button>""",
     """        title="${T('Listen to the clue',"Écoute la définition")}" aria-label="${T('Listen to clue',"Écoute la définition")} ${n}">🔊</button>"""),

    ("""      <p style="margin-top:0"><i>Look at picture A and picture B.
        Find and TAP the differences in picture B — there are ${zonas.length}!
        Then tell your partner: <b>"In A the ball is red, but in B it is blue."</b></i></p>""",
     """      <p style="margin-top:0"><i>${T('Look at picture A and picture B.','Regarde l\\'image A et l\\'image B.')}
        ${T('Find and TAP the differences in picture B — there are','Trouve et TOUCHE les différences sur l\\'image B — il y en a')} ${zonas.length}!
        ${T('Then tell your partner:','Puis dis à ton camarade :')} <b>"${T('In A the ball is red, but in B it is blue.','Sur A le ballon est rouge, mais sur B il est bleu.')}"</b></i></p>"""),

    ("""    if (!d.sceneA) { el.innerHTML = '<p><i>Coming soon.</i></p>'; return; }""",
     """    if (!d.sceneA) { el.innerHTML = `<p><i>${T('Coming soon.','Bientôt disponible.')}</i></p>`; return; }"""),

    ("""    el.innerHTML = `<p style="margin-top:0"><i>Look at picture A. Find and TAP the ${d.diffs.length} differences in picture B!</i></p>""",
     """    el.innerHTML = `<p style="margin-top:0"><i>${T('Look at picture A. Find and TAP the','Regarde l\\'image A. Trouve et TOUCHE les')} ${d.diffs.length} ${T('differences in picture B!','différences sur l\\'image B !')}</i></p>"""),

    ("""        <p class="scr-pie">Looking for stories…</p></div></div>`,""",
     """        <p class="scr-pie">${T('Looking for stories…','Recherche des histoires…')}</p></div></div>`,"""),
]

# "👁 See the answers" sale cinco veces, todas iguales
GLOBAL = [("""<button class="reveal" type="button" hidden>👁 See the answers</button>""",
           """<button class="reveal" type="button" hidden>👁 ${T('See the answers','Voir les réponses')}</button>""")]


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    hechos = 0
    for v, n in CAMBIOS:
        if n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:70]))
            return 1
        t = t.replace(v, n)
        hechos += 1
    for v, n in GLOBAL:
        c = t.count(v)
        if c:
            t = t.replace(v, n)
            hechos += c
    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("motor: %d rotulos traducidos" % hechos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
