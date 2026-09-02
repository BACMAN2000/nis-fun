# -*- coding: utf-8 -*-
"""Lo que quedaba del motor en ingles: los rotulos con escape y plantilla.

La auditoria vieja no los veia porque no sabia leer una cadena de
JavaScript: 'Let\\'s look at the answers' lleva una comilla escapada dentro
y `${quedan} more tries` es una plantilla. La nueva si, y estos son los que
saco.

Van juntos porque son del mismo sitio: la barra del reproductor de la
historia, el marcador de las actividades de escribir, la lista de "lo que
ya se hacer" y la presentacion de cada mascota.
"""
import io, sys

P = r"C:\Projects\nis-portal\nis-fun\engine\index.html"

CAMBIOS = [
    # --- la portada del nivel y el campus --------------------------------
    ('''<img src="../assets/scenes/main-building.jpg?v=${ART_V}" alt="Nordic campus">''',
     '''<img src="../assets/scenes/main-building.jpg?v=${ART_V}" alt="${T('Nordic campus','Le campus Nordic')}">'''),
    ('''<section class="course-status" aria-label="Course progress">''',
     '''<section class="course-status" aria-label="${T('Course progress','Progression du cours')}">'''),
    ('''<div class="course-meter" role="progressbar" aria-label="Overall course progress"''',
     '''<div class="course-meter" role="progressbar" aria-label="${T('Overall course progress','Progression générale du cours')}"'''),
    ("""      ? `Units ${tanda[0].n}–${tanda[tanda.length-1].n}`""",
     """      ? T(`Units ${tanda[0].n}–${tanda[tanda.length-1].n}`, `Unités ${tanda[0].n}–${tanda[tanda.length-1].n}`)"""),

    # --- las mascotas se presentan ---------------------------------------
    ("""  pip:  { que:'a little puffin', dice:"I live on the rocks by the lighthouse. I am very shy, "
          + "so I hide in every picture — can you find me?" },
  luna: { que:'a husky', dice:"I love the snow and I remember everything that happened. "
          + "I will tell you the stories!" },
  kili: { que:'an Andean condor', dice:"I am the postman of the school. I bring letters and "
          + "postcards from far away — but I am not very good at landing!" },""",
     """  pip:  { que: T('a little puffin', 'un petit macareux'),
          dice: T("I live on the rocks by the lighthouse. I am very shy, "
                  + "so I hide in every picture — can you find me?",
                  "J'habite sur les rochers, près du phare. Je suis très timide, "
                  + "alors je me cache dans chaque image — tu me trouves ?") },
  luna: { que: T('a husky', 'une husky'),
          dice: T("I love the snow and I remember everything that happened. "
                  + "I will tell you the stories!",
                  "J'adore la neige et je me souviens de tout ce qui s'est passé. "
                  + "C'est moi qui vais te raconter les histoires !") },
  kili: { que: T('an Andean condor', 'un condor des Andes'),
          dice: T("I am the postman of the school. I bring letters and "
                  + "postcards from far away — but I am not very good at landing!",
                  "Je suis le facteur de l'école. J'apporte des lettres et des "
                  + "cartes postales de très loin — mais je me pose très mal !") },"""),

    # --- la historia de apertura, cuando la unidad no trae la suya --------
    ("""  if (LEVEL==='starters') return `Hello, explorers! Today ${c1} and ${c2} are playing with the world of ${ud.topic}. Look at the big pictures, say every new word out loud and listen to the story with your best ears. Pip is hiding somewhere in this unit too! When you finish all the games, you win a star. Ready, explorers? One, two, three… let's go!`;
  if (LEVEL==='movers') return `Welcome back, Fjord Club! In this unit, ${c1} and ${c2} discover the world of ${ud.topic}. First learn the picture words, then read carefully and listen to your friends — the answers are always hiding in the story. You will also practise ${ud.grammar}. Luna is watching and she only barks for good answers. The adventure starts now!`;
  return `The Aurora Expedition continues! This time, ${c1} and ${c2} take you deep into the world of ${ud.topic}. Read the texts slowly, listen twice like in the real exam, and use ${ud.grammar} like a true explorer. Every activity you finish takes you one step closer to the Flyers exam — and Kili is carrying a star with your name on it. Good luck, explorer!`;""",
     """  if (LEVEL==='starters') return T(`Hello, explorers! Today ${c1} and ${c2} are playing with the world of ${ud.topic}. Look at the big pictures, say every new word out loud and listen to the story with your best ears. Pip is hiding somewhere in this unit too! When you finish all the games, you win a star. Ready, explorers? One, two, three… let's go!`,
    `Bonjour, les explorateurs ! Aujourd'hui ${c1} et ${c2} jouent avec le monde de ${ud.topic}. Regarde bien les grandes images, dis chaque mot nouveau à voix haute et écoute l'histoire avec tes meilleures oreilles. Pip se cache quelque part dans cette unité aussi ! Quand tu finis tous les jeux, tu gagnes une étoile. Prêts, les explorateurs ? Un, deux, trois… c'est parti !`);
  if (LEVEL==='movers') return T(`Welcome back, Fjord Club! In this unit, ${c1} and ${c2} discover the world of ${ud.topic}. First learn the picture words, then read carefully and listen to your friends — the answers are always hiding in the story. You will also practise ${ud.grammar}. Luna is watching and she only barks for good answers. The adventure starts now!`,
    `Content de te revoir, Club du Fjord ! Dans cette unité, ${c1} et ${c2} découvrent le monde de ${ud.topic}. Apprends d'abord les mots en images, puis lis attentivement et écoute tes amis — les réponses se cachent toujours dans l'histoire. Tu vas aussi travailler ${ud.grammar}. Luna regarde, et elle n'aboie que pour les bonnes réponses. L'aventure commence !`);
  return T(`The Aurora Expedition continues! This time, ${c1} and ${c2} take you deep into the world of ${ud.topic}. Read the texts slowly, listen twice like in the real exam, and use ${ud.grammar} like a true explorer. Every activity you finish takes you one step closer to the Flyers exam — and Kili is carrying a star with your name on it. Good luck, explorer!`,
    `L'Expédition Aurore continue ! Cette fois, ${c1} et ${c2} t'emmènent au cœur du monde de ${ud.topic}. Lis les textes doucement, écoute deux fois comme au vrai examen, et sers-toi de ${ud.grammar} comme un vrai explorateur. Chaque activité terminée te rapproche de l'examen — et Kili porte une étoile avec ton nom dessus. Bonne chance, explorateur !`);"""),

    # --- el reproductor de la historia -----------------------------------
    ('''       title="Listen to this part again">${marcaClaves(f, UD.wordlist, vistasClave)}</span>`''',
     '''       title="${T('Listen to this part again','Réécoute ce passage')}">${marcaClaves(f, UD.wordlist, vistasClave)}</span>`'''),
    ('''              <button class="sp-b sp-main sp-play" type="button">&#9654; Play</button>
              <button class="sp-b sp-stop" type="button">&#9209; Stop</button>
              <button class="sp-b sp-prev" type="button" aria-label="Previous part">&#9198; Back</button>
              <button class="sp-b sp-again" type="button" aria-label="Hear this part again">&#128257; Again</button>
              <button class="sp-b sp-next" type="button" aria-label="Next part">&#9197; Next</button>
              <button class="sp-b sp-slow" type="button" aria-pressed="false">&#128034; Slow</button>''',
     '''              <button class="sp-b sp-main sp-play" type="button">&#9654; ${T('Play','Lire')}</button>
              <button class="sp-b sp-stop" type="button">&#9209; ${T('Stop','Arrêter')}</button>
              <button class="sp-b sp-prev" type="button" aria-label="${T('Previous part','Passage précédent')}">&#9198; ${T('Back','Retour')}</button>
              <button class="sp-b sp-again" type="button" aria-label="${T('Hear this part again','Réécoute ce passage')}">&#128257; ${T('Again','Encore')}</button>
              <button class="sp-b sp-next" type="button" aria-label="${T('Next part','Passage suivant')}">&#9197; ${T('Next','Suivant')}</button>
              <button class="sp-b sp-slow" type="button" aria-pressed="false">&#128034; ${T('Slow','Lent')}</button>'''),
    ("""    parte.textContent = 'Part ' + (i+1) + ' of ' + frases.length;""",
     """    parte.textContent = T('Part ', 'Passage ') + (i+1) + T(' of ', ' sur ') + frases.length;"""),

    # --- "lo que ya se hacer" --------------------------------------------
    ("""    `I can say and write the new words: ${(UD.wordlist||[]).slice(0,6).join(', ')}…`,
    UD.grammar ? `I can use <b>${UD.grammar}</b>.` : null,
    `I can understand the story of this unit.`,""",
     """    T(`I can say and write the new words: ${(UD.wordlist||[]).slice(0,6).join(', ')}…`,
      `Je sais dire et écrire les mots nouveaux : ${(UD.wordlist||[]).slice(0,6).join(', ')}…`),
    UD.grammar ? T(`I can use <b>${UD.grammar}</b>.`, `Je sais employer <b>${UD.grammar}</b>.`) : null,
    T(`I can understand the story of this unit.`, `Je comprends l'histoire de cette unité.`),"""),

    # --- el ciclo de intentos --------------------------------------------
    ("""      cuenta.textContent = quedan === 1 ? 'one more try' : `${quedan} more tries`;""",
     """      cuenta.textContent = quedan === 1 ? T('one more try','encore un essai')
        : T(`${quedan} more tries`, `encore ${quedan} essais`);"""),
    ("""      cuenta.textContent = 'Let\\'s look at the answers together.';""",
     """      cuenta.textContent = T("Let's look at the answers together.",
                             'Regardons les réponses ensemble.');"""),

    # --- la celebracion ---------------------------------------------------
    ("""    ? `You have finished Unit ${UD.number}! ⭐⭐⭐⭐`
    : msg || `Activity complete! (${done}/${total})`;""",
     """    ? T(`You have finished Unit ${UD.number}! ⭐⭐⭐⭐`, `Tu as fini l'unité ${UD.number} ! ⭐⭐⭐⭐`)
    : msg || T(`Activity complete! (${done}/${total})`, `Activité terminée ! (${done}/${total})`);"""),

    # --- escribir ---------------------------------------------------------
    ("""    cnt.textContent = `${n} word${n === 1 ? '' : 's'}` +
      (n < min ? ` — ${min - n} more to go` : (n > max ? ` — ${n - max} too many` : ' — just right'));""",
     """    cnt.textContent = T(`${n} word${n === 1 ? '' : 's'}`, `${n} mot${n === 1 ? '' : 's'}`) +
      (n < min ? T(` — ${min - n} more to go`, ` — encore ${min - n}`)
               : (n > max ? T(` — ${n - max} too many`, ` — ${n - max} de trop`)
                          : T(' — just right', ' — parfait')));"""),
    ('''        aria-label="Your story"></textarea>''',
     '''        aria-label="${T('Your story','Ton histoire')}"></textarea>'''),
    ("""    if (!n){ s.textContent = 'Write your story first.'; s.className = 'score partial'; return; }""",
     """    if (!n){ s.textContent = T('Write your story first.',"Écris ton histoire d'abord."); s.className = 'score partial'; return; }"""),
    ("""    s.textContent = n >= min && n <= max ? 'Sent to your teacher ✓'
                                         : `Sent — but it is ${n} words, not ${min}-${max}.`;""",
     """    s.textContent = n >= min && n <= max ? T('Sent to your teacher ✓','Envoyé à ton professeur ✓')
                                         : T(`Sent — but it is ${n} words, not ${min}-${max}.`,
                                             `Envoyé — mais ça fait ${n} mots, pas ${min}-${max}.`);"""),

    # --- marcadores -------------------------------------------------------
    ("""      s.textContent = 'All correct!'; s.className = 'score good';""",
     """      s.textContent = T('All correct!','Tout est juste !'); s.className = 'score good';"""),
    ("""    s.textContent = `${ok} / ${tot} letters`;""",
     """    s.textContent = T(`${ok} / ${tot} letters`, `${ok} / ${tot} lettres`);"""),
    ("""  if(k.examen_parte) partes.push(`${k.examen} · ${k.examen_parte.paper} Part ${k.examen_parte.part}`);
  if(k.tema && k.tema.nombre) partes.push(`${k.grado} · Unit ${k.tema.n}: ${k.tema.nombre}`);""",
     """  if(k.examen_parte) partes.push(T(`${k.examen} · ${k.examen_parte.paper} Part ${k.examen_parte.part}`,
                                   `${k.examen} · ${k.examen_parte.paper} partie ${k.examen_parte.part}`));
  if(k.tema && k.tema.nombre) partes.push(T(`${k.grado} · Unit ${k.tema.n}: ${k.tema.nombre}`,
                                            `${k.grado} · Unité ${k.tema.n} : ${k.tema.nombre}`));"""),
    ('''          <span class="meta">${UD.exam_focus.paper} · Part ${UD.exam_focus.part}</span></div>''',
     '''          <span class="meta">${UD.exam_focus.paper} · ${T('Part','partie')} ${UD.exam_focus.part}</span></div>'''),

    # --- los dos reproductores de audio de actividad ----------------------
    ("""  caja.innerHTML = `<button class="play" type="button">▶ Play</button>
    <button class="stop" type="button" disabled>⏹ Stop</button>""",
     """  caja.innerHTML = `<button class="play" type="button">▶ ${T('Play','Lire')}</button>
    <button class="stop" type="button" disabled>⏹ ${T('Stop','Arrêter')}</button>"""),
    ("""    bPlay.textContent = son ? '▶ Playing…' : '▶ Play'; bPlay.disabled = son; };""",
     """    bPlay.textContent = son ? T('▶ Playing…','▶ Lecture…') : T('▶ Play','▶ Lire'); bPlay.disabled = son; };"""),
    ("""      <button class="play" type="button">▶ Play</button>
      <button class="pause" type="button" disabled>⏸ Pause</button>
      <button class="stop" type="button" disabled>⏹ Stop</button>""",
     """      <button class="play" type="button">▶ ${T('Play','Lire')}</button>
      <button class="pause" type="button" disabled>⏸ ${T('Pause','Pause')}</button>
      <button class="stop" type="button" disabled>⏹ ${T('Stop','Arrêter')}</button>"""),
    ("""    bPlay.textContent = sonando ? '▶ Playing…' : '▶ Play';""",
     """    bPlay.textContent = sonando ? T('▶ Playing…','▶ Lecture…') : T('▶ Play','▶ Lire');"""),

    # --- el error de carga -------------------------------------------------
    ("""app.textContent = 'Error loading content: '+e.message;""",
     """app.textContent = T('Error loading content: ',"Erreur au chargement du contenu : ")+e.message;"""),
]


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")
    hechos = 0
    for v, n in CAMBIOS:
        if n in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:80]))
            return 1
        t = t.replace(v, n)
        hechos += 1
    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("index.html: %d rotulos traducidos" % hechos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
