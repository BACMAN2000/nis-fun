/* ===== 🔐 Que unidades de Fun for Nordic ve cada grado ====================
 *
 * Una fila por grado: que nivel le toca y desde que unidad hasta cual. El
 * rango existe porque Starters lo hacen primero Y segundo grado: no es que
 * los dos vean las 45 unidades, es que se las reparten.
 *
 * REGLA, y es deliberada: mientras un idioma no tenga NINGUNA fila, ese
 * idioma esta abierto entero. Asi el dia que se estrena el panel no se le
 * cierra la puerta a ningun alumno que ya este dentro; la restriccion
 * empieza a valer cuando alguien la escribe. Es lo mismo que hace Practice
 * Tests (sin fila = desbloqueado).
 *
 * Se guarda en la tabla fun_access, con las mismas politicas que los demas
 * candados por grado: lee cualquiera (el alumno necesita saber que le toca),
 * escribe el admin o el profesor de ese grado.
 */
const FUN_NIVELES = ['starters', 'movers', 'flyers'];
/* El reparto que pidio el colegio. Es una PROPUESTA: no se escribe sola, hay
   un boton que la aplica. Flyers se queda en 5.o porque todavia no esta
   decidido si entra 6.o. */
const FUN_REPARTO = { 1: 'starters', 2: 'starters', 3: 'movers', 4: 'movers', 5: 'flyers' };

let _funAccessCache = null;

async function funAccessFilas(){
  const { data, error } = await sb.from('fun_access')
    .select('grade_id,lang,level,desde,hasta,unlocked');
  if (error) throw error;
  return data || [];
}

/* Cuantas unidades tiene cada nivel de verdad. El ingles las trae escritas;
   el frances se cuenta del indice, que es el que manda ([[nada-incompleto]]). */
async function funTotales(lang){
  if (lang === 'fr') { const i = await frIndice(); return i; }
  const o = {}; FUN_NIVELES.forEach(n => o[n] = FUN_CURSOS[n].unidades); return o;
}

async function funAccessPanel(grades){
  const permitidos = grades || GRADES;
  let filas;
  try { filas = await funAccessFilas(); }
  catch (e) { $('#main').innerHTML = `<div class="note err">${esc(e.message)}</div>`; return; }
  _funAccessCache = filas;
  const totEn = await funTotales('en'), totFr = await funTotales('fr');

  const tabla = (lang, totales) => {
    const mias = filas.filter(f => f.lang === lang);
    const abierto = mias.length === 0;
    const porGrado = {};
    mias.forEach(f => porGrado[f.grade_id] = f);
    const nombre = n => lang === 'fr' ? FUN_FR[n].curso : FUN_CURSOS[n].curso;
    const cuerpo = permitidos.map(g => {
      const f = porGrado[g.id];
      const nivel = f ? f.level : (FUN_REPARTO[g.id] || '');
      const max = totales[nivel] || 0;
      const desde = f ? f.desde : 1;
      const hasta = f ? f.hasta : (max || 1);
      const on = f ? f.unlocked : false;
      return `<tr data-g="${g.id}" data-lang="${lang}">
        <td><b>${esc(g.name)}</b></td>
        <td><select class="fa-nivel" style="min-width:15rem">
          <option value="">— sin curso —</option>
          ${FUN_NIVELES.map(n => `<option value="${n}"${n === nivel ? ' selected' : ''}>${esc(nombre(n))} (${totales[n] || 0})</option>`).join('')}
        </select></td>
        <td style="white-space:nowrap">
          <input class="fa-desde" type="number" min="1" value="${desde}" style="width:4.5rem">
          <span class="muted">a</span>
          <input class="fa-hasta" type="number" min="1" value="${hasta}" style="width:4.5rem">
        </td>
        <td style="white-space:nowrap"><span class="badge ${f && on ? 'on' : 'off'}">${!f ? '— sin regla —' : (on ? '🔓 Abierto' : '🔒 Cerrado')}</span></td>
        <td style="white-space:nowrap">
          <button class="btn sm" onclick="window._funAccessGuardar(this)">Guardar</button>
          ${f ? `<button class="btn sm ghost" onclick="window._funAccessQuitar(this)">Quitar</button>` : ''}
        </td></tr>`;
    }).join('');
    return `<div class="card" style="padding:0;overflow-x:auto">
      <div style="padding:14px 16px 0"><h2 style="margin:0">${lang === 'fr' ? '🇫🇷 Français' : '🇬🇧 English'}</h2>
        <p class="muted" style="font-size:.86rem;margin:4px 0 10px">${abierto
          ? 'Sin ninguna regla: <b>todos los grados ven los tres niveles enteros</b>. En cuanto guardes una fila, solo se verá lo que esté escrito aquí.'
          : 'Solo se ve lo escrito aquí. Un grado sin fila <b>no ve nada</b> de este idioma.'}</p></div>
      <table><thead><tr><th>Grado</th><th>Nivel</th><th>Unidades</th><th>Estado</th><th></th></tr></thead>
      <tbody>${cuerpo}</tbody></table></div>`;
  };

  $('#main').innerHTML = `<h1>🔐 Unidades por grado — Fun for Nordic</h1>
    <div class="note">Qué parte del curso puede abrir cada grado. Las unidades fuera del rango
      <b>siguen apareciendo</b> al alumno, con un candado: así ve a dónde va a llegar, pero no se adelanta.
      Es lo mismo que hace <b>📚 Activar unidades</b> con las clases.</div>
    <div class="card">
      <h2 style="margin:0 0 4px;color:var(--blue-d)">El reparto que pidió el colegio</h2>
      <div class="muted" style="font-size:.88rem;margin-bottom:12px">
        1.º y 2.º hacen <b>Starters</b>, 3.º y 4.º <b>Movers</b>, 5.º <b>Flyers</b>.
        Las 45 unidades de Starters se reparten entre 1.º y 2.º, y las 50 de Movers entre 3.º y 4.º.
        <b>6.º queda fuera</b> hasta que se decida si entra en Flyers.
        Esto no se aplica solo: revisa los rangos y pulsa el botón.</div>
      <button class="btn" onclick="window._funAccessReparto('en')">Aplicar a English</button>
      <button class="btn" onclick="window._funAccessReparto('fr')">Aplicar a Français</button>
    </div>
    ${tabla('en', totEn)}
    <div style="height:16px"></div>
    ${tabla('fr', totFr)}`;
}

function _funAccessFila(btn){
  const tr = btn.closest('tr');
  return {
    tr,
    grade_id: Number(tr.dataset.g),
    lang: tr.dataset.lang,
    level: tr.querySelector('.fa-nivel').value,
    desde: Number(tr.querySelector('.fa-desde').value),
    hasta: Number(tr.querySelector('.fa-hasta').value),
  };
}

window._funAccessGuardar = async (btn) => {
  const f = _funAccessFila(btn);
  if (!f.level) { alert('Elige un nivel, o pulsa Quitar para dejar el grado sin curso.'); return; }
  if (!(f.desde >= 1) || !(f.hasta >= f.desde)) { alert('El rango no cuadra: «hasta» tiene que ser mayor o igual que «desde».'); return; }
  btn.disabled = true;
  // un grado hace UN nivel: al guardar se van los otros del mismo idioma
  await sb.from('fun_access').delete().eq('grade_id', f.grade_id).eq('lang', f.lang).neq('level', f.level);
  const { error } = await sb.from('fun_access').upsert({
    grade_id: f.grade_id, lang: f.lang, level: f.level,
    desde: f.desde, hasta: f.hasta, unlocked: true,
    updated_at: new Date().toISOString(),
    updated_by: (state.session && state.session.user && state.session.user.id) || null,
  }, { onConflict: 'grade_id,lang,level' });
  btn.disabled = false;
  if (error) { alert('No se pudo guardar: ' + error.message); return; }
  funAccessPanel(state.profile && state.profile.role === 'admin' ? GRADES : teacherAllowedGrades());
};

window._funAccessQuitar = async (btn) => {
  const f = _funAccessFila(btn);
  if (!confirm('Sin fila, ese grado no ve nada de este idioma. ¿Quitar?')) return;
  btn.disabled = true;
  const { error } = await sb.from('fun_access').delete().eq('grade_id', f.grade_id).eq('lang', f.lang);
  btn.disabled = false;
  if (error) { alert('No se pudo quitar: ' + error.message); return; }
  funAccessPanel(state.profile && state.profile.role === 'admin' ? GRADES : teacherAllowedGrades());
};

window._funAccessReparto = async (lang) => {
  const totales = await funTotales(lang);
  const lineas = Object.entries(FUN_REPARTO)
    .filter(([g, n]) => (totales[n] || 0) > 0)
    .map(([g, n]) => `G${g} → ${lang === 'fr' ? FUN_FR[n].curso : FUN_CURSOS[n].curso} (1–${totales[n]})`);
  if (!lineas.length) { alert('Ese idioma todavía no tiene unidades.'); return; }
  if (!confirm('Se va a escribir esto, con el nivel entero para cada grado:\n\n' + lineas.join('\n') +
               '\n\nLos rangos se ajustan después a mano. ¿Seguir?')) return;
  const ahora = new Date().toISOString();
  const uid = (state.session && state.session.user && state.session.user.id) || null;
  const filas = Object.entries(FUN_REPARTO)
    .filter(([g, n]) => (totales[n] || 0) > 0)
    .map(([g, n]) => ({ grade_id: Number(g), lang, level: n, desde: 1, hasta: totales[n],
                        unlocked: true, updated_at: ahora, updated_by: uid }));
  const { error } = await sb.from('fun_access').upsert(filas, { onConflict: 'grade_id,lang,level' });
  if (error) { alert('No se pudo aplicar: ' + error.message); return; }
  funAccessPanel(state.profile && state.profile.role === 'admin' ? GRADES : teacherAllowedGrades());
};

/* Lo que puede abrir un grado, para pintar la tarjeta del alumno. Devuelve
   null si el idioma no tiene reglas — que significa "todo abierto". */
async function funAccessDeGrado(gradeId, lang){
  try {
    const filas = _funAccessCache || await funAccessFilas();
    _funAccessCache = filas;
    const mias = filas.filter(f => f.lang === lang);
    if (!mias.length) return null;                       // idioma sin reglas
    return mias.filter(f => f.grade_id === gradeId && f.unlocked);
  } catch (e) { return null; }                           // sin red, no se cierra
}
