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

  /* ---- respuestas escritas y repaso final ---- */
  async function guardar(kind, info, payload, extra) {
    await arranca();
    if (!sb || !alumno) return { ok: false, motivo: 'sin sesion' };
    const fila = Object.assign({
      student_id: alumno.id,
      level: info.nivel,
      unit: info.unidad,
      activity_code: info.codigo,
      kind: kind,
      payload: payload || {}
    }, extra || {});
    const { error } = await sb.from('fun_submissions')
      .upsert(fila, { onConflict: 'student_id,level,unit,activity_code,kind' });
    return error ? { ok: false, motivo: error.message } : { ok: true };
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

  return { arranca, hayAlumno, guardar, subirAudio,
           alumno: () => alumno };
})();
