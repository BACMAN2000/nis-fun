/* Conexion del curso con el portal — Fun for Nordic.
 *
 * El curso vive en el mismo dominio que el portal, asi que comparte su
 * sesion de Supabase: si el alumno entro por nis.cohasset.pe, aqui ya se
 * sabe quien es, sin volver a pedirle nada.
 *
 * Guarda tres cosas para que el profesor las evalue despues:
 *   writing   — lo que escribe en los ejercicios
 *   speaking  — la grabacion de voz (el audio va al bucket fun-speaking)
 *   selfcheck — el repaso final que marca el alumno
 *
 * Si no hay sesion o no hay red, el curso sigue funcionando igual: todo se
 * guarda en el navegador y no se pierde nada.
 */
window.BACKEND = (function () {

  let sb = null, alumno = null, listo = false;

  async function arranca() {
    if (listo) return alumno;
    listo = true;
    try {
      const cfg = window.NIS_CONFIG;
      if (!cfg || !window.supabase || !window.supabase.createClient) return null;
      sb = window.supabase.createClient(cfg.SUPABASE_URL, cfg.SUPABASE_KEY);
      const { data } = await sb.auth.getSession();
      alumno = data && data.session ? data.session.user : null;
      return alumno;
    } catch (e) { return null; }
  }

  function hayAlumno(){ return !!alumno; }

  /* ---- que unidades puede abrir este alumno ----
   *
   * Lo decide el profesor en el portal (tabla fun_access, una fila por
   * grado e idioma). Devuelve null cuando NO hay que cerrar nada: sin
   * sesion, sin red, o cuando ese idioma no tiene ninguna regla escrita.
   * Null es "abierto" a proposito — un candado por un fallo de red deja al
   * alumno fuera de su clase sin que nadie sepa por que.
   */
  let _permiso;
  async function permiso() {
    if (_permiso !== undefined) return _permiso;
    _permiso = null;
    await arranca();
    if (!sb || !alumno) return _permiso;
    try {
      const lang = window.LANG === 'fr' ? 'fr' : 'en';
      const { data: filas } = await sb.from('fun_access')
        .select('grade_id,level,desde,hasta,unlocked').eq('lang', lang);
      if (!filas || !filas.length) return _permiso;     // idioma sin reglas
      const { data: perfil } = await sb.from('profiles')
        .select('grade_id').eq('id', alumno.id).maybeSingle();
      const grado = perfil && perfil.grade_id;
      if (!grado) return _permiso;
      const mia = filas.find(f => f.grade_id === grado && f.unlocked &&
                                  f.level === (window.LEVEL_ACTUAL || ''));
      _permiso = mia ? { desde: mia.desde, hasta: mia.hasta }
                     : { desde: 0, hasta: -1 };          // su grado no hace este nivel
    } catch (e) { _permiso = null; }
    return _permiso;
  }

  function puedeAbrir(p, n) {
    return !p || (n >= p.desde && n <= p.hasta);
  }

  /* ---- respuestas escritas y repaso final ---- */
  async function guardar(kind, info, payload, extra) {
    await arranca();
    if (!sb || !alumno) return { ok: false, motivo: 'sin sesion' };
    const fila = Object.assign({
      student_id: alumno.id,
      // El idioma va en la fila y en la clave unica: el curso frances usa los
      // mismos niveles, unidades y codigos que el ingles, asi que sin esto la
      // entrega francesa pisaria la inglesa del mismo alumno.
      lang: (window.LANG === 'fr' ? 'fr' : 'en'),
      level: info.nivel,
      unit: info.unidad,
      activity_code: info.codigo,
      kind: kind,
      payload: payload || {}
    }, extra || {});
    const { error } = await sb.from('fun_submissions')
      .upsert(fila, { onConflict: 'student_id,lang,level,unit,activity_code,kind' });
    return error ? { ok: false, motivo: error.message } : { ok: true };
  }

  /* ---- progreso y tiempo de uso ----------------------------------------
     Sin esto, de una unidad solo queda rastro si el alumno ESCRIBE algo: los
     crucigramas, las escuchas y los juegos no dejaban nada, asi que el panel
     del profesor no podia decir si el curso se usa. Se guarda una fila por
     actividad terminada, con los segundos que estuvo delante. */
  let segundos = 0, desde = Date.now(), reloj = null;
  function cuenta(){
    if (document.visibilityState === 'visible') { segundos += Math.round((Date.now()-desde)/1000); }
    desde = Date.now();
  }
  function arrancaReloj(){
    if (reloj) return;
    document.addEventListener('visibilitychange', cuenta);
    reloj = setInterval(cuenta, 15000);
  }
  async function progreso(info, datos) {
    arrancaReloj(); cuenta();
    const r = await guardar('progress', info, Object.assign({
      hechas: (datos && datos.hechas) || 0,
      total: (datos && datos.total) || 0,
      titulo: (datos && datos.titulo) || ''
    }, datos || {}), { duration_sec: Math.min(segundos, 32000) });
    return r;
  }

  /* ---- grabacion de voz ---- */
  async function subirAudio(blob, info) {
    await arranca();
    if (!sb || !alumno) return { ok: false, motivo: 'sin sesion' };
    const ext = (blob.type || '').includes('ogg') ? 'ogg' : 'webm';
    const ruta = `${alumno.id}/${info.nivel}-u${info.unidad}-${info.codigo}.${ext}`;
    const sub = await sb.storage.from('fun-speaking')
      .upload(ruta, blob, { upsert: true, contentType: blob.type || 'audio/webm' });
    if (sub.error) return { ok: false, motivo: sub.error.message };
    const r = await guardar('speaking', info, { mime: blob.type },
                            { audio_path: ruta, duration_sec: info.segundos || null });
    return r.ok ? { ok: true, ruta } : r;
  }

  // La grabadora llama aqui sin saber nada de Supabase.
  window.REC_SUBIR = async (blob, info) => {
    const r = await subirAudio(blob, info);
    if (!r.ok) throw new Error(r.motivo);
    return r;
  };

  return { arranca, hayAlumno, guardar, progreso, subirAudio,
           permiso, puedeAbrir, alumno: () => alumno };
})();
