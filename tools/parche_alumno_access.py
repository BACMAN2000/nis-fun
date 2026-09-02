# -*- coding: utf-8 -*-
"""La tarjeta del alumno ofrece solo lo que su grado puede abrir.

Las dos tarjetas -la inglesa y la francesa- ofrecian los tres niveles a
todos los de primaria. Ahora preguntan a fun_access. Si el idioma no tiene
ninguna regla escrita, siguen ofreciendo los tres: sin reglas no se cierra
nada, que es la misma promesa que hace el panel.

La inglesa se vuelve asincrona por eso, igual que ya lo era la francesa.
"""
import io, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

P = r"C:\Projects\nis-portal\app.js"

VIEJO = """  const yle = stage==='primary' ? `
    <div class="card" style="margin-top:16px;border-top:5px solid #3b6fb5">
      <h2 style="margin:0 0 4px;color:var(--blue-d)">🧭 Fun for Nordic — Cambridge YLE</h2>
      <div class="muted" style="font-size:.9rem;margin-bottom:12px">Interactive course to get ready for the Cambridge Young Learners exams: 150 units with audio, crosswords and exam tasks — with Pip, Luna and Kili!</div>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <a href="${_withBack('nis-fun/engine/?level=starters','classes_primary')}" target="_blank" rel="noopener" class="btn" style="background:#d97d0d;color:#fff;text-decoration:none">🐧 Pre A1 · Starters</a>
        <a href="${_withBack('nis-fun/engine/?level=movers','classes_primary')}" target="_blank" rel="noopener" class="btn" style="background:#2f9268;color:#fff;text-decoration:none">🐺 A1 · Movers</a>
        <a href="${_withBack('nis-fun/engine/?level=flyers','classes_primary')}" target="_blank" rel="noopener" class="btn" style="background:#3b6fb5;color:#fff;text-decoration:none">🦅 A2 · Flyers</a>
      </div>
      <div class="muted" style="font-size:.85rem;margin:14px 0 6px">📚 Your books to print:</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">${
        ['starters','movers','flyers'].map(n => funLibros(n, 'en', false)).join('')
      }</div>
    </div>` : '';"""

NUEVO = """  /* La tarjeta se rellena despues, cuando fun_access conteste: los niveles
     que ofrece dependen del grado del alumno. Mientras tanto queda el hueco,
     que es medio segundo y no parpadea. */
  const yle = stage==='primary' ? '<div id="yle-card"></div>' : '';"""

ANCLA_RELLENO = """  if (stage==='primary') frIndice().then(idx => {"""

RELLENO = """  if (stage==='primary') _pintaYle();
  if (stage==='primary') frIndice().then(idx => {"""

# la funcion que la pinta, justo antes de studentResults
ANCLA_FN = """/* ---------- My Progress: historial completo del alumno (mocks, practice y actividades) ---------- */"""

FN = """/* La tarjeta inglesa de Fun for Nordic, con los niveles que le tocan a este
   grado. Sin reglas en fun_access se ofrecen los tres, como siempre. */
const _YLE_BOT = {
  starters: {c:'#d97d0d', t:'🐧 Pre A1 · Starters'},
  movers:   {c:'#2f9268', t:'🐺 A1 · Movers'},
  flyers:   {c:'#3b6fb5', t:'🦅 A2 · Flyers'},
};
async function _pintaYle(){
  const caja = document.getElementById('yle-card');
  if (!caja) return;
  const grado = (state.profile && state.profile.grade_id) || 0;
  const permiso = await funAccessDeGrado(grado, 'en');
  const niveles = permiso === null ? ['starters','movers','flyers']
                                   : permiso.map(f => f.level);
  if (!niveles.length) return;            // este grado no hace el curso
  const rango = n => {
    const f = permiso && permiso.find(x => x.level === n);
    return f ? `<small class="muted" style="display:block">Units ${f.desde}–${f.hasta}</small>` : '';
  };
  const botones = niveles.map(n => `<a href="${_withBack('nis-fun/engine/?level='+n,'classes_primary')}"
      target="_blank" rel="noopener" class="btn"
      style="background:${_YLE_BOT[n].c};color:#fff;text-decoration:none">${_YLE_BOT[n].t}</a>`).join('');
  caja.innerHTML = `<div class="card" style="margin-top:16px;border-top:5px solid #3b6fb5">
      <h2 style="margin:0 0 4px;color:var(--blue-d)">🧭 Fun for Nordic — Cambridge YLE</h2>
      <div class="muted" style="font-size:.9rem;margin-bottom:12px">Interactive course to get ready for the Cambridge Young Learners exams: units with audio, crosswords and exam tasks — with Pip, Luna and Kili!</div>
      <div style="display:flex;gap:10px;flex-wrap:wrap">${botones}</div>
      ${niveles.map(rango).join('')}
      <div class="muted" style="font-size:.85rem;margin:14px 0 6px">📚 Your books to print:</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">${
        niveles.map(n => funLibros(n, 'en', false)).join('')
      }</div>
    </div>`;
}

"""

# --- la tarjeta francesa: mismo filtro ----------------------------------
VIEJO_FR = """    const botones = ['starters','movers','flyers'].filter(n => (idx[n]||0) > 0).map(n => {"""
NUEVO_FR = """    const permiso = await funAccessDeGrado((state.profile && state.profile.grade_id) || 0, 'fr');
    const suyos = permiso === null ? ['starters','movers','flyers'] : permiso.map(f => f.level);
    const botones = ['starters','movers','flyers'].filter(n => (idx[n]||0) > 0 && suyos.includes(n)).map(n => {"""

VIEJO_FR2 = """  if (stage==='primary') frIndice().then(idx => {"""
NUEVO_FR2 = """  if (stage==='primary') frIndice().then(async idx => {"""

VIEJO_FR3 = """        ['starters','movers','flyers'].filter(n => (idx[n]||0) > 0).map(n => funLibros(n, 'fr', false)).join('')"""
NUEVO_FR3 = """        suyos.filter(n => (idx[n]||0) > 0).map(n => funLibros(n, 'fr', false)).join('')"""


def main():
    s = io.open(P, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n")

    pasos = [(VIEJO, NUEVO), (ANCLA_RELLENO, RELLENO), (ANCLA_FN, FN + ANCLA_FN),
             (VIEJO_FR2, NUEVO_FR2), (VIEJO_FR, NUEVO_FR), (VIEJO_FR3, NUEVO_FR3)]
    n = 0
    for v, x in pasos:
        if x in t:
            continue
        if t.count(v) != 1:
            print("ANCLA FALLA (%d): %r" % (t.count(v), v[:70]))
            return 1
        t = t.replace(v, x)
        n += 1

    io.open(P, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)
    print("app.js: la tarjeta del alumno respeta fun_access (%d cambios)" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
