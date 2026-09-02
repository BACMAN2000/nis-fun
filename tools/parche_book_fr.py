# -*- coding: utf-8 -*-
"""Ensena el frances al generador de los libros.

book.html es el mismo archivo para los dos idiomas, como el motor y como el
lector de cuentos: ?lang=fr cambia la carpeta de contenido y los rotulos.
Nada mas. Los dibujos, las escenas y la maqueta son los mismos.

Dos arreglos que no son de idioma pero salen aqui:

  * el nombre del dibujo del vocabulario se calculaba sobre la palabra tal
    cual, no sobre la clave inglesa: en frances pedia 'cerf-volant.png' y
    salia el respaldo plano. Es el mismo fallo que ya se corrigio en el
    motor, que en el libro seguia vivo.
  * y ese nombre tampoco quitaba los acentos.
"""
import io, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = r"C:\Projects\nis-fun\book-builder\book.html"

CAMBIOS = [
    # --- idioma ----------------------------------------------------------
    ("""const qs = new URLSearchParams(location.search);
const LEVEL = qs.get('level') || 'flyers';""",
     """const qs = new URLSearchParams(location.search);
/* Frances. Mismo archivo, misma maqueta, mismos dibujos: solo cambia de
   que carpeta sale el contenido y en que idioma van los rotulos. */
const LANG = qs.get('lang') === 'fr' ? 'fr' : 'en';
const CDIR = LANG === 'fr' ? '../content-fr' : '../content';
const T = (en, fr) => (LANG === 'fr' ? fr : en);
const LEVEL = qs.get('level') || 'flyers';"""),

    ("""  const idx = await j(`../content/${LEVEL}/index.json`);""",
     """  const idx = await j(`${CDIR}/${LEVEL}/index.json`);"""),
    ("""  for(const n of list) uds.push(await j(`../content/${LEVEL}/unit-${String(n).padStart(2,'0')}.json`));""",
     """  for(const n of list) uds.push(await j(`${CDIR}/${LEVEL}/unit-${String(n).padStart(2,'0')}.json`));"""),

    # --- el dibujo del vocabulario ---------------------------------------
    ("""    const s3d = key.toLowerCase().replace(/'/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');""",
     """    /* Sobre la clave inglesa y sin acentos, igual que en el motor:
       'cerf-volant' y 'kite' comparten kite.png, y 'geographie' no puede
       salir como 'g-ographie'. */
    const s3d = String((window.VOCAB_ART && VOCAB_ART.base(key)) || key)
      .normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')
      .toLowerCase().replace(/'/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');"""),

    # --- rotulos ---------------------------------------------------------
    ("""  return `<div class="xw">${g}<div class="clues"><h3>Across ➜</h3>${list('across')}<h3>Down ⬇</h3>${list('down')}</div></div>`;""",
     """  return `<div class="xw">${g}<div class="clues"><h3>${T('Across','Horizontal')} ➜</h3>${list('across')}<h3>${T('Down','Vertical')} ⬇</h3>${list('down')}</div></div>`;"""),

    ("""  return `${data.extra?'<div style="font-size:8.5pt;color:var(--soft);margin-bottom:1mm"><i>Careful — one answer is extra!</i></div>':''}""",
     """  return `${data.extra?`<div style="font-size:8.5pt;color:var(--soft);margin-bottom:1mm"><i>${T('Careful — one answer is extra!','Attention — il y a une réponse en trop !')}</i></div>`:''}"""),

    ("""  return `<div style="font-size:9pt;color:var(--soft);margin-bottom:1.5mm"><i>Find and circle the differences in picture B. Then tell your partner: "In A the ball is red, but in B it is blue."</i></div>""",
     """  return `<div style="font-size:9pt;color:var(--soft);margin-bottom:1.5mm"><i>${T('Find and circle the differences in picture B. Then tell your partner: "In A the ball is red, but in B it is blue."','Trouve et entoure les différences sur l\\'image B. Puis dis à ton camarade : « Sur A le ballon est rouge, mais sur B il est bleu. »')}</i></div>"""),

    ("""    <div><span style="font-family:'Baloo 2';font-weight:700;color:var(--soft);letter-spacing:.1em">NORDIC INTERNATIONAL SCHOOL · COHASSET</span>""",
     """    <div><span style="font-family:'Baloo 2';font-weight:700;color:var(--soft);letter-spacing:.1em">NORDIC INTERNATIONAL SCHOOL · COHASSET</span>"""),

    ("""  return `<div class="act"><h2><span class="abadge" style="background:var(--accent)">✎</span>Picture words — look, say and copy.</h2>""",
     """  return `<div class="act"><h2><span class="abadge" style="background:var(--accent)">✎</span>${T('Picture words — look, say and copy.','Les mots en images — regarde, dis et recopie.')}</h2>"""),

    ("""      body = `<span class="listenchip">🎧 Listen online — unit ${ud.number}</span>""",
     """      body = `<span class="listenchip">🎧 ${T(`Listen online — unit ${ud.number}`, `Écoute en ligne — unité ${ud.number}`)}</span>"""),

    ("""      <span class="focus">${ud.exam_focus.paper}<br>Part ${ud.exam_focus.part}</span></div>""",
     """      <span class="focus">${ud.exam_focus.paper}<br>${T('Part','partie')} ${ud.exam_focus.part}</span></div>"""),

    ("""    <div class="op-text"><b>📖 The story of this unit:</b> ${makeIntro(ud)}</div>""",
     """    <div class="op-text"><b>📖 ${T('The story of this unit:',"L'histoire de cette unité :")}</b> ${makeIntro(ud)}</div>"""),

    ("""    <div class="persbox"><b>All about me:</b> my two favourite words of this unit are <span></span> and <span></span>.</div>
    <div class="wordlist"><b>Wordlist:</b> ${ud.wordlist.join(' · ')} &nbsp;·&nbsp; <b>Grammar:</b> ${ud.grammar}</div>""",
     """    <div class="persbox"><b>${T('All about me:','Moi, c\\'est moi :')}</b> ${T('my two favourite words of this unit are','mes deux mots préférés de cette unité sont')} <span></span> ${T('and','et')} <span></span>.</div>
    <div class="wordlist"><b>${T('Wordlist:','Les mots :')}</b> ${ud.wordlist.join(' · ')} &nbsp;·&nbsp; <b>${T('Grammar:','Grammaire :')}</b> ${ud.grammar}</div>"""),

    ("""    <div class="band"><span class="n">${ud.number}</span><h1>${ud.title} · Homework</h1>
      <span class="focus">Fun for Nordic<br>Workbook</span></div>
    <div class="act"><h2><span class="code">1</span>My words — copy each word carefully.</h2>""",
     """    <div class="band"><span class="n">${ud.number}</span><h1>${ud.title} · ${T('Homework','Devoirs')}</h1>
      <span class="focus">Fun for Nordic<br>${T('Workbook',"Cahier d'exercices")}</span></div>
    <div class="act"><h2><span class="code">1</span>${T('My words — copy each word carefully.','Mes mots — recopie chaque mot avec soin.')}</h2>"""),

    ("""    <div class="act"><h2><span class="code">2</span>Homework task</h2>""",
     """    <div class="act"><h2><span class="code">2</span>${T('Homework task','Le travail à la maison')}</h2>"""),

    ("""    <div class="act"><h2><span class="code">3</span>Check yourself</h2>""",
     """    <div class="act"><h2><span class="code">3</span>${T('Check yourself','Vérifie toi-même')}</h2>"""),

    ("""        <span>I know the words of <b>${ud.topic}</b>.</span>
        <span>I can use: <b>${ud.grammar}</b>.</span>""",
     """        <span>${T(`I know the words of <b>${ud.topic}</b>.`, `Je connais les mots de <b>${ud.topic}</b>.`)}</span>
        <span>${T(`I can use: <b>${ud.grammar}</b>.`, `Je sais employer : <b>${ud.grammar}</b>.`)}</span>"""),

    ("""    <div class="wb-sign"><i>Student's signature</i><i>Family signature</i><i>Teacher's ✓</i></div>""",
     """    <div class="wb-sign"><i>${T("Student's signature","Signature de l'élève")}</i><i>${T('Family signature','Signature des parents')}</i><i>${T("Teacher's ✓",'Visa du professeur ✓')}</i></div>"""),

    ("""  const subtitle = MODE === 'wb' ? "Workbook" : MODE === 'key' ? "Teacher's Key" : "Student's Book";""",
     """  const subtitle = MODE === 'wb' ? T("Workbook", "Cahier d'exercices")
    : MODE === 'key' ? T("Teacher's Key", "Corrigé du professeur")
    : T("Student's Book", "Livre de l'élève");"""),

    ("""      `<div class="page"><div class="band"><h1>${idx.name} — Teacher's Key</h1></div>""",
     """      `<div class="page"><div class="band"><h1>${idx.name} — ${T("Teacher's Key","Corrigé du professeur")}</h1></div>"""),

    ("""  return `<div class="keyu"><h2>Unit ${ud.number} · ${ud.title}</h2>${parts.join('')}</div>`;""",
     """  return `<div class="keyu"><h2>${T('Unit','Unité')} ${ud.number} · ${ud.title}</h2>${parts.join('')}</div>`;"""),

    ("""<p class="credit">Written by Paolo Baca</p></div></div>`;""",
     """<p class="credit">${T('Written by','Texte de')} Paolo Baca</p></div></div>`;"""),

    ("""<div class="rtext">${data.text}<p class="credit">Written by Paolo Baca</p></div>`:''}""",
     """<div class="rtext">${data.text}<p class="credit">${T('Written by','Texte de')} Paolo Baca</p></div>`:''}"""),
]

# La historia de apertura cuando la unidad no trae la suya: la misma que en
# el motor, palabra por palabra, para que libro y pantalla digan lo mismo.
VIEJO_INTRO = """  if (LEVEL==='starters') return `Hello, explorers! Today ${c1} and ${c2} are playing with the world of ${ud.topic}. Look at the big pictures, say every new word out loud and listen to the story with your best ears. Pip is hiding somewhere in this unit too! When you finish all the games, you win a star. Ready, explorers? One, two, three… let's go!`;
  if (LEVEL==='movers') return `Welcome back, Fjord Club! In this unit, ${c1} and ${c2} discover the world of ${ud.topic}. First learn the picture words, then read carefully and listen to your friends — the answers are always hiding in the story. You will also practise ${ud.grammar}. Luna is watching and she only barks for good answers. The adventure starts now!`;
  return `The Aurora Expedition continues! This time, ${c1} and ${c2} take you deep into the world of ${ud.topic}. Read the texts slowly, listen twice like in the real exam, and use ${ud.grammar} like a true explorer. Every activity you finish takes you one step closer to the Flyers exam — and Kili is carrying a star with your name on it. Good luck, explorer!`;"""

NUEVO_INTRO = """  if (LEVEL==='starters') return T(`Hello, explorers! Today ${c1} and ${c2} are playing with the world of ${ud.topic}. Look at the big pictures, say every new word out loud and listen to the story with your best ears. Pip is hiding somewhere in this unit too! When you finish all the games, you win a star. Ready, explorers? One, two, three… let's go!`,
    `Bonjour, les explorateurs ! Aujourd'hui ${c1} et ${c2} jouent avec le monde de ${ud.topic}. Regarde bien les grandes images, dis chaque mot nouveau à voix haute et écoute l'histoire avec tes meilleures oreilles. Pip se cache quelque part dans cette unité aussi ! Quand tu finis tous les jeux, tu gagnes une étoile. Prêts, les explorateurs ? Un, deux, trois… c'est parti !`);
  if (LEVEL==='movers') return T(`Welcome back, Fjord Club! In this unit, ${c1} and ${c2} discover the world of ${ud.topic}. First learn the picture words, then read carefully and listen to your friends — the answers are always hiding in the story. You will also practise ${ud.grammar}. Luna is watching and she only barks for good answers. The adventure starts now!`,
    `Content de te revoir, Club du Fjord ! Dans cette unité, ${c1} et ${c2} découvrent le monde de ${ud.topic}. Apprends d'abord les mots en images, puis lis attentivement et écoute tes amis — les réponses se cachent toujours dans l'histoire. Tu vas aussi travailler ${ud.grammar}. Luna regarde, et elle n'aboie que pour les bonnes réponses. L'aventure commence !`);
  return T(`The Aurora Expedition continues! This time, ${c1} and ${c2} take you deep into the world of ${ud.topic}. Read the texts slowly, listen twice like in the real exam, and use ${ud.grammar} like a true explorer. Every activity you finish takes you one step closer to the Flyers exam — and Kili is carrying a star with your name on it. Good luck, explorer!`,
    `L'Expédition Aurore continue ! Cette fois, ${c1} et ${c2} t'emmènent au cœur du monde de ${ud.topic}. Lis les textes doucement, écoute deux fois comme au vrai examen, et sers-toi de ${ud.grammar} comme un vrai explorateur. Chaque activité terminée te rapproche de l'examen — et Kili porte une étoile avec ton nom dessus. Bonne chance, explorateur !`);"""


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    hechos = 0
    for v, n in CAMBIOS + [(VIEJO_INTRO, NUEVO_INTRO)]:
        if v == n or n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:75]))
            return 1
        t = t.replace(v, n)
        hechos += 1
    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("book.html: %d cambios" % hechos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
