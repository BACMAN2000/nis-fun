# -*- coding: utf-8 -*-
"""Ensena el frances al lector de cuentos.

Un solo index.html para los dos idiomas, como en el motor: ?lang=fr cambia
la carpeta de datos, la de audio, la voz del navegador y los textos de la
interfaz. Sin ?lang sigue siendo exactamente la pagina inglesa de siempre.

Se parchea por anclas, nunca reescribiendo el archivo entero: el lector
tiene arreglos que no estan en ninguna otra copia.
"""
import io, os, sys

P = r"C:\Projects\nis-portal\nis-fun\readers\index.html"
s = io.open(P, encoding="utf-8", newline="").read()
orig = s


def cambia(viejo, nuevo, veces=1):
    global s
    n = s.count(viejo)
    if n != veces:
        print(f"ANCLA FALLA ({n} de {veces}): {viejo[:70]!r}")
        sys.exit(1)
    s = s.replace(viejo, nuevo)


# --- idioma, carpetas y textos ------------------------------------------
cambia("""const app = document.getElementById('app');
const params = new URLSearchParams(location.search);
const ID = params.get('id');""",
       """const app = document.getElementById('app');
const params = new URLSearchParams(location.search);
const ID = params.get('id');

/* Frances. Misma pagina, mismos dibujos: solo cambia de donde salen los
   textos, de donde sale el audio y en que idioma lee la voz. */
const LANG = params.get('lang') === 'fr' ? 'fr' : 'en';
const DATA = LANG === 'fr' ? 'data-fr' : 'data';
const AUDIO = LANG === 'fr' ? 'audio-fr' : 'audio';
const T = (en, fr) => (LANG === 'fr' ? fr : en);
const Q = extra => (LANG === 'fr' ? (extra ? extra + '&lang=fr' : '?lang=fr') : (extra || './'));
if (LANG === 'fr'){
  document.documentElement.lang = 'fr';
  document.title = 'Petits Lecteurs Nordic';
  document.getElementById('tit').textContent = 'Petits Lecteurs Nordic';
  document.getElementById('volver').textContent = '\\u2039 La bibliothèque';
  document.getElementById('home').textContent = 'Accueil \\u203a';
  app.innerHTML = '<p class="muted">Chargement…</p>';
}
document.getElementById('volver').href = LANG === 'fr' ? './?lang=fr' : './';""")

# el boton Home tiene que conservar el idioma al volver al curso
cambia("document.getElementById('home').href = HOME;",
       """document.getElementById('home').href = (() => {
  if (new URLSearchParams(location.search).get('lang') !== 'fr') return HOME;
  try { const u = new URL(HOME, location.href); u.searchParams.set('lang', 'fr');
        return u.pathname + u.search + u.hash; } catch(e){ return HOME; }
})();""")

# --- audio: carpeta propia y slug sin tildes ----------------------------
cambia("""  const slug = texto.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,60);
  // con version, para que un 404 guardado de antes no sobreviva
  const a = new Audio(`audio/${slug}.mp3?v=2026-08-27`);""",
       """  // sin tildes: "poupée" y "poupee" tienen que ser el mismo archivo
  const slug = texto.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')
    .toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,60);
  // con version, para que un 404 guardado de antes no sobreviva
  const a = new Audio(`${AUDIO}/${slug}.mp3?v=2026-08-27`);""")

cambia("""    const u = new SpeechSynthesisUtterance(t);
    u.lang = 'en-GB'; u.rate = 0.78;
    const gb = speechSynthesis.getVoices().find(v=>/en[-_]GB/i.test(v.lang));
    if (gb) u.voice = gb;""",
       """    const u = new SpeechSynthesisUtterance(t);
    u.lang = LANG === 'fr' ? 'fr-FR' : 'en-GB'; u.rate = 0.78;
    const re = LANG === 'fr' ? /fr[-_]FR/i : /en[-_]GB/i;
    const v = speechSynthesis.getVoices().find(x=>re.test(x.lang));
    if (v) u.voice = v;""")

# --- la estanteria ------------------------------------------------------
cambia("""  const r = await fetch('data/index.json', {cache: 'no-cache'});
  if (!r.ok){ app.innerHTML = '<p class="muted">No encuentro los cuentos.</p>'; return; }""",
       """  const r = await fetch(`${DATA}/index.json`, {cache: 'no-cache'});
  if (!r.ok){ app.innerHTML = `<p class="muted">${T('The stories are not here.','Les histoires ne sont pas là.')}</p>`; return; }""")

cambia("""      <a class="libro" href="?id=${esc(l.id)}">""",
       """      <a class="libro" href="${Q('?id=' + esc(l.id))}">""")

cambia("""          <div class="meta">${l.paginas} pages</div>""",
       """          <div class="meta">${l.paginas} ${T('pages','pages')}</div>""")

# --- un cuento ----------------------------------------------------------
cambia("""  const r = await fetch(`data/${id}.json`, {cache: 'no-cache'});
  if (!r.ok){ app.innerHTML = '<p class="muted">No encuentro ese cuento.</p>'; return; }""",
       """  const r = await fetch(`${DATA}/${id}.json`, {cache: 'no-cache'});
  if (!r.ok){ app.innerHTML = `<p class="muted">${T('I cannot find that story.','Je ne trouve pas cette histoire.')}</p>`; return; }""")

cambia("""  document.title = d.titulo + ' · Nordic Little Readers';""",
       """  document.title = d.titulo + T(' · Nordic Little Readers', ' · Petits Lecteurs Nordic');""")

cambia("""      <button class="nav" id="atras" ${i===0?'disabled':''}>‹ Back</button>
      <button class="nav" id="alante" ${i>=total-1?'disabled':''}>${i===d.paginas.length-1?'Activity':'Next'} ›</button>""",
       """      <button class="nav" id="atras" ${i===0?'disabled':''}>‹ ${T('Back','Retour')}</button>
      <button class="nav" id="alante" ${i>=total-1?'disabled':''}>${i===d.paginas.length-1?T('Activity','Activité'):T('Next','Suivant')} ›</button>""")

cambia("""          <button class="oir" id="oir">🔊 Listen</button>""",
       """          <button class="oir" id="oir">🔊 ${T('Listen','Écoute')}</button>""")

cambia("""      <h2>${esc(act.titulo || 'Match the words')}</h2>
      <p class="muted">${esc(act.instruccion || 'Tap the picture for each word.')}</p>""",
       """      <h2>${esc(act.titulo || T('Match the words','Associe les mots'))}</h2>
      <p class="muted">${esc(act.instruccion || T('Tap the picture for each word.','Touche l\\'image de chaque mot.'))}</p>""")

cambia("""      pide.innerHTML = '<span class="listo">Well done! ⭐</span>';""",
       """      pide.innerHTML = `<span class="listo">${T('Well done!','Bravo !')} ⭐</span>`;""")

cambia("""  app.innerHTML = '<p class="muted">Something went wrong loading the reader.</p>';""",
       """  app.innerHTML = `<p class="muted">${T('Something went wrong loading the reader.','Une erreur est survenue au chargement.')}</p>`;""")

if s == orig:
    print("nada que cambiar")
    sys.exit(1)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print(f"lector parcheado: {len(orig)} -> {len(s)} bytes")
